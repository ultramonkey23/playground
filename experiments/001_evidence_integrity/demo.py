#!/usr/bin/env python3
"""Negative control: integrity catches altered observations, not fake authors."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from packet import make_packet, validate


original = make_packet("Can a digest detect altered evidence?", "demo", "EXPERIMENT",
                       claim="SHA-256 digest catches accidental edits",
                       observed="baseline result", state="OBSERVED",
                       timestamp="2026-11-02T00:00:00+00:00")
tampered = dict(original)
tampered["observation"] = "fabricated result"
result = {"original_errors": validate(original), "tampered_errors": validate(tampered),
          "expected_detection": "content_sha256 mismatch",
          "author_authentication": "NOT PROVIDED",
          "lab_integration": "NOT TESTED"}
print(json.dumps(result, indent=2))
if result["original_errors"] or result["expected_detection"] not in result["tampered_errors"]:
    raise SystemExit(1)
