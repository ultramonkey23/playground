#!/usr/bin/env python3
"""Validate public review metadata without running experimental code."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path, PurePosixPath

SCHEMA = "umd.playground.review.v1"
STATES = {"ACTIVE", "REVIEW_READY", "BLOCKED"}
ACTIONS = {"REVIEW", "KEEP", "IMPROVE", "EXTRACT", "DISCARD"}
ID = re.compile(r"^[a-z0-9][a-z0-9_-]{2,79}$")


def validate(data: object, experiment: Path) -> list[str]:
    if not isinstance(data, dict):
        return ["review must be a JSON object"]
    errors = []
    if data.get("schema") != SCHEMA:
        errors.append("unsupported schema")
    if data.get("id") != experiment.name or not ID.fullmatch(str(data.get("id", ""))):
        errors.append("review id must match its experiment directory")
    for key in ("title", "question", "summary", "recommendation_reason"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(key + " must be nonempty text")
    if data.get("status") not in STATES:
        errors.append("invalid status")
    if data.get("recommended_action") not in ACTIONS:
        errors.append("invalid recommendation")
    for key in ("limitations", "next_actions"):
        values = data.get(key)
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            errors.append(key + " must be a list of nonempty strings")
    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for i, item in enumerate(evidence):
            if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip()
                for k in ("kind", "environment", "observation", "source")):
                errors.append(f"evidence[{i}] requires kind/environment/observation/source")
    files = data.get("files")
    if not isinstance(files, list):
        errors.append("files must be an explicit list")
    else:
        seen = set()
        for item in files:
            if not isinstance(item, dict):
                errors.append("file entries must be objects")
                continue
            name, label = item.get("path"), item.get("label")
            if not isinstance(name, str) or not isinstance(label, str) or not label.strip():
                errors.append("file entries require path and label strings")
                continue
            p = PurePosixPath(name)
            if p.is_absolute() or p.as_posix() != name or "\\" in name or name.startswith("/") or any(
                segment in ("", ".", "..") for segment in name.split("/")
            ) or name in seen:
                errors.append("unsafe or duplicate selected path: " + name)
                continue
            seen.add(name)
            target = experiment / name
            if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(experiment.resolve()):
                errors.append("selected file missing or unsafe: " + name)
    issue = data.get("issue_number")
    if issue is not None and (type(issue) is not int or issue <= 0):
        errors.append("issue_number must be positive integer or null")
    return errors


def scan(root: Path) -> list[tuple[str, list[str]]]:
    results = []
    for file in sorted(root.glob("*/review.json")):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            errs = validate(data, file.parent)
        except (ValueError, OSError) as e:
            errs = [type(e).__name__ + ": " + str(e)]
        results.append((str(file), errs))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate active Playground review manifests")
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent / "experiments")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("experiments directory missing")
    results = scan(args.root)
    for name, errors in results:
        print(("INVALID" if errors else "VALID") + ": " + name)
        for error in errors:
            print("  - " + error)
    if not results:
        print("NO REVIEW FILES; an empty set is not validation success for any experiment")
    print(f"Review summaries: {len(results)}, invalid: {sum(bool(e) for _, e in results)}")
    return int(any(errors for _, errors in results))


if __name__ == "__main__":
    raise SystemExit(main())
