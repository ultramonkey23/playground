# Community research — mobile agent capability patterns (2026-11-02)

This is implementation research from independent builders and public issues, **not** evidence that these projects are installed, safe, or supported in Cody's ChatGPT session.

## Adopt now

1. **Durable exchange beats transient chat:** WorkDone reports ChatGPT event/card delivery differences and mobile delivery limitations. We use GitHub issues, comments, and commits as inspectable handoff artifacts rather than pretending a paused chat is a daemon. Source: https://github.com/ivorpad/workdone
2. **Structured tools and fewer round-trips:** Phone Use reports mobile ChatGPT successfully exercising Android tools but shows that repeated model/tool calls dominate elapsed time even when native actions are fast. Favor a single explicit bounded task with independent readback and grouped GitHub changes. Source: https://github.com/anotb/phone-use
3. **Separate authority from tool reach:** Phone MCP publishes an OAuth/permission-scoped Android agent bridge with foreground, virtual-display, and file modes. Portable lesson: discover actual tools and record capability boundaries; do not assume a generic connection can act on all systems. Source: https://github.com/Mirochill/Phone-MCP
4. **Mobile submission needs redundancy:** GitHub community reports issue URL prefill data lost when the mobile app intercepts URLs. Provide clipboard/plain Markdown + manual issue creation, not only generated deep links. Source: https://github.com/orgs/community/discussions/113726
5. **Phone-only execution is real but distinct:** Android Termux developer reports show genuine local coding tools on phones. They are optional execution bodies, not a reason to replace this shared public GitHub interface. Sources: https://www.reddit.com/r/codex/comments/1x1djre/ and https://www.reddit.com/r/LocalLLM/comments/1rly87s/

## Research candidates (not implemented here)

- **Outbound on-device MCP:** DroidBridge explores polling a secure tunnel without inbound ports; not a substitute for an absent Lab connection. https://github.com/zephyr7030/DroidBridge
- **Agent wake/events:** WorkDone distinguishes Work events from normal chat cards and reports delivery limitations. Any persistent notifications require separate setup, consent, and real event/wakeup proof.
- **Hosted/static UI:** GitHub Pages could expose `site/index.html` as a mobile portal after enabling Pages in repository settings. Merely committing HTML does not publish a website.
- **GitHub mobile cloud coding agent:** a separate optional body if available/account-authorized; never presume that ordinary ChatGPT GitHub tools delegate to it.

## Engineering consequences

- Use **existing authenticated GitHub connection**, not an API key in a webpage.
- Use **public issue + code + evidence** as the durable unit.
- Use **append-only distinct files** where concurrent authors might collide.
- Keep independent **execution proof**, branch SHA and artifact readback.
- Make public-to-private transport a **candidate** for the existing Lab intake owner after real inspection; no automatic trust or canonical promotion.

## Source caution

External README claims are author reports and may be incomplete. The founding Playground proof is limited to operations actually performed with this session's GitHub and Python tools. No outside project was installed or granted permission.
