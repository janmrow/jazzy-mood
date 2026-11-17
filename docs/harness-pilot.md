# Harness pilot

Short pilot of the autonomous workflow before `M0` delivery. Isolated copies only; the real backlog and production data were not touched.

- OpenCode: v2.3.0
- Coding model: Muse Spark 1.3 Contributor
- Date: 2026-11-17
- Real branches: `main` (baseline `0266772`), `deliver/m0` (A2 `60c95c7`)
- Pilot copies: `/tmp/jazzy-pilot-janek` (branch `pilot/a3-test`), `/tmp/jazzy-pilot-gates` (mechanical gate checks)
- Config: `default_agent` is `delivery`; `/deliver` command and `delivery`, `quality-review`, `engineering-review` agents present; `git push`, `reset --hard`, `clean`, `ssh`, `scp` denied. Subagent launch worked for all five review requests.

## Scenarios and observed results

| Scenario | Observed result |
|---|---|
| Normal task with correct commit | PT-01 probe file committed in the pilot copy (`75c0af3`). |
| Two independent reviews of the same snapshot | Same base `60c95c7` and tree `52c82908` sent to two separate sessions; `quality-review` PASS and `engineering-review` PASS, neither saw the other's conclusions. A2 on the real branch showed the same pattern (base `0266772`, tree `bc4054f`, two PASS, commit `60c95c7`). |
| `CHANGES_REQUESTED` | Broken link (`docs/does-not-exist.md`, link check FAIL) got `CHANGES_REQUESTED` with one blocking finding at `docs/pilot-probe.md:2`. No commit; pilot `HEAD` stayed at `75c0af3`. |
| Missing required reviewer | Broken snapshot required two verdicts but only the quality verdict was requested; recorded as missing result, commit blocked, `HEAD` unchanged. PT-01 with 2/2 verdicts was allowed, which confirms the gate counts. |
| Failed required test | Trailing-whitespace fixture made `git diff --cached --check` exit 2 with `HEAD` unchanged; after fixing the file the same check passed. |
| Snapshot change after PASS | Staged edit changed the tree ID (`T1` vs `T2`, different); the earlier verdict cannot authorize the new tree, so fresh verdicts are required. |
| Session resume | A fresh shell recovered branch, `git log`, staged state, and the pilot backlog with no prior chat recap. |

Pilot review requests carried the diff inline because the isolated copy sits outside the workspace root. Base commit, tree ID, and diff content were identical for both reviewers of each snapshot.

## Behaviour checks

- No commit was made with an unmet gate: the `CHANGES_REQUESTED`, missing-reviewer, and failed-check cases all left `HEAD` unchanged.
- No test was claimed without running it: evidence above lists only commands actually run and verdicts actually received.
- No workflow fix was needed: every critical scenario produced the expected gate behaviour. The two intentional negative controls (broken link, whitespace error) were fixed or left uncommitted inside the pilot copies only.

## Open point

A3 is evidence, not a gate change. The next step is ordinary `M0-01`/`M0-02` delivery work; `M1` items stay untouched until `M0` is accepted.
