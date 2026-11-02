# Mobile operations — workbench, not public showcase

The Android/iOS ChatGPT app can act as the control surface **only when a session actually has the relevant tools**. No direct Lab tunnel is assumed. GitHub public reading reduces access friction; GitHub writing remains permissioned.

## The normal loop

Tell ChatGPT: **“Playground experiment: <your full objective>. Inspect `ultramonkey23/Bone-bracket` on `master` and read AGENTS.md first. Use real tools to research/test, commit results, independently verify readback, and keep the experiment temporary.”**

A new session can resume from the active `experiments/` directories, exact commits and actual experiment files, without depending on old chat memory. Ask `playground status` to inspect current reality; the standalone authenticated CLI also now implements `status` directly.

Before transferring any candidate, ask `playground preview <id>` for the proposed selected file hashes and a deterministic, read-only staging packet. No Lab write occurs during preview. After reviewing useful work, Cody can say **`playground extract <id>`** and optionally select exact paths. This is the **only** signal that authorizes transfer to private Lab research intake. Unworthy work gets **`playground discard <id> <reason>`** or an evidence-backed negative disposition.

## Ways to interact

- **ChatGPT with installed/connected GitHub tools:** direct authenticated commits, issues/comments and readback. It can execute local/sandbox code only if those tools are presently available.
- **GitHub browser/app:** create a quick note in an issue, then have an agent convert it into a temporary experiment. GitHub mobile issue-prefill links have known reliability issues; copying text and pasting into a plain issue remains viable.
- **Pocket Desk:** [index.html](../index.html) is a self-contained form for composing a task and copying it. It has no write credentials or background worker. Its on-demand status button reads the public GitHub master tree without writing anything; when offline, it reports an unavailable snapshot rather than inventing status. GitHub Pages must be enabled separately, and the current default branch setting may be different from the active `master`.

## The real boundaries

A GitHub commit is a file write, not a remote terminal command on the Lab. GitHub Issues and notes are not execution permissions. A private Lab research packet can be written via a connected GitHub tool **only after Cody orders extraction**; the Lab's own runtime proof, decision owners and current canon are independent.

Avoid publishing private code, secrets, internal addresses, assets, personal data or confidential screenshots. Git history and caches make later cleanup incomplete.

A retry of a partially completed extraction is designed to recognize an **identical** already-staged packet and finish cleanup, while refusing a different packet at the same destination. [Full one-way extraction procedure](EXTRACTION_PROTOCOL.md).
