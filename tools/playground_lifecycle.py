#!/usr/bin/env python3
"""GitHub-only Playground experiment lifecycle; no Lab host connection.

Requires an authenticated `gh` CLI when doing remote operations. In ChatGPT mobile,
AGENTS.md documents the equivalent operations through connected GitHub tools.
This client cannot authenticate that a message came from Cody: actor approval
must be independently established at the initiating interaction.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
from pathlib import PurePosixPath

PLAYGROUND = "ultramonkey23/Bone-bracket"
LAB = "ultramonkey23/ultramonkeydog-lab"
BRANCH = "master"
INGEST = "research/vault/ingest"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,79}$")
SHA_RE = re.compile(r"^[a-f0-9]{40}$")
MAX_FILE = 100_000
MAX_PACKET = 350_000


class LifecycleError(RuntimeError):
    pass


class GitHubNotFound(LifecycleError):
    pass


def api(method: str, path: str, data: dict | None = None) -> dict:
    cmd = ["gh", "api", "-X", method, "-H", "Accept: application/vnd.github+json", path]
    if data is not None:
        cmd += ["--input", "-"]
    try:
        proc = subprocess.run(cmd, input=json.dumps(data) if data is not None else None,
                              text=True, capture_output=True, timeout=45, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise LifecycleError(f"GitHub transport unavailable: {type(exc).__name__}") from exc
    if proc.returncode:
        if "HTTP 404" in proc.stderr:
            raise GitHubNotFound(f"GitHub {method} {path.split('?')[0]} not found")
        raise LifecycleError(f"GitHub {method} {path.split('?')[0]} refused (exit {proc.returncode}); no blind retry")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise LifecycleError("GitHub returned non-JSON response") from exc


def validate_id(exp_id: str) -> str:
    if not ID_RE.fullmatch(exp_id):
        raise LifecycleError("experiment ID must be a safe, relative slug")
    return exp_id


def validate_selection(items: list[str]) -> list[str]:
    if not items:
        raise LifecycleError("explicit --select paths required; never extract the whole experiment implicitly")
    result = []
    for item in items:
        path = PurePosixPath(item)
        if path.is_absolute() or len(path.parts) < 1 or any(p in (".", "..", "") for p in path.parts) or "\\" in item or path.as_posix() != item:
            raise LifecycleError(f"unsafe selected path: {item!r}")
        if item not in result:
            result.append(item)
    return result


def get_head(repo: str) -> str:
    result = api("GET", f"repos/{repo}/git/ref/heads/{BRANCH}")["object"]["sha"]
    if not SHA_RE.fullmatch(result):
        raise LifecycleError("invalid GitHub HEAD SHA")
    return result


def get_tree(repo: str, sha: str) -> tuple[str, list[dict]]:
    commit = api("GET", f"repos/{repo}/git/commits/{sha}")
    tree_sha = commit["tree"]["sha"]
    tree = api("GET", f"repos/{repo}/git/trees/{tree_sha}?recursive=1")
    if tree.get("truncated"):
        raise LifecycleError("remote tree is truncated; refuse destructive operation")
    return tree_sha, list(tree["tree"])


def read_bytes(repo: str, path: str, sha: str, *, max_bytes: int = MAX_FILE) -> bytes:
    file = api("GET", f"repos/{repo}/contents/{path}?ref={sha}")
    if file.get("type") != "file" or file.get("encoding") != "base64":
        raise LifecycleError(f"{path}: GitHub did not provide file bytes")
    if int(file.get("size", 0)) > max_bytes:
        raise LifecycleError(f"{path}: exceeds {max_bytes} byte limit")
    try:
        result = base64.b64decode("".join(file["content"].split()), validate=True)
    except (ValueError, KeyError) as exc:
        raise LifecycleError(f"{path}: malformed base64") from exc
    if len(result) > max_bytes or len(result) != file.get("size"):
        raise LifecycleError(f"{path}: decoded bytes differ from GitHub file size")
    git_blob_sha = hashlib.sha1(b"blob " + str(len(result)).encode("ascii") + b"\0" + result).hexdigest()
    if file.get("sha") != git_blob_sha:
        raise LifecycleError(f"{path}: content does not match Git blob SHA")
    return result


def build_packet(exp_id: str, head: str, files: list[tuple[str, bytes]], *,
                 question: str, author: str, consumer: str, findings: str,
                 limitations: str, next_action: str, proof: str) -> str:
    if not SHA_RE.fullmatch(head):
        raise LifecycleError("source commit must be an exact SHA")
    fields = (question, author, consumer, findings, limitations, next_action, proof)
    if any(not value.strip() for value in fields):
        raise LifecycleError("research question, author, consumer, findings, limitations, next action and proof are required")
    chunks = [f"# Playground extraction — {exp_id}", "",
              f"- **Topic / local question:** {question}",
              f"- **Author/model/provider as claimed:** {author}",
              "- **Packet identity:** deterministic by source SHA, selected bytes and operator fields; GitHub commit records staging time",
              f"- **Source:** https://github.com/{PLAYGROUND}/tree/{head}/experiments/{exp_id}",
              f"- **Exact source revision:** `{head}`",
              f"- **Intended Lab owner / consumer:** {consumer}",
              "- **Classification:** owner-selected research staging; NOT implementation, canon, Lab proof, or automatic learning", "",
              "## Useful findings", findings, "",
              "## Contradictions and limitations", limitations, "",
              "## Proposed translation / validation", next_action, "",
              "## Proof ceiling", proof, "",
              "## Owner selection", "This packet is a selected one-way extraction candidate, not a grant of authority to mutate Lab code.", "",
              "## Exact selected sources"]
    for path, payload in files:
        try:
            content = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise LifecycleError(f"{path}: only text sources may be staged in existing research intake") from exc
        digest = hashlib.sha256(payload).hexdigest()
        chunks += ["", f"### `{path}`", f"- **SHA-256:** `{digest}`", f"- **Bytes:** {len(payload)}",
                   f"- **Source:** https://github.com/{PLAYGROUND}/blob/{head}/experiments/{exp_id}/{path}",
                   "", "<details><summary>Original source text (verbatim lines)</summary>", "",
                   "~~~text", content, "~~~", "", "</details>"]
    packet = "\n".join(chunks) + "\n"
    if len(packet.encode("utf-8")) > MAX_PACKET:
        raise LifecycleError("packet exceeds bounded research intake size")
    return packet


def load_selection(exp_id: str, head: str, selected: list[str]) -> list[tuple[str, bytes]]:
    validate_id(exp_id)
    _, tree = get_tree(PLAYGROUND, head)
    all_files = {t["path"] for t in tree if t.get("type") == "blob"}
    result = []
    for rel in selected:
        full = f"experiments/{exp_id}/{rel}"
        if full not in all_files:
            raise LifecycleError(f"source file not found at pinned head: {full}")
        result.append((rel, read_bytes(PLAYGROUND, full, head)))
    return result


def remove_experiment(exp_id: str, expected_head: str, reason: str) -> str:
    """Delete files from current master without rewriting history or touching siblings."""
    validate_id(exp_id)
    if not reason.strip():
        raise LifecycleError("retirement requires a reason")
    if get_head(PLAYGROUND) != expected_head:
        raise LifecycleError("Playground master moved; do not delete under a stale snapshot")
    tree_sha, entries = get_tree(PLAYGROUND, expected_head)
    prefix = f"experiments/{exp_id}/"
    victims = [t for t in entries if t.get("type") == "blob" and t.get("path", "").startswith(prefix)]
    if not victims:
        raise LifecycleError("experiment has no active files to retire")
    changes = [{"path": t["path"], "mode": t["mode"], "type": "blob", "sha": None} for t in victims]
    new_tree = api("POST", f"repos/{PLAYGROUND}/git/trees", {"base_tree": tree_sha, "tree": changes})["sha"]
    commit = api("POST", f"repos/{PLAYGROUND}/git/commits", {"message": f"Retire experiment {exp_id}: {reason}",
                                                             "tree": new_tree, "parents": [expected_head]})["sha"]
    api("PATCH", f"repos/{PLAYGROUND}/git/refs/heads/{BRANCH}", {"sha": commit, "force": False})
    actual = get_head(PLAYGROUND)
    if actual != commit:
        raise LifecycleError("branch readback did not confirm retirement")
    _, remaining = get_tree(PLAYGROUND, actual)
    if any(t.get("type") == "blob" and t.get("path", "").startswith(prefix) for t in remaining):
        raise LifecycleError("experiment still present after retirement")
    return commit



def status() -> dict:
    """Live, read-only branch status suitable for mobile handoff."""
    head = get_head(PLAYGROUND)
    _, tree = get_tree(PLAYGROUND, head)
    experiments: dict[str, dict] = {}
    for item in tree:
        path = str(item.get("path", ""))
        bits = path.split("/")
        if len(bits) < 3 or bits[0] != "experiments" or item.get("type") != "blob":
            continue
        if not ID_RE.fullmatch(bits[1]):
            continue
        entry = experiments.setdefault(bits[1], {"id": bits[1], "files": 0, "bytes": 0})
        entry["files"] += 1
        entry["bytes"] += int(item.get("size") or 0)
    return {"result": "READ_ONLY", "repo": PLAYGROUND, "branch": BRANCH,
            "head": head, "active_experiments": sorted(experiments.values(), key=lambda e: e["id"]),
            "note": "GitHub reports current branch bytes, not execution or owner approval"}


def preview(args: argparse.Namespace) -> dict:
    """Owner-reviewable exact source selection; no Lab write or Playground deletion."""
    head = get_head(PLAYGROUND)
    if head != args.expected_head:
        raise LifecycleError("Playground master differs from supplied expected HEAD")
    selected = load_selection(args.id, head, validate_selection(args.select))
    packet = build_packet(args.id, head, selected, question=args.question, author=args.author,
                          consumer=args.consumer, findings=args.findings, limitations=args.limitations,
                          next_action=args.next_action, proof=args.proof)
    return {"result": "PREVIEW_ONLY_NO_MUTATION", "source_head": head,
            "selected": [{"path": p, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                         for p, data in selected],
            "packet_sha256": hashlib.sha256(packet.encode("utf-8")).hexdigest(),
            "packet_bytes": len(packet.encode("utf-8")),
            "lab_destination": f"{INGEST}/playground_{args.id}_{head[:12]}.md",
            "approval": "REQUIRES_DIRECT_CODY_EXTRACTION_COMMAND",
            "no_write_performed": True}


def extract(args: argparse.Namespace) -> dict:
    if not args.owner_approved:
        raise LifecycleError("explicit Cody authorization required; --owner-approved acknowledges external approval, not proof of identity")
    head = get_head(PLAYGROUND)
    if head != args.expected_head:
        raise LifecycleError("Playground master differs from supplied expected HEAD")
    selection = load_selection(args.id, head, validate_selection(args.select))
    packet = build_packet(args.id, head, selection, question=args.question, author=args.author,
                          consumer=args.consumer, findings=args.findings, limitations=args.limitations,
                          next_action=args.next_action, proof=args.proof)
    dest = f"{INGEST}/playground_{args.id}_{head[:12]}.md"
    # Confirm the current Lab research intake owner exists. This is a staging-only write.
    read_bytes(LAB, f"{INGEST}/README.md", BRANCH)
    packet_bytes = packet.encode("utf-8")
    lab_commit = None
    resumed = False
    try:
        existing = read_bytes(LAB, dest, BRANCH, max_bytes=MAX_PACKET)
    except GitHubNotFound:
        existing = None
    if existing is None:
        encoded = base64.b64encode(packet_bytes).decode("ascii")
        lab_commit = api("PUT", f"repos/{LAB}/contents/{dest}",
                         {"message": f"Stage Cody-selected Playground experiment {args.id}",
                          "content": encoded, "branch": BRANCH})["commit"]["sha"]
    elif existing == packet_bytes:
        # Recovery after an earlier successful write but failed network/cleanup.
        # An existing identical packet is safe to verify and finish retiring.
        resumed = True
    else:
        raise LifecycleError("Lab destination already exists with DIFFERENT bytes; refuse overwrite")
    readback = read_bytes(LAB, dest, BRANCH, max_bytes=MAX_PACKET)
    if readback != packet_bytes:
        raise LifecycleError("Lab readback does not match; Playground remains active")
    try:
        retired = remove_experiment(args.id, head, "verified Cody-selected extraction")
    except LifecycleError as exc:
        return {"result": "PARTIAL_LAB_WRITTEN_PLAYGROUND_STILL_ACTIVE", "lab_commit": lab_commit,
                "lab_path": dest, "resumed": resumed, "error": str(exc)}
    return {"result": "EXTRACTED_AND_RETIRED", "lab_commit": lab_commit,
            "lab_path": dest, "resumed": resumed, "playground_commit": retired}


def discard(args: argparse.Namespace) -> dict:
    if not args.reason.strip():
        raise LifecycleError("discard requires evidence-based reason")
    if get_head(PLAYGROUND) != args.expected_head:
        raise LifecycleError("Playground master differs from supplied expected HEAD")
    commit = remove_experiment(args.id, args.expected_head, "unworthy: " + args.reason)
    return {"result": "DISCARDED_FROM_ACTIVE_BRANCH", "playground_commit": commit,
            "note": "Git history remains accessible; repository files were not erased from past commits"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Disposable GitHub Playground: one-way Cody-approved Lab extraction")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="read-only list of current master experiments")
    for name in ("extract", "preview", "discard"):
        p = sub.add_parser(name)
        p.add_argument("id", type=validate_id)
        p.add_argument("--expected-head", required=True, help="exact 40-character current Playground master SHA")
    sub.choices["extract"].add_argument("--owner-approved", action="store_true",
        help="acknowledges explicit Cody authorization in the initiating interaction")
    for name in ("preview", "extract"):
        e = sub.choices[name]
        e.add_argument("--select", action="append", required=True,
                       help="experiment-relative file; repeat for each approved source")
        for option in ("question", "author", "consumer", "findings", "limitations", "next-action", "proof"):
            e.add_argument("--" + option, required=True)
    sub.choices["discard"].add_argument("--reason", required=True)
    args = parser.parse_args()
    try:
        if args.command == "status":
            result = status()
        else:
            if not SHA_RE.fullmatch(args.expected_head):
                raise LifecycleError("invalid --expected-head")
            result = (preview(args) if args.command == "preview" else
                      extract(args) if args.command == "extract" else discard(args))
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0 if result["result"] in ("EXTRACTED_AND_RETIRED", "DISCARDED_FROM_ACTIVE_BRANCH", "READ_ONLY", "PREVIEW_ONLY_NO_MUTATION") else 2
    except (LifecycleError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"result": "BLOCKED", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
