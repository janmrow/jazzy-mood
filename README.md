# Music Recommendation

> Status: M1-01 delivers the first form-to-result slice on a tiny fixture. The full catalogue arrives in M2.

Describe what you want to hear and get one demo album from a tiny fixture, with a short reason and a search link. The curated catalogue and repeat picks arrive in M2.

This repository starts at **M0, the catalogue trial**. The [roadmap](docs/roadmap.md) takes it from a small sample to a public release on an existing Mikrus 2.1 with no additional running costs. The product comes first. The project also gives you a real system on which to practise acceptance testing, release checks, observability and recovery.

## Where M0 stands

The M0 sample holds 30 albums in `catalog/m0-sample.csv`, each with a recorded identity source and `proposed` mood tags: drafts pending evidence, not confirmed facts. A clean validator run means schema-clean only. The [catalogue trial](docs/catalogue-trial.md) maps 10 request types against the full sample with a boundary recommendation; result terms (`eligible`, `suitable`, `plausible`, fit 0–2) are defined in [product](docs/product.md#result-terms). `tools/validate_catalog.py` plus 60 pytest tests guard the CSV shape and vocabulary. M0 is accepted in the [backlog](docs/backlog.md) with listening deferred to M2-01; M1 builds the first form-to-result slice.

Product work lives on branch `deliver/m1`; `main` receives it after owner review.

## Run the first slice (M1-01)

The page and the API share one origin. The API returns one fixture album
with local selection only; no decision provider is contacted.

```sh
pip install -r backend/requirements-test.txt
python3 -m uvicorn backend.app.main:app --port 8000
```

In another terminal, for frontend development with live reload:

```sh
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`. For the single-origin build served by the API:

```sh
cd frontend && npm install && npm run build
python3 -m uvicorn backend.app.main:app --port 8000
```

Open `http://localhost:8000`, submit `Late-night jazz with a steady beat
and no vocals.`, and expect one fixture card with a search listening link.
Blank input shows a clear message. If the request fails, the description
stays in place with a retry button.

## Checks

One command runs pytest, frontend type checking, the production build and
the browser journey against the single-origin backend:

```sh
./scripts/check.sh
```

CI runs the same command on push and pull request (see
`.github/workflows/ci.yml`). Routine checks use fixture data and a disabled
provider.

## Start in this repository

Repository layout: `README.md`, `AGENTS.md`, `opencode.jsonc`, `.opencode/` (agents and the `/deliver` command), `docs/` (backlog, delivery, product, quality, architecture, decisions, operations, roadmap, catalogue-trial, harness-pilot, pull-requests), `catalog/` (M0 sample), `backend/` (FastAPI slice with a synthetic fixture), `frontend/` (React page and Playwright journey), `tools/` (CSV validator), `tests/` (validator tests), `backend/tests/` (API checks), `scripts/check.sh` (project check), `.github/workflows/ci.yml`, and `.gitignore`.

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
