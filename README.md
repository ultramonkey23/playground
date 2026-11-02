# 🧪 Ultramonkeydog Playground

A disposable, conversation-first AI research workbench. **Public for technical accessibility, not public participation**. Temporary experiments are written to GitHub master and shown in a mobile review page.

**Open the [Playground Desk](https://ultramonkey23.github.io/playground/)** · [Browse active source](https://github.com/ultramonkey23/playground/tree/master/experiments) · [Review workflow](docs/REVIEW_WORKFLOW.md)

## Your normal workflow

**1. Talk naturally here.** Tell ChatGPT what to explore, build, investigate, test, compare or improve. No special command phrases or Termux required for ordinary work. In a connected session, the assistant reads current repository instructions and state, performs work with available tools, commits results and a structured review summary, and links your specific experiment in the Playground Desk.

**2. Inspect on the page.** Refresh results and tap an experiment. Review the actual claim, evidence and provenance, limitations, next tests and files. Read the source when you want to. Draft notes on your phone. GitHub remains the public data source; no private Lab content is fetched.

**3. Choose.** Keep the experiment, request improvements, propose a discard, or select specific files to send to the Lab. The page copies/shares a decision handoff for this ChatGPT conversation. **You must paste and submit it here**: a button does not transfer anything, post a note or authenticate owner approval. You may instead speak naturally here and ask to act on an experiment.

**4. ChatGPT executes your authorized decision.** Only Cody's explicit direct request can trigger extraction. The connected agent re-checks live master, your selected scope, the private Lab intake owner, and exact write/readback before retiring the experiment. Discard never writes to the Lab. GitHub issues and public text are advisory, not extraction approval.

## Where things live

- [experiments/](experiments/README.md): temporary source, evidence and files.
- Each current experiment has an optional review.json; newly created experiments should publish it per [the review contract](docs/REVIEW_WORKFLOW.md).
- [tools/review_manifest.py](tools/review_manifest.py): validates review records against local source files.
- [tools/playground_lifecycle.py](tools/playground_lifecycle.py): explicit status, preview, extract and discard CLI for authenticated Termux/other hosts. Normal ChatGPT conversation can use connected GitHub tools directly.
- [Mobile workflow](docs/MOBILE_OPERATIONS.md) and [extraction protocol](docs/EXTRACTION_PROTOCOL.md) document actual authority boundaries.

The Playground is **not** a private Lab mirror, persistent agent memory, always-on worker, or an automatic Lab control plane. A GitHub Pages site cannot secretly use your GitHub credentials. Local browser notes are not cross-device synced until submitted through an authenticated action.

## Proof boundaries

The founding evidence-integrity experiment has run successfully in user-provided Termux output; 20 Python tests passed on the user's device (2026-11-02). The live preview completed without mutation. The conversation-first review UI and manifest validator were added later; do not infer new tests or browser deployment from that earlier run. A live Cody-approved private Lab transfer remains untested until explicitly requested.

**Never upload secrets, unapproved private code, personal data, unpublished assets or internal host information.** Public Git history remains readable after deleting a file from current master.
