#!/usr/bin/env python3
"""Read-only probes of REAL private Lab modules using synthetic public fixtures.

No private Lab source is copied into this public repository. This file never
executes a natural-language instruction, patches the Lab, or writes Lab state.
"""
from __future__ import annotations
import argparse
import contextlib
import importlib
import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "umd.playground.word_math_connected_probes.v1"
LAB_REPO = "ultramonkey23/ultramonkeydog-lab"
MODULES = (
    "labcore.word_math", "labcore.validation", "labcore.routing",
    "labcore.zero_point_spine", "labcore.morphogenesis_grid",
    "labcore.goal_gravity",
)

def git_head(root):
    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              capture_output=True, text=True, timeout=20).stdout.strip()
    branch, sha = git("branch", "--show-current"), git("rev-parse", "HEAD")
    if branch != "master" or len(sha) != 40 or not (root / "labcore/word_math.py").is_file():
        raise RuntimeError("private Lab master checkout required")
    return sha

def imports(root):
    sys.path.insert(0, str(root))
    modules, failures = [], {}
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
            if not Path(mod.__file__).resolve().is_relative_to(root.resolve()):
                raise RuntimeError("module not loaded from selected Lab")
            modules.append(mod)
        except Exception as exc:
            modules.append(None)
            failures[name] = type(exc).__name__
    return modules, failures

def sem(wm, phrase):
    return wm.semantic_vector_from_words(wm.extract_word_packet(phrase))

def sequence_and_prerequisites(wm, *mods):
    # Own composition, not a reimplementation.
    ab = wm.compose("must push", "may stop")
    ba = wm.compose("may stop", "must push")
    gates = {str(s): wm.compose_conditional(
        {"execution_pressure": 0.9}, {"execution_pressure": 1.0},
        {"execution_pressure": s})["execution_pressure"] for s in (0.0, 0.5, 1.0)}
    shared = wm.semantic_overlap(
        sem(wm, "must run and fix with proof"),
        sem(wm, "run the repair and verify with proof"))
    assert ab["composed_vector"] != ba["composed_vector"], "lost causal order"
    assert gates == {"0.0": 0.0, "0.5": 0.45, "1.0": 0.9}, "lost prerequisite gating"
    return {"different_when_reversed": True, "forward_intent": ab["intent"],
            "reverse_intent": ba["intent"], "reality_gate_values": gates,
            "shared_activation": shared["shared_activation"],
            "shared_resonance": shared["resonance_score"]}

def execution_and_consent(wm, validation, routing, spine, *mods):
    cases = {
        "benign": "please forge a mission for the lab",
        "destructive": "rm -rf everything and delete all files",
        "conditional": "push if tests pass",
        "negated": "do not push to origin",
    }
    observed = {}
    for name, phrase in cases.items():
        d = spine.evaluate_program_text(phrase, seed="playground", jitter=0.0)
        observed[name] = {"execution_state": d["execution_state"],
                          "next_state": d["recommended_next_state"],
                          "action_tier": d["action_tier"],
                          "scope_decision": d["scope_decision"]}
    assert observed["destructive"]["execution_state"] == "HARD_BLOCKED"
    assert observed["conditional"]["execution_state"] != "EXECUTION_ALLOWED_AFTER_YES"
    assert "push" not in wm.extract_word_packet(cases["negated"])["intent_verbs"]
    return observed

def connected_systems_and_word_math(wm, validation, routing, *mods):
    tasks = {
        "small": "fix readme small output",
        "cross_organ": "deep improve broad connected systems and mesh wiring across organs",
        "game_systems": "deep improve combat progression economy save systems and their cross-system dependencies",
    }
    comparison = {}
    for name, task in tasks.items():
        plan = validation.validation_plan_data(task, project="lab", execute=False)
        posture = routing._execution_posture(task, "script")
        comparison[name] = {
            "validation_tier": plan.get("recommended_tier"),
            "connected_systems_policy": (plan.get("system_strategy") or {}).get("policy"),
            "connected_inspection_required": (plan.get("system_strategy") or {}).get("required"),
            "routing_integration_policy": posture.get("system_integration_policy"),
            "word_math_activation": wm.semantic_activation_vector(sem(wm, task)),
            "required_check_count": len(plan.get("required_checks") or []),
        }
    assert comparison["small"]["connected_systems_policy"] == "REUSE_EXISTING_ORGANS_WHEN_PRESENT"
    assert comparison["cross_organ"]["connected_systems_policy"] == "CONNECTED_SYSTEMS_FIRST"
    assert comparison["cross_organ"]["connected_inspection_required"] is True
    return {"cases": comparison, "proof_ceiling": "side-by-side authentic organs; Word Math is NOT wired into this validation policy by the probe"}

def bioelectric_attachment(wm, validation, routing, spine, morph, *mods):
    inputs = {"hazard": "rm -rf all files with force",
              "proof": "tests verified and passed with proof receipt"}
    result = {}
    for name, phrase in inputs.items():
        grid = morph.MorphogenesisGrid({"router": ["proof"], "proof": ["router"]})
        grid.cells["router"].voltage = 0.7
        grid.cells["proof"].voltage = 0.7
        signal = grid.inject_semantic_stress("router", sem(wm, phrase))
        grid.step(steps=12)
        result[name] = {"signal": signal, "router_voltage": grid.cells["router"].voltage,
                        "neighbor_voltage": grid.cells["proof"].voltage}
    assert result["hazard"]["signal"] < 0 < result["proof"]["signal"]
    assert result["hazard"]["router_voltage"] < result["proof"]["router_voltage"]
    return {"cases": result, "steps": 12, "starting_voltage": 0.7}

def gravity_attachment(wm, validation, routing, spine, morph, gravity):
    texts = {"delivery": "urgent mission to push and commit with proof",
             "hazard": "rm -rf all files with force",
             "repair": "run verification and test with proof"}
    result = {}
    for name, phrase in texts.items():
        cfg, proof = gravity.semantic_potential_field_config(
            sem(wm, phrase), gravity.PotentialFieldConfig())
        field = gravity.evaluate_potential_and_force(
            x=(1.0, 1.0), x_goal=(0.0, 0.0),
            proof_density=proof, config=cfg)
        result[name] = {"k_goal": cfg.k_goal, "k_obstacle": cfg.k_obstacle,
                        "proof_density": proof, "potential_energy": field["potential_energy"],
                        "net_force": field["net_force"]}
    assert result["hazard"]["k_obstacle"] >= result["repair"]["k_obstacle"]
    return {"cases": result, "proof_ceiling": "simulated field, not a real project trajectory"}

PROBES = [
    ("sequence_and_prerequisites", sequence_and_prerequisites, (0,)),
    ("execution_and_consent", execution_and_consent, (0, 3)),
    ("connected_systems_and_word_math", connected_systems_and_word_math, (0, 1, 2)),
    ("bioelectric_attachment", bioelectric_attachment, (0, 4)),
    ("gravity_attachment", gravity_attachment, (0, 5)),
]

def run(root):
    head = git_head(root)
    with contextlib.redirect_stdout(io.StringIO()):
        modules, failures = imports(root)
    results = []
    for label, func, required in PROBES:
        missing = [MODULES[n] for n in required if modules[n] is None]
        if missing:
            results.append({"case": label, "state": "BLOCKED", "missing_modules": missing,
                            "import_error_types": {m: failures[m] for m in missing}})
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                output = func(*modules)
            results.append({"case": label, "state": "PASS", "observations": output})
        except Exception as exc:
            results.append({"case": label, "state": "FAIL", "error_type": type(exc).__name__,
                            "note": "Debug locally; private tracebacks intentionally excluded."})
    status = "PASS" if all(x["state"] == "PASS" for x in results) else "PARTIAL"
    return {"schema": SCHEMA, "status": status, "lab_head": head, "lab_branch": "master",
            "private_source_exported": False, "lab_write_performed": False,
            "runtime": "real private Lab imports, synthetic fixtures, read-only",
            "cases": results}

def main():
    p = argparse.ArgumentParser(description="Probe Word Math and Connected Systems in actual Lab checkout")
    where = p.add_mutually_exclusive_group(required=True)
    where.add_argument("--lab-root", type=Path, help="existing private Lab master clone")
    where.add_argument("--clone-private", action="store_true", help="temporary authenticated gh clone, auto-cleaned")
    args = p.parse_args()
    try:
        if args.clone_private:
            with tempfile.TemporaryDirectory(prefix="umd-playground-lab-") as temp:
                root = Path(temp) / "lab"
                subprocess.run(["gh", "repo", "clone", LAB_REPO, str(root),
                                "--", "--depth", "1", "--branch", "master"],
                               check=True, capture_output=True, text=True, timeout=180)
                output = run(root)
        else:
            output = run(args.lab_root.expanduser().resolve())
    except Exception as exc:
        output = {"schema": SCHEMA, "status": "BLOCKED",
                  "error_type": type(exc).__name__,
                  "note": "Local authentication/private checkout needs inspection; no Lab changes made."}
    print(json.dumps(output, sort_keys=True, indent=2, allow_nan=False))
    return 0 if output["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
