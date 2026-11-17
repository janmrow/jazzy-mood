# Quality

Use [product criteria](product.md#acceptance-criteria) and actual risk to select checks. The goal is confidence in the release and short, useful evidence for the owner's playtest.

## Evidence by risk

| Risk | Evidence to add when the behaviour lands |
|---|---|
| Invalid input calls the provider or leaks into logs | pytest API checks for blank and oversized input, a provider call spy, and a log inspection with a unique synthetic phrase. P01, P08. |
| The result is outside the catalogue or ignores a known constraint | Unit checks on eligibility and selection and an API check against a small known catalogue. Check an explicit instrumental preference and a no-match case. P02, P04. |
| The same result returns after asking for another | Check session exclusions, exhausted choices and variety across valid matches. Control randomness in tests where the result must be reproducible. P03. |
| A slow or unavailable provider breaks the page | Simulate timeouts, quota responses and malformed typed output. Exercise the real selection logic and check that the local path still returns a valid album. P05 covers retry without losing input; P06 covers the fallback still returning a valid album within the M3 deadline. |
| The form works by API but fails for a visitor | A small Playwright suite covers the main journey and important recovery. The owner also tries the phone view, keyboard behaviour, copy and links. P01, P02, P05, P07. |
| A catalogue update damages music data or repeat handling | Validate required fields and sources, allowed tag values, duplicate IDs, eligible links and migrations. Run an import against a temporary SQLite database and check repeat imports. P02–P04. |
| A technically healthy release cannot be operated | Smoke-test the same image over HTTPS. Record memory, disk, latency and error observations. Rehearse backup, restore and rollback. Check log rotation and the cost and data controls in [operations](operations.md). |

## Local and CI checks

Before the app exists, check the relevant documents and source data, and use `git diff --cached --check` on the proposed change. For M0, required checks are `git diff --cached --check` plus the backlog item's manual inspection list recorded as evidence. M1 introduces one check entry point, documented in the README, that CI runs as well. Include frontend type checking, the production build, pytest and the essential browser journey. Make CI report failure when a check fails. Use fixtures and a simulated provider in routine checks, even if a live provider has been configured on a developer's machine.

Keep the automated suite small and meaningful. Derive assertions from expected behaviour and failures a visitor would notice. Use stable IDs and properties of recommendations as assertions. An exact title is appropriate only when the test fixture makes that choice meaningful. Reviewers should ask what would break if a test were removed or if a faulty change passed it.

## Model and catalogue evaluation

Use 30–50 synthetic descriptions with a frozen catalogue and recorded matcher and provider versions. Include varied energy, rhythm, ambiguity, explicit constraints, thin catalogue coverage and repeats. A small English set is the release baseline. Add representative Polish descriptions if evaluating a later language claim.

1. Record eligible results or expected boundaries for each example. Some cases can have several good picks. Treat a violated explicit constraint as a failure.
2. Compare the local-selection and provider-assisted paths on the same set. Score musical fit as 0 for unsuitable, 1 for plausible or 2 for strong. Record unsupported reasons, repeated choices, no-match results, response time and provider errors.
3. Ask the owner to listen to a representative sample and judge usefulness without seeing which method made each pick when practical. Record important disagreements.
4. Keep the free decision provider enabled for visitors only if the owner accepts its contribution, cost boundary and data handling. Preserve local selection and rerun a targeted comparison when the catalogue, prompt or provider changes materially.

## Owner playtest

Allow 10–15 minutes with a phone and a desktop. Try:

1. `A quiet rainy evening, some groove, no vocals.` Look for a plausible result and a reason you can understand.
2. `Something energetic and sample-heavy.` Compare the change in feel. Tap `Try another` and check that the second pick still fits.
3. Enter spaces and trigger a controlled network failure. Check feedback, keyboard navigation and whether you can recover without typing the description again.
4. Open the listening link and, in the M3 or later preview, try the same request with the provider disabled.

Send the agent a short observation with the expected outcome. It records whether the issue changes an acceptance criterion, reveals a bug, or suggests new work. A playtest decision is recorded separately from automated check results.

## Performance and follow-up experiments

Run the initial k6 smoke test from another machine against the owner's test deployment. Use a little concurrent traffic, for example five simultaneous users for a minute, with external inference switched off. Record the 95th percentile latency, unexpected errors and VPS headroom. Set the release threshold using that baseline and the owner's experience. Measure external inference separately on a small sample. Later mutation tests can check whether the suite detects specific mistakes in ranking, eligibility or fallback.
