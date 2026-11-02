# Mobile-first operations

The Playground's principal job is to let a ChatGPT mobile session perform useful R&D **without an inbound Lab connection**.

## Three usable modes

### A — ChatGPT + connected GitHub tools (observed in founding session)

Ask: “Use my connected GitHub tools for `ultramonkey23/Bone-bracket`. Work on `master`. First read `AGENTS.md` and the relevant current files. Open an issue for this mission, execute the experiment with available sandbox tools, commit evidence files, read the files back, and link the issue/commit. Separate verified actions from claims that need Lab/runtime access.”

Do not ask a chat to *claim* it wrote to GitHub: request concrete tool-backed readback and a commit URL. If no authenticated GitHub write tool is present, switch to Mode B.

### B — GitHub app/web issue submission (no ChatGPT GitHub write permission required)

Open [new issue](https://github.com/ultramonkey23/Bone-bracket/issues/new/choose), choose NOTE / CHALLENGE / EXPERIMENT, paste proposal, then submit. [Mobile proposal composer](../site/index.html) can generate copyable Markdown in any local browser once the HTML is opened/downloaded.

**Community-observed caveat:** GitHub app deep links sometimes lose prefilled issue title/body parameters on Android or iOS. The clipboard + manual issue route is intentional, not a broken fallback. A GitHub account is still required to submit.

### C — Independent local/cloud execution

Use Python sandbox, browser, Termux, Codex, or another available tool *only if it is present for this session*. Keep examples self-contained. Publish exact command, inputs, exit code, and observed stdout. No direct Lab runtime is necessary to research an independent hypothesis.

## Mobile prompt patterns

- “**Research & test:** compare three existing GitHub implementations of [problem], cite primary code, choose a falsifiable hypothesis, implement a small executable benchmark in Playground on master, run it, report evidence.”
- “**Second opinion:** pick the newest Playground challenge, independently reproduce and attack its strongest claim. Comment with exact counterexample, not a summary.”
- “**Handoff:** inspect issue #[N], collect current files and execution evidence, state executed/unexecuted work, then add one sourced comment without changing its authority.”
- “**Prototype:** create a standalone offline HTML/JS or Python prototype in Playground, test it with real input, commit and read back. Do not require the private Lab.”

## Capability discovery

At the start of every task, record: available GitHub tools, ability to execute code, ability to access URLs, current branch, and any enabled background/scheduler/host capabilities. Do **not** infer feature presence from a ChatGPT product announcement or old thread.

## Current limitations

This session can GitHub-write and can run local Python, but has not shown a direct private Lab tunnel, live Lab host, or repository-admin rename/default-branch settings API. ChatGPT background wakeups and push notifications must be verified independently before advertised.

For observability, use GitHub issue comments and commits instead of volatile chat-only completion reports. Compare public material with the real target branch before every consequential action.
