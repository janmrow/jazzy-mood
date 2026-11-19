# Backlog

- **Active milestone** M0
- **Milestone state** Awaiting acceptance (agent work complete; owner listening check and boundary decision open)
- **Accepted milestones** None
- **Product branch** `deliver/m0` holds the M0 sample and trial; harness and setup branches hold workflow and docs polish only and never carry product changes.

The delivery agent may choose and split items inside the active milestone. An item is ready once its dependencies are implemented, any named prerequisite decision is recorded and the work has enough evidence to begin. The owner sets the next milestone at acceptance. See [delivery](delivery.md) for state transitions and [product](product.md) for the `P01`–`P08` criteria.

Use `Open`, `Implemented` or `Blocked` on work items. Milestone states (`In delivery`, `Awaiting acceptance`, `Accepted`) live with the Active milestone line above and are never interchangeable with item states. Add one short note for a material result or a blocker. When splitting an item, use child IDs such as `M1-01a`, keep the parent outcome, and mark the parent implemented only when its acceptance evidence is complete. Use the item ID in the commit subject so progress can be found in Git.

## M0 · Prove the catalogue

### M0-01 · Prepare a sourced catalogue sample

- **State** Implemented
- **Depends on** None
- **Criteria** P02, P04
- **Result** 30-row validated sample (13 instrumental, 15 vocal, 2 unknown); `tools/validate_catalog.py` reports OK 30 rows with 30 proposed rows pending the listening check; pytest 25 passed.

Create `catalog/m0-sample.csv` with about 30 candidate albums across the proposed music styles. Record a stable candidate ID, artist, title, year when verified, identity source and relevant reuse notes. Add a small vocabulary to describe energy, mood, groove and vocals where evidence supports it. Record the basis for those attributes and allow unknown values. Use a documented convention for multiple tags so later import work is straightforward.

The owner can sort or inspect the sample, open representative identity sources and distinguish facts from proposed labels. Check for duplicate albums, missing identity sources and unclear reuse before committing. Flag incomplete candidates and keep them separate from any eligible release data. If permissions or evidence limit the sample, report the actual count and gaps.

### M0-02 · Try the sample against realistic requests

- **State** Implemented
- **Depends on** M0-01
- **Criteria** P02, P03, P04
- **Result** Trial covers M0-001 to M0-030 with 10 cases (vague, strict instrumental, two alternative sets, three gaps, mood contrast, unknown handling, soft preference) plus the catalogue boundary recommendation; all picks fit 1 proposed pending the listening check.

Create `docs/catalogue-trial.md` with 8–12 practical English descriptions and examples of suitable candidates from the sample. Include at least one vague request, one strict instrumental constraint, one request with good alternatives and one gap or mismatch. Show why the available data supports each highlighted example. Mark uncertain interpretations for the owner's listening check.

Present a short recommendation on catalogue boundaries, whether albums are worth keeping, and which data needs improvement before widening the import. The owner can try several listening links and accept the direction. This item can be completed with local findings before any live inference or paid account is used.

## M1 · Deliver the first link

### M1-01 · Build and check a complete form-to-result flow

- **State** Open
- **Depends on** Accepted M0
- **Criteria** P01, P02, P05, P07

Implement one English form calling the API, which returns an album from a tiny local fixture. Display the result, loading and a recoverable failure. Keep useful focus and keyboard behaviour. Include a cheap health endpoint at `/healthz`. Add the project check command and CI to this first app slice. Use pytest for request validation and the successful response, and a Playwright test from form submission to displayed card. Both reviewers check this first complete product slice.

The owner can start it locally with documented commands, get a result, and verify that a blank submission or a simulated failure gives clear feedback. The playtest may use controlled test data. Mark the fixture clearly when demonstrating it.

### M1-02 · Package and smoke-test the HTTPS route

- **State** Open
- **Depends on** M1-01
- **Criteria** P01, P02, P07

Build the production-shaped image off the server. Add the minimal Compose setup and the early deployment instructions in [operations](operations.md). Smoke-test the exact image locally. Provide the owner with a reproducible way to deploy it under the included Mikrus subdomain and capture HTTPS, host port reachability and resource observations. The owner runs the server-side step from their operations environment. The milestone handoff identifies any live check still waiting for that step.

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
