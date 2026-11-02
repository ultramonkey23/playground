# 🧪 Ultramonkeydog Playground

**A disposable remote R&D workbench for Cody and tool-enabled AI assistants.**

The repository is **public for accessibility**, not because the Playground is primarily intended as a public community. Public visibility lets mobile ChatGPT and other clients read source without private-repository friction. GitHub authentication is still required to write. Everything stored here is publicly readable.

**Canonical work branch:** [master](https://github.com/ultramonkey23/playground/tree/master). The old repo name `Bone-bracket` and GitHub default branch `main` still need owner-side Settings changes. Until then, choose **master** explicitly.

## From ChatGPT mobile

Tell a GitHub-connected ChatGPT: **“Use the Playground on master. Read AGENTS.md and current source. Experiment on this idea, actually test it with your tools, commit the working artifacts, and read them back.”**

When an experiment is decided:

- **`playground extract <id>`** — only on **Cody's explicit command**, select the actual valuable evidence/files, stage a bounded research packet into the Lab's existing research intake, independently verify Lab readback, **then remove the source experiment from the active Playground**. It is one-way; no automatic Lab code or canon promotion.
- **`playground discard <id> <reason>`** — remove an unworthy experiment from active `master` with a real reason; do **not** write anything to the Lab.
- **`playground status`** — inspect the current active experiment folders and existing tool capability; do not infer from old notes.

These are **ChatGPT operational commands** requiring authorized GitHub tool actions under [the extraction protocol](docs/EXTRACTION_PROTOCOL.md). When a properly authenticated `gh` CLI is available, [the lifecycle script](tools/playground_lifecycle.py) also offers executable `status`, `preview`, `extract` and `discard` commands.

## Active work

- [experiments/](experiments/README.md): temporary experiments, notes, prototypes and tests; do not turn it into an ever-growing archive.
- [Mobile operations](docs/MOBILE_OPERATIONS.md): use ChatGPT/GitHub without a Lab network tunnel.
- [Pocket Desk](index.html): optional offline HTML mission composer; not deployed by default.
- [Research patterns](docs/COMMUNITY_RESEARCH.md): findings from independent developer experiments.
- [Proof and boundaries](docs/PROOF_AND_BOUNDARIES.md): what is and isn't verified.

## The lifecycle

```text
Idea → temporary experiment → real execution and evidence → evaluation
                                                       ↙        ↘
                                             CODY EXTRACTS    UNWORTHY
                                             selected value   / rejected
                                                  ↓               ↓
                                        Lab research intake     discard
                                        (verified readback)       ↓
                                                  ↓          remove from
                                        remove from active    active branch
                                        Playground
```

Nothing automatically enters the private Lab. Public Playground files and untrusted issue comments cannot confer your approval. The Lab's actual research, code, proof and integration owners are not replaced.

**Disappearance means removal from the current branch, not erasure of Git history or caches.** Do not ever put secrets, proprietary Lab source, internal addresses, unreleased assets, or sensitive data here expecting cleanup to make them private.

## Proof level

The founding GitHub-connected session has committed files to `master` and verified them by GitHub readback. A testable packet-integrity experiment is in [001](experiments/001_evidence_integrity/README.md). A public-to-private **unapproved** advisory test was retracted from the Lab's active branch when Cody clarified approval sovereignty; it remains in Git history. A Cody-approved extraction has **not** yet been executed.
