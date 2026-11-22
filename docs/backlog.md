# Backlog

- **Active milestone** M1
- **Milestone state** Open (M0 accepted by owner on 2026-11-19; listening sampling deferred beyond M0 to M2-01 import batches under D08; E01 boundary taken as trial recommendation unless revised)
- **Accepted milestones** M0
- **Product branches** `deliver/m0` holds the M0 sample and trial; `deliver/m1` holds the M1 slice. Harness and setup branches hold workflow and docs polish only and never carry product changes.

The delivery agent may choose and split items inside the active milestone. An item is ready once its dependencies are implemented, any named prerequisite decision is recorded and the work has enough evidence to begin. The owner sets the next milestone at acceptance. See [delivery](delivery.md) for state transitions and [product](product.md) for the `P01`–`P08` criteria.

Use `Open`, `Implemented` or `Blocked` on work items. Milestone states (`In delivery`, `Awaiting acceptance`, `Accepted`) live with the Active milestone line above and are never interchangeable with item states. Add one short note for a material result or a blocker. When splitting an item, use child IDs such as `M1-01a`, keep the parent outcome, and mark the parent implemented only when its acceptance evidence is complete. Use the item ID in the commit subject so progress can be found in Git.

## M0 · Prove the catalogue

### M0-01 · Prepare a sourced catalogue sample

- **State** Implemented
- **Depends on** None
- **Criteria** P02, P04
- **Result** 30-row validated sample (13 instrumental, 15 vocal, 2 unknown); `tools/validate_catalog.py` reports OK 30 rows with 30 proposed rows pending the listening check; pytest 60 passed. A clean run means schema-clean only, not musically confirmed.

Create `catalog/m0-sample.csv` with about 30 candidate albums across the proposed music styles. Record a stable candidate ID, artist, title, year when verified, identity source and relevant reuse notes. Add a small vocabulary to describe energy, mood, groove and vocals where evidence supports it. Record the basis for those attributes and allow unknown values. Use a documented convention for multiple tags so later import work is straightforward.

The owner can sort or inspect the sample, open representative identity sources and distinguish facts from proposed labels. Check for duplicate albums, missing identity sources and unclear reuse before committing. Flag incomplete candidates and keep them separate from any eligible release data. If permissions or evidence limit the sample, report the actual count and gaps.

### M0-02 · Try the sample against realistic requests

- **State** Implemented
- **Depends on** M0-01
- **Criteria** P02, P03, P04
- **Result** Trial covers M0-001 to M0-030 with 10 cases (vague, strict instrumental, two alternative sets, three gaps, mood contrast, unknown handling, soft preference) plus the catalogue boundary recommendation; all picks fit 1 proposed. M0 rows stay `proposed`; the upgrade to `sourced` lands with the M2-01 import under D08.

Create `docs/catalogue-trial.md` with 8–12 practical English descriptions and examples of suitable candidates from the sample. Include at least one vague request, one strict instrumental constraint, one request with good alternatives and one gap or mismatch. Show why the available data supports each highlighted example. Mark uncertain interpretations for the owner's listening check.

Present a short recommendation on catalogue boundaries, whether albums are worth keeping, and which data needs improvement before widening the import. The owner can try several listening links and accept the direction. This item can be completed with local findings before any live inference or paid account is used.

## M1 · Deliver the first link

### M1-01 · Build and check a complete form-to-result flow

- **State** Implemented
- **Depends on** Accepted M0
- **Criteria** P01, P02, P05, P07
- **Result** Single-origin form-to-result slice on a 3-row synthetic fixture (FIX-001 to FIX-003, clearly marked fixture, local selection only). FastAPI validates trimmed 1–500 characters with bounded recent_ids and exposes cheap `/healthz`; React page shows result, loading and recoverable error with focus and keyboard support. `./scripts/check.sh` runs pytest (71 passed: 60 catalogue + 11 API), `tsc --noEmit`, production build and Playwright (10 passed: 5 chromium + 5 mobile covering valid, blank, failure-retry, loading guard and keyboard focus).

Implement one English form calling the API, which returns an album from a tiny local fixture. Display the result, loading and a recoverable failure. Keep useful focus and keyboard behaviour. Include a cheap health endpoint at `/healthz`. Add the project check command and CI to this first app slice. Use pytest for request validation and the successful response, and a Playwright test from form submission to displayed card. Both reviewers check this first complete product slice.

The owner can start it locally with documented commands, get a result, and verify that a blank submission or a simulated failure gives clear feedback. The playtest may use controlled test data. Mark the fixture clearly when demonstrating it.

### M1-01a · Validation feedback and request reference

- **State** Implemented
- **Depends on** M1-01
- **Criteria** P01, P05, P07
- **Result** Textarea caps at 500 with a live code-point count matching server length; blank or rejected input shows an inline message and returns focus to the field. Failed requests keep the retry card and show the `X-Request-ID` reference when the server answered. Middleware logs failed requests instead of dropping them. `./scripts/check.sh` green: pytest 71 passed, typecheck and build pass, Playwright 14 passed (7 chromium + 7 mobile).

### M1-01b · Log hygiene on valid and rejected input

- **State** Implemented
- **Depends on** M1-01a
- **Criteria** P08
- **Result** `check.sh` runs uvicorn with `--no-access-log` so the default access format (full request line with query string) cannot leak visitor text outside the audited app logger. New pytest covers the 422 paths (blank, oversized) with a unique phrase and asserts both carry `X-Request-ID`. `./scripts/check.sh` green: pytest 72 passed, Playwright 14 passed.

### M1-01c · Deterministic single-flight submit

- **State** Implemented
- **Depends on** M1-01b
- **Criteria** P05
- **Result** Synchronous `submittingRef` guard blocks a second submit in the same task (state reads stale until re-render). New e2e dispatches two clicks in one task against a counting route: it fails with 2 calls without the guard and passes with 1. `./scripts/check.sh` green: pytest 72 passed, Playwright 16 passed (8 chromium + 8 mobile).

### M1-01d · Harden the check harness against stale servers

- **State** Implemented
- **Depends on** M1-01c
- **Criteria** workflow rule (check reliability)
- **Result** `check.sh` refuses a port that already answers `/healthz`, verifies the ready server is its own (process alive plus `Uvicorn running` on that port in its log, with a short retry), uses a unique `mktemp` log shown only on failure, and fails fast when the backend dies. Probe: with a dummy `/healthz` occupant on the port, the script passes pytest/typecheck/build then aborts before any browser run with the port message. `./scripts/check.sh` green.

### M1-01e · Explicit 404 for unknown API paths

- **State** Implemented
- **Depends on** M1-01d
- **Criteria** operations (health and logs)
- **Result** `GET/HEAD/POST/PUT/PATCH/DELETE/OPTIONS /api` and `/api/{path}` return JSON 404 (`{"detail": "Not Found"}`) instead of the mounted `index.html`, so typo'd API paths cannot mask as a healthy page. The fallback sits after all specific API routes and before the static mount. `check.sh` builds the frontend before pytest so the API tests run against the mounted single-origin app; probes: fallback removed fails with and without `dist`, closing the clean-checkout hole. `./scripts/check.sh` green: pytest 73 passed, Playwright 16 passed.

### M1-01f · Split runtime and test requirements

- **State** Implemented
- **Depends on** M1-01e
- **Criteria** D02
- **Result** `backend/requirements.txt` holds only fastapi and uvicorn (verified: no httpx/pytest import in `backend/app/`); new `backend/requirements-test.txt` adds pytest and httpx for the TestClient. CI and README install the test file only (runtime pulled via `-r`); the future M1-02 image takes runtime only. `./scripts/check.sh` green: pytest 73 passed, Playwright 16 passed.

### M1-01g · Type the fixture and return copies

- **State** Implemented
- **Depends on** M1-01f
- **Criteria** D02, D05
- **Result** `FixtureAlbum` TypedDict mirrors the API `Album` keys with a parity test; `select_album` returns a copy so a caller mutation cannot pollute later picks (covered by a mutation test). `./scripts/check.sh` green: pytest 75 passed, Playwright 16 passed.

### M1-01h · Honest demo copy

- **State** Implemented
- **Depends on** M1-01g
- **Criteria** P02
- **Result** Listening links say where they go (`Search YouTube for listening options`); reasons use plain words (`demo entry, not a catalogue recommendation`) instead of team jargon; README promises the demo, not the catalogue. `./scripts/check.sh` green: pytest 75 passed, Playwright 16 passed.

### M1-01i · Remove listening and search links from the demo

- **State** Implemented
- **Depends on** M1-01h
- **Criteria** P02
- **Result** Owner decision 2026-11-22: no listening or search proposal in the M1 demo. `FixtureAlbum` and API `Album` drop `listening_url` and `listening_label`; React card shows artist, title and reason only with zero links (year already dropped in M1-01j); pytest asserts both keys absent and e2e asserts zero links (valid, double-submit mock and keyboard paths updated). Listening links and verified years return with the catalogue in M2-03/M2-01.

### M1-01j · Drop synthetic years from the demo

- **State** Implemented
- **Depends on** M1-01i
- **Criteria** P02
- **Result** `FixtureAlbum` drops `year`; API returns `year: null` so the card shows no `Released` line for fixture picks. Verified years return with the catalogue in M2-01. Frontend year guard uses `!= null` for missing values.

### M1-01k · Match the counter to the server limit

- **State** Implemented
- **Depends on** M1-01j
- **Criteria** P01
- **Result** Counter shows trimmed code-point length; `maxlength` removed so emoji and padded input follow the same 1–500 rule the server enforces. E2e asserts no `maxlength` cap and trimmed counts (`15 / 500`, padded 500).

### M1-01l · Focus retry after a failed request

- **State** Implemented
- **Depends on** M1-01k
- **Criteria** P07
- **Result** Request errors move keyboard focus to `Try again` instead of the error heading; validation errors still return to the field. E2e asserts retry is focused after an aborted request. Also fixes the M1-01k result typo (`15 / 500`).

### M1-01m · Say the demo is single and fixed

- **State** Implemented
- **Depends on** M1-01l
- **Criteria** P02, P03
- **Result** Fixture reasons state the demo ignores the description and always shows the same entry; page banner and card note say resubmits repeat and variety arrives in M2. Pytest asserts the ignores-phrase; e2e asserts the banner and card notes with zero links.

### M1-01n · Redesign the demo screen (Ribbon, dawn)

- **State** Implemented
- **Depends on** M1-01m
- **Criteria** P05, P07
- **Result** Hallmark full redesign at app scope (scope: app screen, no hero): Ribbon dawn tokens plus shared scale and base rules; console panel with live mono counter; record card with hairline rules; three-channel disabled states; retry keeps focus; gate-19 dash fixes in both request references. `./scripts/check.sh` green with zero test edits.

### M1-01o · Harden control states and focus visibility

- **State** Implemented
- **Depends on** M1-01n
- **Criteria** P05, P07
- **Result** Disabled field and button ignore hover (no misleading affordance) and carry a third channel (dashed border) beside opacity and cursor; button has an explicit instant `:focus-visible` ring; result heading uses `:focus-visible`; spinner no longer opts out of reduced-motion. `./scripts/check.sh` green.

### M1-01p · Self-host the demo faces

- **State** Implemented
- **Depends on** M1-01o
- **Criteria** P08
- **Result** Three latin woff2 faces (Figtree, Instrument Sans, JetBrains Mono, ~81 kB) ship from `frontend/src/fonts/` with `font-display: swap`; Google Fonts links removed from `index.html`, so the page opens zero third-party connections. `./scripts/check.sh` green.

### M1-01q · Harden the request path and live feedback

- **State** Implemented
- **Depends on** M1-01p
- **Criteria** P05, P07
- **Result** `requestRecommendation` aborts stalled requests after 15 s and turns malformed JSON into a request error keeping `X-Request-ID`; success keeps its reference and shows it on the card; loading moves keyboard focus to the announcement; the counter joins `aria-describedby`; dead error-heading ref removed. E2e asserts the success reference. `./scripts/check.sh` green.

### M1-01r · Harden backend edges and the runbook

- **State** Implemented
- **Depends on** M1-01q
- **Criteria** P01, P05, P08
- **Result** Unhandled errors return JSON 500 with `X-Request-ID`; empty fixture returns 503; `/api/` trailing slash returns JSON 404; recent IDs over 64 chars are rejected with blanks and padding covered; README runs use `--no-access-log`. Pytest covers each new branch. `./scripts/check.sh` green.

### M1-01s · Cover the new backend branches

- **State** Implemented
- **Depends on** M1-01r
- **Criteria** P01, P05
- **Result** Pytest pins the 64-char boundary both sides (64 accepted, 65 rejected) and forces the middleware except path (JSON 500 with `X-Request-ID`). `./scripts/check.sh` green.

### M1-01t · Redesign the demo screen (Darkroom, amber)

- **State** Implemented
- **Depends on** M1-01s
- **Criteria** P05, P07
- **Result** Second Hallmark full redesign at app scope: print-black ground, amber safelight primary, condensed poster capitals, zero radius, hairline sheet rows; Sofia Sans Extra Condensed and Barlow self-hosted; fonts carry no third party. `./scripts/check.sh` green with zero test edits.

### M1-01u · Point the field at the live radius token

- **State** Implemented
- **Depends on** M1-01t
- **Criteria** P07
- **Result** `.field` uses `var(--radius-card)` (zero under Darkroom) instead of the removed `--radius-part`; no visual change, no dead token reference. `./scripts/check.sh` green.

### M1-01v · Reject unusable recommendation shapes

- **State** Implemented
- **Depends on** M1-01u
- **Criteria** P05
- **Result** `requestRecommendation` validates the album shape (id, artist, title, reason as strings) and turns a wrong-shaped 200 into the request-error path with description kept, retry focused and `X-Request-ID` shown. E2e covers a malformed 200. `./scripts/check.sh` green.

### M1-01w · Harden hover and empty-shape branches

- **State** Implemented
- **Depends on** M1-01v
- **Criteria** P05, P07
- **Result** Primary hover moves to the deep amber (was visually inert against focus); shape guard requires non-blank id, artist, title and reason. E2e drives both malformed shapes in one retry flow with call counting. `./scripts/check.sh` green.

### M1-01x · Pin request IDs on health and 404 paths

- **State** Implemented
- **Depends on** M1-01w
- **Criteria** P05, P08
- **Result** Pytest asserts `X-Request-ID` on `/healthz` and on every unknown-API 404 shape (GET/POST/OPTIONS/HEAD), pinning the middleware order for log correlation. `./scripts/check.sh` green.

### M1-01y · Fix stale docs and dash copy

- **State** Implemented
- **Depends on** M1-01x
- **Criteria** P02, D01
- **Result** Product, D01 and architecture carry explicit M1 demo exceptions (no link/year, no matching, no second pick until M2); M1-01i result fixed for the dropped year; backlog names both product branches; UI uses `1 to 500` instead of the en dash. `./scripts/check.sh` green.

### M1-02 · Package and smoke-test the HTTPS route

- **State** Blocked (2026-11-22: no container runtime in the agent environment — `docker` CLI absent, no `/var/run/docker.sock`; SSH/SCP denied by workspace policy — so the image cannot be built or smoke-tested here; Mikrus subdomain mapping plus host-port/HTTPS/resource observations are owner-run steps per operations)
- **Depends on** M1-01
- **Criteria** P01, P02, P07

Build the production-shaped image off the server. Add the minimal Compose setup and the early deployment instructions in [operations](operations.md). Smoke-test the exact image locally. Provide the owner with a reproducible way to deploy it under the included Mikrus subdomain and capture HTTPS, host port reachability and resource observations. The owner runs the server-side step from their operations environment. The milestone handoff identifies any live check still waiting for that step. The image installs `backend/requirements.txt` only; `backend/requirements-test.txt` stays in CI and local checks (M1-01f).

## M2 · Make it worth using

| Work item | State | Depends on | Result and evidence |
|---|---|---|---|
| **M2-01 · Import an eligible catalogue** | Open | Accepted M1 | SQLite schema, validated versioned source or import, and persistence on a local volume. The owner can rebuild it and inspect provenance. Integration checks use a temporary database. P02, P04. |
| **M2-02 · Match descriptions locally** | Open | M2-01 | Match supported constraints, rank by evidence, choose among comparable matches and handle no eligible result. Test known constraints, no match and seeded variation. P02, P04, P06. |
| **M2-03 · Add another pick and polish the result** | Open | M2-02 | Keep the description, avoid recent album IDs when an alternative exists, handle exhaustion, and open a suitable listening link. Verify one repeated request in the browser and do a short mobile playtest. P02, P03, P05, P07. |

## M3 · Measure the provider's value

| Work item | State | Depends on | Result and evidence |
|---|---|---|---|
| **M3-01 · Prepare the shared comparison set** | Open | Accepted M2 | Version 30–50 synthetic descriptions, expected constraints and a simple fit rubric. Record the local baseline against a fixed catalogue. P02–P04. |
| **M3-02 · Integrate bounded interpretation and fallback** | Open | M3-01 | One typed provider call, a deadline, request limits, validated responses and a local fallback. Cover timeout, malformed output, free quota exhaustion and disabled mode with simulated results. Record the proxy client-identity finding for any per-client limit. P06, P08. |
| **M3-03 · Compare and decide** | Open | M3-02 | Run the approved free trial with synthetic inputs. Compare the same examples and note fit, failures, response times, real plan settings and handling of visitor text. Record the owner's enable or disable decision, including a clear UI notice if enabled. P06, P08. |

## M4 · Release to friends

| Work item | State | Depends on | Result and evidence |
|---|---|---|---|
| **M4-01 · Verify operations and recovery** | Open | Accepted M3 | Check the release image, log rotation, restart, backup, restore and rollback. Include a small load smoke test from outside the VPS with the decision provider disabled. Review host and proxy logging before any privacy claim and confirm abuse behaviour. |
| **M4-02 · Accept a release candidate** | Open | M4-01 | Hand over the release tag, test evidence, live URL or deployment steps and a short playtest. Verify mobile, keyboard, different moods, repeat requests, links and graceful fallback. The owner chooses when to share. P01–P08. |
