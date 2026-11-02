#!/usr/bin/env python3
"""Compare actual existing Word Math fusion paths and an in-memory candidate edge.

Imports real private Lab modules from an authenticated checkout. Never executes
text as a shell command or invokes Lab mutation/dispatch functions. Public repo
contains only this harness and synthetic inputs; do not publish private source.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import importlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

LAB_REPO = "ultramonkey23/ultramonkeydog-lab"
SCHEMA = "umd.playground.organ_fusion_discovery.v1"

def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True, timeout=25).stdout.strip()

def check_checkout(root: Path) -> dict:
    if git(root, "branch", "--show-current") != "master":
        raise RuntimeError("must use private Lab master, not a detached or alternate branch")
    if git(root, "status", "--porcelain"):
        raise RuntimeError("private Lab checkout is dirty; refusing ambiguous local state")
    if not (root / "labcore/word_math.py").is_file():
        raise RuntimeError("not the private Lab checkout")
    return {"lab_head": git(root, "rev-parse", "HEAD"), "branch": "master"}

def modules(root: Path, names: tuple[str, ...]) -> dict:
    sys.path.insert(0, str(root))
    loaded = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for name in names:
            mod = importlib.import_module("labcore." + name)
            origin = Path(mod.__file__).resolve()
            if not origin.is_relative_to(root.resolve()):
                raise RuntimeError("module import resolved outside requested Lab")
            loaded[name] = mod
    return loaded

def semantic(mods: dict, text: str) -> dict:
    wm = mods["word_math"]
    return wm.semantic_vector_from_words(wm.extract_word_packet(text))

def compact_daemons(rows: list[dict]) -> list[dict]:
    return [
        {"archetype": str(d["archetype"]), "target": str(d["target_bridge"]),
         "spawn_score": d["spawn_score"], "semantic_affinity": d["semantic_affinity"]}
        for d in rows
    ]

def probe_neurodaemon(mods: dict) -> dict:
    myc = mods["mycelial_pattern_fusion"]
    phrases = {
        "neutral": "",
        "proof": "verified proof validated tests and evidence",
        "repair": "repair broken structures and improve recovery",
        "fusion": "fuse systems together and optimize architecture",
    }
    outputs = {}
    for label, phrase in phrases.items():
        env = myc._mission_semantic_environment(phrase)
        daemons = myc._calculate_neurodaemon_swarm([], [], semantic_environment=env)
        outputs[label] = compact_daemons(daemons)
    base = outputs["neutral"]
    return {
        "existing_link": "Word Math language testimony -> Mycelial Neurodaemon semantic context",
        "cases": outputs,
        "placement_changed": {k: [x["target"] for x in v] != [x["target"] for x in base]
                              for k,v in outputs.items() if k != "neutral"},
        "score_changed": {k: [x["spawn_score"] for x in v] != [x["spawn_score"] for x in base]
                          for k,v in outputs.items() if k != "neutral"},
        "affinity_changed": {k: [x["semantic_affinity"] for x in v] != [x["semantic_affinity"] for x in base]
                             for k,v in outputs.items() if k != "neutral"},
        "proof_ceiling": "synthetic advisory daemon comparison; no real mission executed",
    }

def probe_mind_profiles(mods: dict) -> dict:
    mind = mods["four_mind"]
    profiles = {
        "proof_specialist": semantic(mods, "verify test proof evidence"),
        "repair_specialist": semantic(mods, "repair fix recover broken systems"),
        "fusion_specialist": semantic(mods, "fuse merge architecture systems"),
    }
    tasks = {
        "verify": "verify evidence and test safety",
        "repair": "repair broken systems",
        "fuse": "fuse architecture and connected systems",
    }
    result = {}
    for label, text in tasks.items():
        ranked = mind._rank_tool_semantic_profiles(semantic(mods, text), profiles)
        result[label] = {
            "top_match": (ranked.get("top_match") or {}).get("tool"),
            "ranked": [
                {"profile": v["tool"], "resonance": v["resonance_score"],
                 "coverage": v["mission_coverage"]}
                for v in ranked.get("ranked_profiles", [])
            ],
        }
    return {"existing_link": "Word Math -> Four Mind tool-profile capability fit",
            "tasks": result,
            "distinct_winners": len({r["top_match"] for r in result.values()}),
            "proof_ceiling": "advisory ranking, not executor selection or outcome"}

def probe_scribe_scope(mods: dict) -> dict:
    wm, scribe, spine = (mods[k] for k in
                         ("word_math", "scribe_translation", "zero_point_spine"))
    phrases = {
        "prohibition": "Do not push origin.",
        "question": "Could you push origin?",
        "conditional": "Only if tests pass, must push origin after the receipt is verified.",
        "claimed_proof": "Cody claims the tests passed, but maybe the build failed.",
    }
    outputs = {}
    for label, phrase in phrases.items():
        direct = wm.word_math_packet(phrase, seed="playground-fusion", jitter=0.0)
        testimony = scribe._word_math_semantic_testimony(phrase)
        gate = spine.evaluate_program_text(phrase, seed="playground-fusion", jitter=0.0)
        outputs[label] = {
            "scribe_handoff_result": testimony.get("result"),
            "semantic_vector_preserved": testimony.get("semantic_vector") == direct["semantic_vector"],
            "scoped_summary_preserved": (testimony.get("scoped_events") or {}).get("summary")
                                        == direct.get("scoped_event_lowering", {}).get("summary"),
            "scribe_may_execute": testimony.get("may_execute"),
            "zero_point_execution_state": gate.get("execution_state"),
            "zero_point_scope_decision": gate.get("scope_decision"),
        }
    return {"existing_links": ["Scribe -> Word Math testimony",
                                "Word Math -> Zero Point Spine gates"],
            "cases": outputs, "proof_ceiling": "language as synthetic data, never commands"}

def probe_socket_visibility(mods: dict, root: Path) -> dict:
    reg = mods["math_socket_registry"]
    owners = (
        "power_router", "zero_point_spine", "action_math_fusion",
        "scribe_translation", "four_mind", "mycelial_pattern_fusion",
        "morphogenesis_grid", "goal_gravity", "sense_calibration",
        "dimensional_compiler", "growth_physics",
    )
    direct_imports = []
    for owner in owners:
        path = root / "labcore" / (owner + ".py")
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        found = any(
            isinstance(n, ast.ImportFrom)
            and ((n.module == "labcore.word_math")
                 or (n.module == "labcore" and any(x.name == "word_math" for x in n.names)))
            or isinstance(n, ast.Import)
            and any(x.name == "labcore.word_math" for x in n.names)
            for n in ast.walk(tree)
        )
        if found:
            direct_imports.append(owner)
    sockets = [d for d in reg.DOGFOOD_SOCKETS if d.producer_id == "word_math"]
    declared = sorted({req.consumer_id for d in sockets for req in d.consumers})
    return {
        "declared_socket_consumers": declared,
        "allowlisted_direct_source_importers": sorted(direct_imports),
        "direct_importers_not_in_declared_socket_consumer_set": sorted(set(direct_imports) - set(declared)),
        "meaning": "Different inventories: a source import is not a typed socket subscription nor runtime use",
        "proof_ceiling": "live source AST and registered static declarations, not runtime wiring proof",
    }

def probe_bioelectric_daemon_candidate(mods: dict) -> dict:
    myc = mods["mycelial_pattern_fusion"]
    morph = mods["morphogenesis_grid"]
    target = "four_mind_to_pattern_fusion"
    outcomes = {}
    phrases = {
        "proof": "verified tests proof evidence passed",
        "hazard": "delete everything danger damage destructive",
    }
    for label, phrase in phrases.items():
        grid = morph.MorphogenesisGrid({target: ["neighbor"], "neighbor": [target]})
        grid.cells[target].voltage = 0.7
        grid.cells["neighbor"].voltage = 0.7
        signal = grid.inject_semantic_stress(target, semantic(mods, phrase))
        grid.step(steps=12)
        after = grid.cells[target].voltage
        rows = {}
        for gain in (0.0, 0.5, 1.0, 2.0):
            # This conversion is a NEW TEMPORARY EXPERIMENTAL ADAPTER, not a Lab law.
            # Gain 0 is the no-adapter control; positive gains are a sweep.
            resistance = max(0.1, 1.0 + gain * (0.7 - after))
            paths = [{"path": target, "resistance": resistance}]
            daemons = myc._calculate_neurodaemon_swarm(
                [], paths, semantic_environment=myc._mission_semantic_environment(phrase)
            )
            rows[str(gain)] = {
                "derived_resistance": round(resistance, 6),
                "assignments": [d["target_bridge"] for d in daemons],
                "spawn_scores": [d["spawn_score"] for d in daemons],
            }
        outcomes[label] = {"semantic_signal": signal, "voltage": after, "gain_sweep": rows}
    return {
        "existing_links": ["Word Math -> Morphogenesis semantic stress",
                            "Word Math -> Mycelial advisory semantic affinity"],
        "new_in_memory_candidate": "Morphogenesis voltage -> candidate bridge resistance -> Neurodaemon placement",
        "candidate_is_not_lab_wiring": True,
        "assumption": "resistance=clamp_min(0.1,1+gain*(0.7-voltage)); gain sweep is NOT calibrated",
        "conditions": outcomes, "proof_ceiling": "synthetic in-memory adapter only; never registered or persisted",
    }

PROBES = (
    ("neurodaemon_affinity_vs_placement", ("word_math", "mycelial_pattern_fusion"), probe_neurodaemon),
    ("four_mind_semantic_tool_fit", ("word_math", "four_mind"), probe_mind_profiles),
    ("scribe_spine_scope_integrity", ("word_math", "scribe_translation", "zero_point_spine"), probe_scribe_scope),
    ("socket_graph_visibility", ("math_socket_registry",), probe_socket_visibility),
    ("bioelectric_to_daemon_candidate", ("word_math", "morphogenesis_grid", "mycelial_pattern_fusion"), probe_bioelectric_daemon_candidate),
)

def run(root: Path) -> dict:
    origin = check_checkout(root)
    sys.dont_write_bytecode = True
    results = []
    for label, required, func in PROBES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                loaded = modules(root, required)
                observation = func(loaded, root) if label == "socket_graph_visibility" else func(loaded)
            results.append({"probe": label, "state": "OBSERVED", "observation": observation})
        except Exception as exc:
            results.append({"probe": label, "state": "UNAVAILABLE",
                            "error_type": type(exc).__name__,
                            "note": "See local traceback if needed. No private exception text is published."})
    if git(root, "status", "--porcelain"):
        return {"schema": SCHEMA, "status": "BLOCKED",
                "reason": "private checkout changed during observation; quarantine the output",
                **origin}
    return {
        "schema": SCHEMA, "status": "OBSERVED" if all(r["state"] == "OBSERVED" for r in results) else "PARTIAL",
        **origin, "proof_ceiling": "real module functions in isolated synthetic exercises; not whole Lab operation",
        "explicit_lab_write_operations": 0, "private_source_in_output": False, "probes": results,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Measure existing Word Math fusions, not rewire the Lab")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--clone-private", action="store_true",
                       help="clone a clean private master temporarily using authenticated gh")
    group.add_argument("--lab-root", type=Path, help="use a CLEAN existing private Lab master checkout")
    args = parser.parse_args()
    try:
        if args.clone_private:
            with tempfile.TemporaryDirectory(prefix="lab-fusion-probe-") as directory:
                root = Path(directory) / "lab"
                subprocess.run(["gh", "repo", "clone", LAB_REPO, str(root),
                                "--", "--depth", "1", "--branch", "master"],
                               check=True, capture_output=True, text=True, timeout=180)
                output = run(root)
        else:
            output = run(args.lab_root.expanduser().resolve())
    except Exception as exc:
        output = {"schema": SCHEMA, "status": "BLOCKED", "error_type": type(exc).__name__,
                  "reason": "Private clone/import/environment blocked; Lab execution UNKNOWN"}
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0 if output["status"] == "OBSERVED" else 2

if __name__ == "__main__":
    raise SystemExit(main())
