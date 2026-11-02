# Mobile operations — speak naturally, inspect results, decide

## Default: ChatGPT is the interface

Use the connected ChatGPT conversation. Say something like:

> Experiment with this approach to my idea, try a real implementation and adversarial test, save the temporary work to the Playground, and show me the result page.

No command syntax, Termux or prebuilt mission form is required. The assistant must inspect live master and AGENTS.md before acting, check available GitHub/execute tools, do real work where possible, and publish a review.json with accurate evidence and limits. Then it gives Cody a link such as:

https://ultramonkey23.github.io/playground/?experiment=001_evidence_integrity

Results are not updated by a background worker. They change when an authorized connected agent or Termux writes GitHub master.

## Review on your phone

1. Open the [Playground Desk](https://ultramonkey23.github.io/playground/), which GitHub Pages hosts from master.
2. Tap Refresh results (it also attempts to load once on page opening); choose an experiment.
3. Read findings, actual evidence/provenance, limitations and next actions; open exact source if needed.
4. Type notes. These save **locally on that browser only**; no remote write happens yet.
5. Choose **Improve**, **Keep active**, **Request Lab transfer**, or **Discard**. For Lab transfer, explicitly check the exact files. The page copies a revision-pinned instruction; paste and **send it in this connected ChatGPT conversation**. A native share option is offered when supported.
6. The agent re-reads live current state, acts only with appropriate authority, then updates the review. If the source changed, reconcile with Cody. No private Lab data is retrieved by the page.

You can alternatively simply tell ChatGPT "I inspected experiment X, add my note ...", or "send X to Lab, but only the files Y and Z", without touching any page controls.

## GitHub notes

If you prefer notes directly on GitHub, the page links to the experiment's issue thread (if the review manifest supplies one) or opens a prefilled new issue as a fallback. GitHub sign-in and submission are still required. On some phones, prefilled fields may disappear; copy your note first. GitHub issue contents are public. Issue notes are **not extraction authorization**.

## Direct results publishing from Termux

If a real experiment must execute on Termux because the ChatGPT environment cannot execute a private Lab checkout, the normal finish should **not** require finding and uploading a local file. For the seven-probe Word Math organ fusion experiment, run the current `probe_fusions.py --clone-private --publish`. That uses your existing GitHub authentication to publish validated synthetic output into the public Playground and update the review card. To publish an already-completed `~/fusion-results.json`, use `publish_results.py` with no arguments.

The publishing command requires deliberate user invocation because this is a **public repository**, and a public Git commit persists. It validates bounded output and known probe records before upload; no private Lab source should be included. It does not write to the Lab or authorize extraction. ChatGPT can then inspect the latest public result directly after the user says to review it. Pasting output into ChatGPT also works.

## Constraints

The public GitHub Pages site has no backend writer, GitHub token, Lab tunnel, ability to start ChatGPT jobs, or background execution. Public GitHub REST rate limits may interrupt refresh; the page reports failures instead of inventing results. Private Lab staging still requires Cody's direct instruction in authenticated context and exact readback.

Optional power-user CLI: from a current authenticated clone, run python tools/playground_lifecycle.py status, preview, extract or discard as documented in [EXTRACTION_PROTOCOL.md](EXTRACTION_PROTOCOL.md). Termux is useful for local execution but is **not** a requirement for ordinary conversation-first research.
