#!/usr/bin/env python3
"""Explicitly publish one bounded synthetic fusion result to the PUBLIC Playground.

Reads ~/fusion-results.json by default. Does not access or mutate the private Lab.
Uses the operator's existing gh/git authentication in an isolated public clone.
All commits are on master, fast-forward only; no credentials are stored in code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "ultramonkey23/playground"
EXPERIMENT = "002_word_math_connected_attachments"
BASE = "experiments/" + EXPERIMENT
TARGET = BASE + "/latest_results.json"
REVIEW = BASE + "/review.json"
SCHEMA = "umd.playground.organ_fusion_discovery.v1"
EXPECTED_PROBES = frozenset({
    "neurodaemon_affinity_vs_placement",
    "four_mind_semantic_tool_fit",
    "scribe_spine_scope_integrity",
    "socket_graph_visibility",
    "socket_fabric_authority_boundary",
    "structural_connected_policy",
    "bioelectric_to_daemon_candidate",
})
SAFE_TOP_LEVEL = frozenset({
    "schema", "status", "branch", "lab_head", "proof_ceiling",
    "explicit_lab_write_operations", "private_source_in_output", "probes",
})
SECRET_PATTERN = re.compile(
    r"(?i)(?:github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]{12,}"
    r"|sk-[A-Za-z0-9]{16,}|-----BEGIN [^-]*PRIVATE KEY-----"
    r"|/data/data/com[.]termux/|/home/[^/\s]+/|/Users/[^/\s]+/"
    r"|(?:bearer|authorization)\s*[:=]\s*\S+)"
)
PRIVATE_KEYS = frozenset({
    "access_token", "api_key", "password", "private_key", "secret",
    "credential", "traceback", "private_source", "source_code", "raw_source",
})


class PublishError(RuntimeError):
    pass


def _walk_safe(value: object, level: int = 0) -> None:
    if level > 20:
        raise PublishError("Result nesting too deep for public inspection")
    if isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(k, str) or k.lower() in PRIVATE_KEYS or SECRET_PATTERN.search(k):
                raise PublishError("Unsafe result field name; no public write performed")
            _walk_safe(v, level + 1)
    elif isinstance(value, list):
        for entry in value:
            _walk_safe(entry, level + 1)
    elif isinstance(value, str):
        if len(value) > 3000 or SECRET_PATTERN.search(value) or "\x00" in value:
            raise PublishError("Possible private data or oversized text; no public write performed")
    elif value is None or isinstance(value, (int, float, bool)):
        return
    else:
        raise PublishError("Unsupported result value type")


def validate_result(data: object) -> dict:
    if not isinstance(data, dict) or set(data) != SAFE_TOP_LEVEL:
        raise PublishError("Not the expected bounded Playground probe schema")
    if data.get("schema") != SCHEMA or data.get("status") != "OBSERVED":
        raise PublishError("Only fully observed synthetic fusion runs can be published")
    if data.get("branch") != "master" or not re.fullmatch(r"[a-f0-9]{40}", str(data.get("lab_head", ""))):
        raise PublishError("Missing exact private Lab master revision")
    if data.get("explicit_lab_write_operations") != 0 or type(data.get("explicit_lab_write_operations")) is not int:
        raise PublishError("Cannot publish a result reporting Lab write operations")
    if data.get("private_source_in_output") is not False:
        raise PublishError("Cannot publish result marked as containing private Lab source")
    cases = data.get("probes")
    if not isinstance(cases, list) or len(cases) != len(EXPECTED_PROBES):
        raise PublishError("Expected seven recorded probes")
    names = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"probe", "state", "observation"}:
            raise PublishError("Unexpected probe record shape")
        if case.get("state") != "OBSERVED" or not isinstance(case.get("observation"), dict):
            raise PublishError("Incomplete or unobserved probe record")
        names.append(case.get("probe"))
    if len(names) != len(set(names)) or set(names) != EXPECTED_PROBES:
        raise PublishError("Probe names do not match the expected public experiment")
    _walk_safe(data)
    serialized = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    if len(serialized.encode("utf-8")) > 250_000:
        raise PublishError("Result too large for public publishing")
    return data


def _command(argv: list[str], *, cwd: Path | None = None, timeout: int = 90) -> str:
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublishError("Required GitHub command unavailable or timed out: " + type(exc).__name__) from exc
    if p.returncode:
        # Avoid copying process environment, credentials or detailed GitHub
        # diagnostics into the public artifact.
        raise PublishError("Command failed (" + argv[0] + " " + argv[1] + ", exit "
                           + str(p.returncode) + ")")
    return p.stdout.strip()


def prepare_review(review: dict, lab_head: str, digest: str) -> dict:
    if not isinstance(review, dict) or review.get("schema") != "umd.playground.review.v1" \
            or review.get("id") != EXPERIMENT:
        raise PublishError("Public review record has changed format")
    evidence = review.get("evidence")
    if not isinstance(evidence, list):
        raise PublishError("Review evidence is malformed")
    review = dict(review)
    review["status"] = "REVIEW_READY"
    review["summary"] = (
        "A complete corrected seven-probe synthetic fusion run was published from an "
        "authenticated Termux GitHub session for private Lab master " + lab_head[:12] +
        ". All seven records reported OBSERVED. The latest raw, bounded observations "
        "are in latest_results.json; downstream benefits are NOT independently "
        "evaluated or proven. Earlier findings remain in FINDINGS.md."
    )
    row = {
        "kind": "OPERATOR_PUBLISHED_COMPLETE_TERMUX_RUN",
        "environment": "User-hosted Termux synthetic Lab module execution; private Lab master " + lab_head,
        "observation": "7/7 probes OBSERVED; public result SHA-256 " + digest +
                       ". GitHub authentication establishes publication provenance, not independent runtime attestation.",
        "source": "latest_results.json",
    }
    review["evidence"] = [row] + [
        item for item in evidence if not (
            isinstance(item, dict) and item.get("kind") == row["kind"]
        )
    ]
    review["limitations"] = [
        line for line in review.get("limitations", [])
        if not ("updated harness requires a new run" in line.lower()
                or "the termux output was truncated" in line.lower())
    ]
    followup_limit = (
        "New output is user-hosted synthetic execution, not independent device "
        "attestation or proof of a production capability upgrade."
    )
    if followup_limit not in review["limitations"]:
        review["limitations"].append(followup_limit)
    review["next_actions"] = [
        "Review latest_results.json for correct negative-stress behavior, Four Mind "
        "positive-control coverage, and bridge diversity versus baseline.",
    ] + [
        item for item in review.get("next_actions", [])
        if not item.startswith("Review latest_results.json")
    ]
    review["recommended_action"] = "REVIEW"
    review["recommendation_reason"] = (
        "A complete corrected result is now available. Interpret causality, "
        "downstream behavior and regressions before considering integration."
    )
    selected = review.get("files")
    if not isinstance(selected, list):
        raise PublishError("Review file selection is malformed")
    review["files"] = selected if any(
        isinstance(x, dict) and x.get("path") == "latest_results.json" for x in selected
    ) else [{"path": "latest_results.json", "label": "Latest complete published synthetic results"}] + selected
    return review


def publish_result(data: dict) -> dict:
    validate_result(data)
    serial = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
    digest = hashlib.sha256(serial.encode("utf-8")).hexdigest()
    with tempfile.TemporaryDirectory(prefix="playground-public-publish-") as tmp:
        working = Path(tmp) / "playground"
        _command(["gh", "repo", "clone", REPO, str(working),
                  "--", "--depth", "1", "--branch", "master"], timeout=180)
        branch = _command(["git", "branch", "--show-current"], cwd=working)
        if branch != "master":
            raise PublishError("Public clone is not on master; refusing write")
        if _command(["git", "status", "--porcelain"], cwd=working):
            raise PublishError("Unexpected dirty public clone; refusing write")
        destination = working / TARGET
        review_path = working / REVIEW
        if not review_path.is_file() or not (working / BASE / "probe_fusions.py").is_file():
            raise PublishError("Expected active experiment does not exist on public master")
        review_data = json.loads(review_path.read_text(encoding="utf-8"))
        updated = prepare_review(review_data, data["lab_head"], digest)
        destination.write_text(serial, encoding="utf-8")
        review_path.write_text(json.dumps(updated, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        _command(["git", "add", "--", TARGET, REVIEW], cwd=working)
        changes = _command(["git", "diff", "--cached", "--name-only"], cwd=working)
        if changes:
            _command(["git", "commit", "-m",
                      "Publish complete Termux fusion probe result for Playground review"], cwd=working)
            _command(["git", "push", "origin", "HEAD:master"], cwd=working, timeout=120)
        commit = _command(["git", "rev-parse", "HEAD"], cwd=working)
        # Read the remote again and verify both published artifact bytes.
        _command(["git", "fetch", "origin", "master"], cwd=working, timeout=120)
        remote_json = _command(["git", "show", "FETCH_HEAD:" + TARGET], cwd=working)
        remote_review = _command(["git", "show", "FETCH_HEAD:" + REVIEW], cwd=working)
        if remote_json + "\n" != serial or json.loads(remote_review) != updated:
            raise PublishError("Push may have succeeded but public readback did not match")
        return {
            "result": "PUBLISHED_TO_PUBLIC_PLAYGROUND",
            "lab_written": False,
            "public_commit": commit,
            "lab_head": data["lab_head"],
            "probes": len(data["probes"]),
            "sha256": digest,
            "review_url": "https://ultramonkey23.github.io/playground/?experiment=" + EXPERIMENT,
        }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Publish synthetic fusion result to PUBLIC Playground master (public Git history persists)")
    p.add_argument("file", nargs="?", type=Path,
                   default=Path.home() / "fusion-results.json",
                   help="default: ~/fusion-results.json")
    args = p.parse_args()
    try:
        source = args.file.expanduser()
        if not source.is_file() or source.stat().st_size > 250_000:
            raise PublishError("Expected bounded result JSON not found: " + str(source))
        data = json.loads(source.read_text(encoding="utf-8"))
        result = publish_result(data)
        print(json.dumps(result, indent=2))
        return 0
    except (PublishError, ValueError, OSError) as exc:
        print("PUBLICATION_NOT_PERFORMED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
