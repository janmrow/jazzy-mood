# Music Recommendation

Describe what you want to hear and get one album from a curated jazz and hip-hop catalogue. Each pick comes with a short reason and a listening link. Ask for another to explore the same mood.

This repository starts at **M0, the catalogue trial**. The [roadmap](docs/roadmap.md) takes it from a small sample to a public release on an existing Mikrus 2.1 with no additional running costs. The product comes first. The project also gives you a real system on which to practise acceptance testing, release checks, observability and recovery.

## Where M0 stands

The M0 sample holds 30 albums in `catalog/m0-sample.csv`, each with a recorded identity source and proposed mood tags awaiting the owner listening check. The [catalogue trial](docs/catalogue-trial.md) maps 10 request types against the full sample with a boundary recommendation. `tools/validate_catalog.py` plus 56 pytest tests guard the CSV shape and vocabulary. The milestone is `Awaiting acceptance` in the [backlog](docs/backlog.md): the remaining step is the owner listening check and the catalogue boundary decision (E01), then M1 builds the first form-to-result slice.
## Start in this repository

This starter is already committed in this repository. Open this repository in OpenCode at the repository root, where `AGENTS.md` and `.opencode/` are located.

Branch map: `main` is the shared base. Product work for the active milestone lives on `deliver/m0`. Harness and setup branches hold docs and workflow polish only and never carry product changes. Check `git branch -a` and the backlog header before starting.

Repository layout: `README.md`, `AGENTS.md`, `opencode.jsonc`, `.opencode/` (agents and the `/deliver` command), `docs/` (backlog, delivery, product, quality, architecture, decisions, operations, roadmap, harness-pilot, pull-requests), and `.gitignore`. `catalog/` starts in M0; `backend/` and `frontend/` arrive with M1. Their absence on this branch is expected. The M0 catalogue trial (`docs/catalogue-trial.md`) lives on the product branch `deliver/m0`.

### Day one

- Prerequisite: OpenCode with this repository open. `/deliver` is the project command defined in `.opencode/commands/deliver.md`. Type it in the OpenCode input, not in a plain shell. Use `/deliver M0` to name the milestone explicitly.
- Plain-git fallback: without OpenCode, read the backlog header, make a small branch, edit, run `git diff --cached --check`, and hand the diff to the owner. Do not expect the snapshot and review machinery to run outside OpenCode.
- First commands: `git branch -a`, `git log --oneline -8`, then read `docs/backlog.md`, `docs/product.md`, `docs/delivery.md`.
- Language: conversation with the owner in Polish; documentation, code, tests, UI copy, commit subjects and bodies, and handoffs in plain English.
- History note: `docs/harness-pilot.md` records a past workflow trial. Skip it on day one; it is not required to deliver M0.
- Snapshot note: `docs/delivery.md` asks for `git write-tree` twice to prove the index did not change mid-capture. The two IDs must match before saving `.delivery/<tree_id>.diff`.

### Checks

At M0 there is no check command yet. Required checks are `git diff --cached --check` plus the manual inspection list in the backlog item, recorded as evidence. M1-01 introduces one check entry point and CI; its command will be documented here.

Run **`/deliver`** to start the active milestone. The agent picks a ready item, makes and checks small changes, obtains the required review, and commits locally. When the milestone is ready, it hands you a build or a concrete review exercise. Use `/deliver M0` to name the active milestone explicitly. See [delivery](docs/delivery.md) for acceptance, resuming work and a pilot on a disposable branch.

## Your role

- As owner, decide scope and acceptance; as tester, try phone, keyboard, musical fit and failure states, then report observations.

Example feedback: “The first pick matched my mood. When I asked for another, I wanted a different album with the same feel.” Add the desired outcome and ask the agent to update the criteria, tests and implementation as needed.

Project documentation, UI copy, agent prompts and acceptance examples use plain English. Read [product](docs/product.md) for the intended experience, [backlog](docs/backlog.md) for the current state, and [operations](docs/operations.md) before the first deployment.
