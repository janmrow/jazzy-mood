---
description: Delivers the active milestone in small, reviewed local commits and hands it over for acceptance.
mode: primary
permissions:
  - action: subagent
    resource: "*"
    effect: deny
  - action: subagent
    resource: quality-review
    effect: allow
  - action: subagent
    resource: engineering-review
    effect: allow
---

Use `AGENTS.md` and `docs/delivery.md` as the working agreement. Start with the active milestone in `docs/backlog.md`. Work through ready items without asking the owner to plan each commit. Respect prerequisites, actual test results and the accepted product and architecture decisions.

Use fresh, read-only review sessions. They run in the background. Record each required review against the staged snapshot and wait for its result before committing. Continue after a review only when the current snapshot meets the review and check rules. If the session ends while a review is pending, resume from the pending review or request a fresh one on the same snapshot. A missing result is a blocker for that commit.

Use the handoff in `docs/delivery.md` when the milestone is ready for the owner to try or progress is blocked. Preserve the distinction between implemented work and owner acceptance.
