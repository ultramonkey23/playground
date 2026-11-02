> **Original-task scope correction (2026-11-02):** This is an analysis of seven *baseline and exploratory synthetic probes*, **not a completed Word Math × Connected Systems multi-organ fusion campaign**. No factorial attachment of both capabilities into several other Lab organs has been executed. The earlier repair-focused recommendations misrepresented the owner's mission. See [SCOPE_REASSESSMENT.md](SCOPE_REASSESSMENT.md) before interpreting any upgrade claim.

# Corrected fusion-run analysis — November 2, 2026

## Source and evidence ceiling

- **Published public Playground:** `latest_results.json` on `master` at commit `183a54fc987f00cf8cb8ef07c0e236073e829d7e`, produced by the explicit public publisher at 20:58:25 UTC.
- **Lab source revision in output:** `a08c9619ba606e972dbcfb99f898cc3a5c69bfed` on `master`. Connected GitHub inspection confirmed this was the private Lab's current `master` while this analysis was performed. The specific underlying organ source files were inspected live and their blobs matched the current tree.
- **Execution:** seven of seven probe records have `state=OBSERVED`; overall `status=OBSERVED`. That means seven Python probe functions returned observations from an authenticated user-hosted run. These are *not* seven independent end-to-end integration successes. The public GitHub commit authenticates publication, not the private Termux process or unseen local runtime.
- **Mutations:** the run reported `explicit_lab_write_operations=0` and `private_source_in_output=false`. No private Lab modification or live consumer adoption was demonstrated. Lab local state beyond the reported clean temporary checkout remains UNKNOWN.

## Corrective source audit — important, supersedes the upgrade recommendation

**This report originally proposed “health-aware repair prioritization” and a quarantine/repair dual-channel integration as though the Lab did not already own comparable capabilities. That conclusion was not grounded in the relevant whole Lab. Withdraw the recommendation.** The source-level recovery below identifies existing owners and actual consumer seams; it is a **targeted** audit, not full live runtime attestation.

Source read on private Lab `master` at `a08c9619ba606e972dbcfb99f898cc3a5c69bfed`:

| Existing owner | Verified behavior and source location | Execution ceiling |
| --- | --- | --- |
| `labcore/morphogenesis_grid.py` | `bioelectric_edge_modulation` quarantines critically low-voltage edges at multiplier 0.05, boosts flux through moderately damaged tissue, and leaves healthy edges at baseline. `step` also maintains local repair alarms and restorative dynamics. | Implemented function and existing unit tests; actual use requires a caller. |
| `labcore/physarum_router.py` | `physarum_step(..., bioelectric_grid=None)` **already multiplies edge flow by the Grid's bioelectric modulation** when a grid is supplied. This is the existing Grid→Physarum fusion hook I missed. | The inspected default `run_physarum_convergence` loop calls `physarum_step` **without** the optional grid, and code search found no other passing callsite. This establishes the *inspected call path's* behavior, not what inaccessible active agents execute. |
| `labcore/mycelial_routing.py` | Existing selection path consumes Physarum convergence and combines mastery, outcome reliability, route-health memory and failure/integrity penalties. | Source-consumer evidence; no independent currently-running executor trace. |
| `labcore/runtime_watchdog.py` → `labcore/metabolic_reflex.py` → `labcore/immune_repair.py` | Existing nervous→immune chain triages watchdog abnormalities, gates repairability and authority, dispatches bounded repair, validates outcomes, and records repair evidence. The watchdog loop has an explicit `auto_reflex` flag. | Actual function-call path exists, but `auto_reflex=False` is its declared default; which running processes enable it remains UNKNOWN. |
| `labcore/path_feedback_loop.py` | Existing `deposit_outcome_feedback` and `read_route_health` preserve proof-backed success, danger and congestion evidence for route-family and route-specific adaptation. | A real evidence-consumer and persistence path exists; no claim of specific local runtime activity. |
| `labcore/mycelial_pattern_fusion.py` | The Neurodaemon self-check explicitly asserts `neurodaemon_semantics_do_not_change_spawn_equation_yet` and says semantic testimony remains **observational until runtime calibration earns control influence**. Spawn scoring already uses measured bridge need and inverse daemon density. | Intentional contract, not an accidentally unwired semantic signal. |

**Reinterpretation of the published seven-probe run:** The `voltage → invented bridge resistance → Neurodaemon score` adapter is an isolated **alternative experimental mapping**, not discovery of an absent repair-prioritization capability. The recorded voltage, assignment and target-diversity effects remain valid within that synthetic setup. They do **not** prove production advancement, absence of comparable Lab machinery, or a missing bridge that should be added. Prior comparison of this adapter to an empty baseline omitted the Lab's existing Grid→Physarum and watchdog→immune owners; therefore it is **not** an upgrade comparison against the real architecture.

Do not replace, connect around, or tune these owners based on this Playground exercise. Before drawing any new integration conclusions, independently inspect the current live callsites, runtime inputs and downstream consumers (including active agent work inaccessible over GitHub), and compare against the **existing** integrated pathways. No change to Lab contracts is warranted from this result.

## Measured outcomes

| Experiment | Measured fact | Meaning and proof ceiling |
| --- | --- | --- |
| Word Math → Mycelial | Proof and repair changed several daemon `semantic_affinity` values, but 0 of 5 placements and 0 rounded spawn scores changed for those inputs. | Existing semantic connection changes advisory metadata; its raw testimony does **not** enter the current `_calculate_neurodaemon_swarm` scoring formula under these fixtures. |
| Four Mind capability matching | **Three distinct non-null winners** in five tasks: repair→repair specialist (resonance 0.8), recognized proof→proof specialist (0.6), recognized assimilation→assimilation control (3.5). `verify` and `fuse` still yielded null. | The prior reported “two winners” was counting null. The existing overlap engine works for matched semantic dimensions; no proof of complete natural-language coverage or actual executor selection. |
| Scribe → Word Math → Zero Point | 4/4 test cases preserved the semantic vector and scoped summary, all `scribe_may_execute=false`. The conditional request was held pending evidence. Questions/prohibitions had zero executable events despite a `SAFE_TO_PROCEED` state. | Scoped language behavior survived the observed handoffs; no command execution authority was granted. |
| Typed sockets | Four declared consumers of the semantic-vector socket, eleven targeted source importers. Read-only observer compatible; simulated ACTIVE_WRITE/PROVEN consumer rejected with authority and proof-ceiling blockers; handoff compilable. | Socket registry ≠ complete call graph. Existing safety boundary held in this isolated probe. |
| Connected Systems First | The same simple task changed **STANDARD/4 required checks** on a leaf to **DEEP/6 checks** with cross-organ structural context. Its routing-policy text remained unchanged; the cross-organ case added state-integrity and dependent-regression checks. Broad tasks were DEEP already, with 6→8 checks as radius expanded. | Structural validation adapts even when Routing posture does not. Whether a later executor consumes the escalation is not established by this side-by-side observation. |
| Word Math → Morphogenesis → experimental Mycelial adapter | Corrected recognized hazard produced −1.0 signal and voltage 0.233981; proof produced +0.34 and voltage 0.877620; neutral and unmatched hazard produced +0.04 and voltage 0.736223. | Word Math's existing bioelectric polarity works on recognized inputs. The voltage→resistance→daemon edge is **temporary synthetic adapter code**, not an existing Lab connection. |

## Cross-organ adapter: actual gain sweep

One bridge was given an **experimentally invented** resistance input:

`bridge_resistance = max(0.1, 1 + gain * (0.7 - simulated_voltage))`.

No tuning coefficients have been outcome-calibrated. The run tested gain 0, 0.5, 1.0, 2.0; all other bridge resistance baselines and the sequential daemon density mechanism remained as specified by the harness.

| Signal condition | Gain 0 baseline: fifth daemon | Gain 1: fifth daemon | Gain 1: fifth score | Gain 1: distinct targets |
| --- | --- | --- | ---: | ---: |
| Neutral (+0.04) | four_mind_to_pattern_fusion | pattern_fusion_to_burst | 1.35 → 1.35 | 5 → 4 |
| Recognized proof (+0.34) | four_mind_to_pattern_fusion | pattern_fusion_to_burst | 1.35 → 1.35 | 5 → 4 |
| Recognized destructive/risk (−1.00) | four_mind_to_pattern_fusion | four_mind_to_pattern_fusion | 1.35 → 1.98 | 5 → 5 |
| Unmatched danger wording (+0.04) | four_mind_to_pattern_fusion | pattern_fusion_to_burst | 1.35 → 1.35 | 5 → 4 |

For recognized hazard, the fifth daemon's rounded spawn score increases with gain: **1.35 at 0; 1.66 at 0.5; 1.98 at 1; 2.61 at 2**, without moving its target. At gains above zero, recognized proof and neutral move the fifth daemon to an already occupied bridge, leaving only four unique targets (the target-count metric decreases). Those target moves are observations; no objective utility improvement is proven. The 1.35→1.35 constancy for proof with a changed target also makes raw candidate score margins and deterministic tie-break order worth instrumenting before drawing a stronger conclusion.

## Existing native physiology junction — source verified (earlier inference withdrawn)

The actual `MorphogenesisParameters.v_critical` is **0.25**. The corrected hazard's simulated node voltage is **0.233981**, below that critical threshold. The existing `bioelectric_edge_modulation` code returns **0.05** for an edge whose minimum endpoint voltage is at or below 0.25. That quarantine function **was not called by this fusion experiment**; 0.05 is a source-derived *predicted output*, not another observed case.

The earlier analysis **incorrectly presented this as a new dual-channel fusion opportunity without recovering existing consumers**. The native Grid→Physarum edge-modulation hook and watchdog→immune repair chain already exist (see corrective audit above). The artificial adapter changed a Neurodaemon *advisory* score, not native repair assignment, and it has not been compared to those actual mechanisms. Whether the optional Physarum grid hook is activated in specific current runtimes, and how repair execution responds to it, remain UNKNOWN.

## Additional quirks

- **Neutral is not zero.** Word Math's registered pressure floors are proof 0.2 and danger 0.1. Current bioelectric formula yields `0.5×0.2 − 0.6×0.1 = +0.04`. That is a real neutral baseline in the current math, not validated evidence of actual health improvement. Whether the baseline is intended remains UNKNOWN.
- **Semantic coverage versus ranking power.** `verify` and `fuse` had zero above-neutral dimensions in the specific tested phrases, while recognized proof, repair and assimilation terms matched profiles. That supports a lexical/corpus coverage question, *not* a conclusion that Four Mind's matching engine is broken or needs a replacement.
- **Two planning views, one task.** Validation's structural context was sufficient to raise the tier and add checks; Routing's integration policy remained based on the task text. This may be intentional separation of roles. The decisive next question is whether the downstream executor reads and obeys the validation plan, not whether two fields carry identical strings.

## Revised evidence ceiling

- The published seven-probe measurements demonstrate synthetic differences in existing semantic and scoring functions. They do not establish an absent repair capability or a beneficial new fusion.
- Native Grid→Physarum coupling, adaptive Mycelial routing, watchdog/metabolic-reflex/immune-repair and outcome feedback **already exist** in current source. Do not treat them as new implementation requirements.
- Specific activation of the optional bioelectric Grid argument in real Physarum convergence, watchdog auto-reflex configuration, agent activity and downstream repair outcomes remain **UNKNOWN** without live execution evidence.
- The Neurodaemon semantic-affinity/score separation is intentional in its own current self-check. Do not presume it should drive placement.
- No Lab mutations, new adapters or new agent contracts are justified by the measured experiment.

**Corrected assessment:** The public publish/review workflow works. The experiment is valid as a bounded synthetic study but did **not** discover a need for “health-aware repair prioritization.” The earlier upgrade suggestion is withdrawn.
