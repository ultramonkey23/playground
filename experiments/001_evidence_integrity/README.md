# Experiment 001 — evidence integrity is not evidence truth

**Hypothesis:** a SHA-256 digest over canonical JSON detects post-creation modification of a packet's observation field. This **does not** prove who authored the packet, whether the observation is true, or whether the Lab consumed it.

## Run

From repository root:

```sh
python3 experiments/001_evidence_integrity/demo.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
python3 tools/packet.py new --title "Independent observation" --actor "mobile-chat" --kind EXPERIMENT --claim "test" --observed "example" --state OBSERVED
```

Expected: the original packet validates, an observation changed without recalculating its hash fails validation, and integrity tests pass. **Recalculation by an attacker can produce a new valid digest:** no cryptographic author signature exists.

## Proof

The founding session executed the prototype locally before publication: five focused Python tests passed and the negative control returned `content_sha256 mismatch`. Rerun on checked-out GitHub source to reproduce; do not treat a report as a substitute for independently executing the code.

See [tools/packet.py](../../tools/packet.py) and [tools/test_packet.py](../../tools/test_packet.py).
