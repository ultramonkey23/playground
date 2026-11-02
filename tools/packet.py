#!/usr/bin/env python3
"""Public Playground evidence packets. Integrity is NOT author authentication."""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "umd.playground.packet.v1"
KINDS = {"NOTE", "CHALLENGE", "EXPERIMENT", "FAILURE", "RESULT"}
STATES = {"PROPOSED", "OBSERVED", "REPRODUCED", "REFUTED", "UNKNOWN"}


def canonical_bytes(packet: dict) -> bytes:
    unsigned = {key: value for key, value in packet.items() if key != "content_sha256"}
    return json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def fingerprint(packet: dict) -> str:
    return hashlib.sha256(canonical_bytes(packet)).hexdigest()


def make_packet(title: str, actor: str, kind: str = "NOTE", *, claim: str = "", source: str = "", observed: str = "", state: str = "UNKNOWN", timestamp: str | None = None) -> dict:
    if kind not in KINDS or state not in STATES:
        raise ValueError("invalid kind or state")
    stamp = timestamp or datetime.now(timezone.utc).isoformat(timespec="seconds")
    packet = {"schema": SCHEMA, "title": title, "actor_claim": actor, "kind": kind,
              "created_utc": stamp, "claim": claim, "source_pointer": source,
              "observation": observed, "evidence_state": state,
              "authority": "PUBLIC_ADVISORY_NOT_LAB_CANON"}
    packet["content_sha256"] = fingerprint(packet)
    return packet


def validate(packet: object) -> list[str]:
    if not isinstance(packet, dict):
        return ["packet must be an object"]
    errors = []
    required = {"schema", "title", "actor_claim", "kind", "created_utc", "claim",
                "source_pointer", "observation", "evidence_state", "authority", "content_sha256"}
    if set(packet) != required:
        errors.append("required fields differ: " + ", ".join(sorted(required.symmetric_difference(packet))))
    if packet.get("schema") != SCHEMA:
        errors.append("unsupported schema")
    if packet.get("kind") not in KINDS:
        errors.append("unsupported kind")
    if packet.get("evidence_state") not in STATES:
        errors.append("unsupported evidence state")
    if packet.get("authority") != "PUBLIC_ADVISORY_NOT_LAB_CANON":
        errors.append("authority must remain advisory")
    for key in ("title", "actor_claim", "claim", "source_pointer", "observation", "created_utc"):
        if not isinstance(packet.get(key), str):
            errors.append(f"{key} must be a string")
    if not isinstance(packet.get("title"), str) or not packet["title"].strip():
        errors.append("title required")
    if not isinstance(packet.get("actor_claim"), str) or not packet["actor_claim"].strip():
        errors.append("actor claim required")
    try:
        dt = datetime.fromisoformat(packet.get("created_utc", ""))
        if dt.tzinfo is None or dt.utcoffset() is None or dt.utcoffset().total_seconds() != 0:
            errors.append("created_utc must be an offset-aware UTC timestamp")
    except (TypeError, ValueError, AttributeError):
        errors.append("created_utc is not ISO 8601")
    try:
        actual = fingerprint(packet)
    except (ValueError, TypeError):
        errors.append("packet cannot be canonically encoded")
    else:
        if packet.get("content_sha256") != actual:
            errors.append("content_sha256 mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or verify advisory, content-hashed Playground evidence packets")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("--title", required=True)
    new.add_argument("--actor", required=True)
    new.add_argument("--kind", choices=sorted(KINDS), default="NOTE")
    new.add_argument("--claim", default="")
    new.add_argument("--source", default="")
    new.add_argument("--observed", default="")
    new.add_argument("--state", choices=sorted(STATES), default="UNKNOWN")
    sub.add_parser("verify").add_argument("file", type=Path)
    args = parser.parse_args()
    if args.command == "new":
        packet = make_packet(args.title, args.actor, args.kind, claim=args.claim, source=args.source, observed=args.observed, state=args.state)
        print(json.dumps(packet, ensure_ascii=False, indent=2))
        return 0
    try:
        packet = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"INVALID: {exc}")
        return 2
    errors = validate(packet)
    print("VALID (integrity only, NOT identity/proof)" if not errors else "INVALID: " + "; ".join(errors))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
