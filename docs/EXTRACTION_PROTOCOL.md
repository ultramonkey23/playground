# One-way Lab extraction and disposable experiment lifecycle

The Playground exists to **work, decide, and disappear**. Its public visibility is an access convenience for mobile ChatGPT, not an invitation to accumulate community submissions.

## States

```text
ACTIVE → EXTRACTED_AND_RETIRED  (only Cody explicitly authorizes extraction)
       → DISCARDED             (unworthy after scoped evidence or Cody rejection)
       → ACTIVE                (uncertain, still under investigation)
```

No permanent Playground result archive, no alternative Lab memory. Existing Git history supplies audit/rollback but is not a privacy deletion mechanism.

## ChatGPT mobile commands

**`playground preview <experiment-id> [selected files]` — read-only review**

Pin current `master`, inspect selected exact bytes and SHA-256 digests, and output the deterministic proposed Lab packet SHA-256 and destination. This does **not** write to the private Lab, delete files or grant approval.

**`playground extract <experiment-id> [selected files]`**

1. Check that the **current directly participating Cody** explicitly requested extraction and identifies the experiment and approved scope. A public issue or JSON label does not grant this permission.
2. Read live public Playground `master` HEAD and all selected experiment files. Check real execution evidence, attribution and privacy. Recover the current private Lab `research/vault/ingest/README.md` owner on `master`; do not blindly rely on this document.
3. Create one bounded Markdown research packet with topic, provenance and exact source SHA, relevant findings and selected source text/hashes, consumer, contradictions, proof ceiling and proposed next investigation. Nothing outside the user-approved selection goes into Lab.
4. Use **authenticated GitHub tools** to create one new `research/vault/ingest/playground_<id>_<source-sha-prefix>.md` on private Lab `master`. Do not touch Lab application code, agent contracts, registry, or canon.
5. **Read the Lab file back and compare its exact bytes/content.** If write/readback fails, do not retire the Playground experiment. If a previous partial attempt wrote the exact **same deterministic packet**, verify it and safely resume cleanup; if the destination content differs, refuse to overwrite and escalate for review.
6. Remove every active `experiments/<id>/` path on public Playground `master` in a non-forced commit only if its expected HEAD still matches. Verify the active tree no longer contains it. If remote changed, report partial, retain source, and reconcile.
7. Link the Lab packet and cleanup commits for the user, with accurate proof limits. A staged packet is not automatically adopted; Cody owns subsequent acceptance.

**`playground discard <experiment-id> <reason>`**

Inspect current evidence and objective; if definitively unworthy, duplicate, abandoned by Cody, or disproven within scope, delete its active directory from `master` and verify. Do **not** write a Lab packet. Unknown or unexecuted is not automatically unworthy. Record a concise reason in the Git commit; don't create a new permanent tombstone file.

## Standalone `gh` CLI

The repository has [`tools/playground_lifecycle.py`](../tools/playground_lifecycle.py), which can run where an appropriately permissioned `gh` CLI already exists. This is a separate CLI entrypoint; it is not the private Lab's `labctl`. It is **not** a background daemon and is **not** needed for ChatGPT's GitHub connector route.

Read active experiments (no writes): `python3 tools/playground_lifecycle.py status`.

Find current head: `gh api repos/ultramonkey23/playground/git/ref/heads/master --jq '.object.sha'`.

Before asking Cody to select anything, replace `extract` in the following command with `preview` and omit `--owner-approved` to obtain a **read-only** selection digest and exact proposed packet SHA-256.

To extract a specific approved selection, call:

```sh
python3 tools/playground_lifecycle.py extract 001_evidence_integrity \
  --expected-head "<exact GitHub master SHA>" --owner-approved \
  --select README.md --select demo.py \
  --question "Exact hypothesis being evaluated" \
  --author "Authenticated caller and model (as claim)" \
  --consumer "Lab research intake / actual proposed consumer" \
  --findings "Observed positive finding" \
  --limitations "Contradictions and unknowns" \
  --next-action "Independent validation or integration candidate" \
  --proof "Precise execution/proof ceiling"
```

**This command is an example, NOT an authorization to extract experiment 001.** The `--owner-approved` switch is a declaration by an authorized operator, not cryptographic authentication. Only actual caller identity and the source instruction supply authority.

To discard **an experiment judged unworthy**:

```sh
python3 tools/playground_lifecycle.py discard 001_evidence_integrity \
  --expected-head "<exact GitHub master SHA>" \
  --reason "Specific failed acceptance criterion or Cody rejection"
```

Again, this is a command illustration, not a decision to discard 001.

## Two crucial constraints

- **No reverse synchronization:** private Lab material is not automatically copied back to public Playground. A Lab readback verifies one specific selected write; it is not a request to expose other private data.
- **Git retention:** deleting an experiment from the active branch does not remove it from historical commits, forks, logs, search caches, or copies. Never stage secrets on public GitHub.

## What is actually tested

The code has isolated tests for explicit owner approval refusal, path traversal, content-hash provenance, exact Lab readback, readback failure retaining Playground files, exact-directory retirement and stale HEAD refusal. Live remote extraction into the Lab requires a **future explicit Cody selection** and an available authenticated GitHub writer; no such extraction has been initiated.
