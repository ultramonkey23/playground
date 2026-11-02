# Review workflow: conversation-first Playground

The GitHub Pages Pocket Desk is a public **read-only review UI**, not a Lab control plane. ChatGPT with the connected GitHub plugin is the ordinary writer and experiment executor; the user gives goals naturally in this chat. No public site has private Lab credentials, an agent daemon or automatic extraction permission.

## Active experiment contract

New experiments should include experiments/SAFE_ID/review.json next to their real work and evidence. Fields:
- schema = umd.playground.review.v1
- id = the safe experiment folder name.
- title, question, summary = nonempty review prose.
- status = ACTIVE, REVIEW_READY, or BLOCKED. REVIEW_READY means reviewable, not approved.
- evidence = array of objects with nonempty kind, environment, observation, source. Mark user-reported, simulated and unexecuted evidence explicitly.
- limitations, next_actions = arrays of strings.
- recommended_action = REVIEW, KEEP, IMPROVE, EXTRACT, DISCARD; advice is not authorization.
- recommendation_reason = rationale.
- files = explicit array of path/label objects for candidate selection. Paths must stay within the experiment directory.
- issue_number = optional positive integer linking an authenticated GitHub issue discussion.

A missing review.json means an older experiment has not published a review summary. The page must not invent findings.

## Operating loop

1. Cody describes an objective naturally here. The connected assistant inspects current AGENTS.md, master, active work, available tools, and relevant evidence.
2. The assistant runs actual work when available and creates/updates temporary experiment sources and review.json. Preserve the complete goal, distinguish observed, reported, inferred, unknown and unexecuted. No private information goes into public GitHub.
3. The assistant validates review.json with python tools/review_manifest.py, executes relevant tests where possible, and commits/readbacks current master without force.
4. The assistant links the page with ?experiment=SAFE_ID, so Cody can inspect summaries, evidence, selected sources and limitations without using Termux.
5. Cody writes a note, asks for more investigation, keeps the experiment, discards it, or elects to send selected research to the Lab. The page copies or shares an exact revision-pinned decision message for Cody to submit back into this connected conversation. A click alone does NOT write to GitHub or to the Lab.
6. The assistant verifies the new direct instruction and live repository state. On an authorized Lab extraction it independently inspects the current private Lab intake owner, writes only selected research there, verifies exact readback, then retires the public experiment. Lab intake is not Lab adoption.
7. Discard removes active files with a justified user decision and no Lab write. Unknown is not an automatic failure.

## Notes and limitations

Browser notes are local drafts until Cody submits them to ChatGPT or an authenticated GitHub issue. Storage is not shared across devices and may be erased with browser data. The page never embeds credentials or silently uploads private notes. Submitting a note to a public Playground experiment makes it public.

The page queries public GitHub REST data only on refresh. Unauthenticated rate limits and network failures can prevent updates; those are displayed, not filled with stale or imaginary proof. It never automatically changes the private Lab.

Public GitHub history remains readable after deleting current-branch experiment files. Do not put private Lab source, secrets, internal addresses or unreleased work here.
