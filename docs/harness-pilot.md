# Harness pilot

Short pilot of the autonomous workflow before `M0` delivery. Isolated copies only; the real backlog and production data were not touched.

- OpenCode v2.3.0, Muse Spark 1.3 Contributor model, 2026-11-17; isolated copies only, real backlog untouched.
- Config: `default_agent` delivery; push/reset/ssh/scp denied; six review requests ran (A2×2, PT-01×2, broken-link×1, this report×1).

## Observed through review sessions (scenarios 1–3)

| # | Scenario | Result |
| --- | --- | --- |
| 1 | Normal task with correct commit | PT-01 probe file committed in the pilot copy (`75c0af3`). |
| 2 | Two independent reviews of the same snapshot | Same base `60c95c7` and tree `52c82908` sent to two separate sessions; `quality-review` PASS and `engineering-review` PASS, neither saw the other's conclusions. A2 on the real branch showed the same pattern (base `0266772`, tree `bc4054f`, two PASS, commit `60c95c7`). |
| 3 | `CHANGES_REQUESTED` | Broken link (`docs/does-not-exist.md`, link check FAIL) got `CHANGES_REQUESTED` with one blocking finding at `docs/pilot-probe.md:2`. No commit; pilot `HEAD` stayed at `75c0af3`. |

## Mechanical checks, scenarios 4–7 (shell only, no reviewer session)

| # | Check | Result |
| --- | --- | --- |
| 4 | Gate-count illustration | Broken snapshot required two verdicts but only the quality verdict was requested; recorded as missing result, commit blocked, `HEAD` unchanged. No missing-verdict round was run; enforcement untested. |
| 5 | Failed check | Trailing-whitespace fixture made `git diff --cached --check` exit 2 with `HEAD` unchanged; after fixing the file the same check passed. Command ran; no agent commit was blocked by it. |
| 6 | Snapshot change | Staged edit changed the tree ID (`T1` vs `T2`, different). No PASS was invalidated through re-review; the fresh-verdict rule is quoted from the docs, not exercised. |
| 7 | Session resume | A fresh shell recovered branch, `git log`, staged state, and the pilot backlog with no prior chat recap. No fresh OpenCode session resumed the work. |

Pilot review requests carried the diff inline because the isolated copy sits outside the workspace root. Base commit, tree ID, and diff content were identical for both reviewers of each snapshot.

## Behaviour checks

- `HEAD` stayed unchanged in every negative case. Only the `CHANGES_REQUESTED` case refused through an actual review verdict; the rest report shell output, not review verdicts.
- Evidence lists only commands actually run and verdicts actually received through review sessions.
- Scenarios 1–3 ran through reviewer sessions; scenarios 4–7 are shell illustrations only and do not demonstrate gate enforcement. No workflow change follows from this pilot alone. A real `/deliver` pilot with a delivery-agent session remains an owner-run step.

## Open point

A3 is evidence, not a gate change. The next step is ordinary `M0-01`/`M0-02` delivery work; `M1` items stay untouched until `M0` is accepted.
