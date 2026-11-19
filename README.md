# Music Recommendation

> Status: M0 is docs and data only — no running app yet. The clickable app (one page, one text field, one result) arrives in M1.

Describe what you want to hear and get one album from a curated jazz and hip-hop catalogue. Each pick comes with a short reason and a listening link. Ask for another to explore the same mood.

This repository starts at **M0, the catalogue trial**. The [roadmap](docs/roadmap.md) takes it from a small sample to a public release on an existing Mikrus 2.1 with no additional running costs. The product comes first. The project also gives you a real system on which to practise acceptance testing, release checks, observability and recovery.

## Where M0 stands

The M0 sample holds 30 albums in `catalog/m0-sample.csv`, each with a recorded identity source and `proposed` mood tags: drafts pending evidence, not confirmed facts. A clean validator run means schema-clean only. The [catalogue trial](docs/catalogue-trial.md) maps 10 request types against the full sample with a boundary recommendation; result terms (`eligible`, `suitable`, `plausible`, fit 0–2) are defined in [product](docs/product.md#result-terms). `tools/validate_catalog.py` plus 57 pytest tests guard the CSV shape and vocabulary. The milestone is `Awaiting acceptance` in the [backlog](docs/backlog.md): the remaining step is the owner listening check and the catalogue boundary decision ([E01](docs/decisions.md)), then M1 builds the first form-to-result slice.

Product work lives on branch `deliver/m0`; `main` receives it via PR 2 after owner review.

## Start in this repository

Repository layout: `README.md`, `AGENTS.md`, `opencode.jsonc`, `.opencode/` (agents and the `/deliver` command), `docs/` (backlog, delivery, product, quality, architecture, decisions, operations, roadmap, catalogue-trial, harness-pilot), `catalog/` (starts in M0), `tools/` (CSV validator), `tests/` (validator tests), and `.gitignore`. `backend/` and `frontend/` arrive with M1.

## Contributor setup (agents)

This starter is already committed in this repository. Open a terminal in the repository root, where `AGENTS.md` and `.opencode/` are located.

```sh
opencode
```

Use [OpenCode V2](https://opencode.ai/docs/migrate-v1/). Connect your coding provider locally if needed and select the exact model you want with `/models`. The repository leaves the model choice to you. If you select [Muse Spark 1.3 Contributor](https://dev.meta.ai/docs/muse-spark), check the model available to your account and use it with materials you are comfortable sharing for training. This choice is independent of the app's runtime model.

Run **`/deliver`** to start the active milestone. The agent picks a ready item, makes and checks small changes, obtains the required review, and commits locally. Delivery stays inside the active milestone: the agent never marks a milestone Accepted and never starts the next milestone's items before the owner accepts the current one. When the milestone is ready, it hands you a build or a concrete review exercise. Use `/deliver M0` to name the active milestone explicitly. See [delivery](docs/delivery.md) for acceptance, resuming work and a pilot on a disposable branch.

## Your role

- As product owner, choose the scope, make tradeoffs and decide when a version is ready to share.
- As business analyst, turn observations into concrete examples. Describe the desired experience and what an unsuitable result looks like.
- As quality engineer, try the app on a phone and with a keyboard, explore musical fit and failure states, and review acceptance and release evidence. The agent writes and reviews the code and automated tests.

Example feedback: “The first pick matched my mood. When I asked for another, I wanted a different album with the same feel.” Add the desired outcome and ask the agent to update the criteria, tests and implementation as needed.

Project documentation, UI copy, agent prompts and acceptance examples use plain English. Read [product](docs/product.md) for the intended experience, [backlog](docs/backlog.md) for the current state, and [operations](docs/operations.md) before the first deployment.
