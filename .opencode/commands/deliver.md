---
description: Deliver ready work in the active milestone and hand it over for acceptance.
agent: delivery
subagent: false
---

Run the workflow in `docs/delivery.md`. Read `AGENTS.md` and find the active milestone in `docs/backlog.md`.

Optional milestone argument: $ARGUMENTS

An empty argument selects the active milestone. A supplied argument must be a single milestone ID such as `M0`. Check it against the active milestone and its prerequisites. If it names a different milestone, continue only when the owner has explicitly accepted the current milestone and authorized the named one. Record that transition in the backlog. Keep implementation, review and local commits inside the resulting milestone.
