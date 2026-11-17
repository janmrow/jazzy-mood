# Delivery workflow

`/deliver` handles the active milestone in [backlog](backlog.md). It runs on a local branch and ends with a result the owner can try. It can complete several small commits in one session. The visible state of the project is the backlog and Git history.

## 1. Start or resume

- Read [AGENTS.md](../AGENTS.md), the backlog, the relevant acceptance criteria and the latest commits. Confirm the active milestone, its prerequisites and the working branch.
- Use a local branch such as `deliver/m0`. Preserve work from another person or another task. Reuse a branch with attributable work from an interrupted run. Compare pending progress against the committed backlog. An uncommitted `Implemented` marker belongs to the pending change and only takes effect after its commit. When unrelated changes prevent isolation, use a separate worktree if the task is independent or report the concrete conflict.
- Pick the first ready item by dependency and value. Split it into coherent changes if needed. Update the backlog with the item ID and any dependency the split creates. Work on independent ready items if one item becomes blocked.
- Read only the project material needed for the change. Take implementation details and reversible choices forward inside the existing decisions. Bring the owner a concrete choice if you need to change scope, an external data boundary, deployment topology or running cost.

## 2. Implement and collect evidence

- Keep the change small enough to explain and verify. A typical commit finishes one slice of behaviour, one data improvement or one operational change. Include affected docs and tests when needed.
- Use the matching checks from [quality](quality.md). Record commands, results and any check that could not be run. Resolve required check failures before marking a change implemented. Use real acceptance criteria as the basis of test expectations.
- Stage only the files that belong to the change. Include the backlog update in the staged snapshot. Run `git diff --cached --check`, inspect the staged file list and confirm that new files are included. If the change is incomplete, its staged status remains provisional until the gates pass.
- Run tests after the final staging, against the staged state: first confirm `git diff` shows no changes to the reviewed files, then run the tests. A worktree edit afterwards means re-stage, re-run the affected checks, and take a fresh snapshot.

## 3. Review rules

Each review judges one frozen snapshot; any material change to it invalidates prior verdicts.

| Change | Required reviews |
|---|---|
| Ordinary product, catalogue, behaviour or test-coverage change | `quality-review` |
| First complete product slice, API contract, data source or migration, inference, privacy, cost controls, deployment, or delivery and CI gates | `quality-review` and `engineering-review` |
| Editorial correction that changes no requirement or rule | Implementer's diff check |

Use a staged snapshot to give the reviewers consistent input. Record the base commit (`git rev-parse HEAD`) and an index tree ID from `git write-tree`. Capture the snapshot atomically: run `git write-tree` twice and require the same tree ID before saving the diff, proving the index did not change mid-capture. Save `git diff --cached --no-ext-diff` to an ignored file under `.delivery/` named for that tree (for example `.delivery/<tree_id>.diff`). Give each reviewer the same file, base commit, tree ID, item ID, criterion IDs and check evidence. Avoid including secrets or user data in the snapshot. Give neither reviewer the other's conclusions. Both can read relevant repository files. They work in separate OpenCode sessions and report in the background.

### Review request template

Send each reviewer the same message in this shape:

```text
Review the staged snapshot on its own merits.
Base commit: <HEAD sha>
Tree ID: <git write-tree id>
Snapshot file: .delivery/<tree_id>.diff
Item ID: <backlog item>
Criterion IDs: <Pxx, Dxx>
Changed files: <staged file list>
Check evidence: <commands run and their results>
Return your report in the shape from docs/delivery.md
under Review report format. Work independently.
```

### Review report format

Each reviewer returns one report in this shape:

```text
verdict: PASS | CHANGES_REQUESTED | UNABLE_TO_REVIEW
base_commit: <HEAD sha reviewed>
tree_id: <git write-tree id reviewed>
findings:
  - severity: blocking | advisory
    location: <file:line or scope>
    consequence: <what breaks for the user or system>
    criterion: <Pxx, Dxx, or workflow rule>
checks_observed: <commands actually run and their result>
```

A report is valid only for the identical base commit and staged tree it names. A missing verdict, a report that names a different base commit or tree ID, an unverifiable snapshot, or any blocking finding keeps the commit pending. If the reviewer cannot assess the change, return `UNABLE_TO_REVIEW` and state the missing evidence. Resolve blocking findings or seek a fresh verdict with evidence that resolves the objection. Document any consequential advisory finding you defer. If you make a material change, take a new snapshot, rerun the affected checks, and get fresh required verdicts. Include the base commit, tree ID, staged file list, and check evidence with each request so the basis of the decision can be reproduced. Stop and hand off a clear blocker if repeated review or test failures prevent progress.

The review step is a workflow instruction checked in the pilot. CI provides an independent check of the app once M1 introduces runnable code. If the pilot repeatedly misses review gates, inspect the session and tighten the workflow before considering a separate commit guard.

## 4. Commit, continue and hand off

### Git conventions

- Work on a local branch named for the job: `deliver/<milestone>` for milestone work, `pilot/*` for disposable harness trials (delete when done), `setup/*` for one-off setup branches such as PR preparation.
- Commits stay local. The agent commits on the working branch and never pushes, rewrites published history, or uses destructive commands. If asked to publish, the agent stops with the branch ready and hands it to the owner instead of attempting push. Publishing (push, pull request, merge) is the owner's decision in the owner's environment.
- A commit subject starts with the item ID and uses the imperative mood; the commit gate below defines the required subject and body evidence.
- A pull request is the owner's vehicle for publishing or for asking review outside the agent workflow. The workflow never requires one, and the snapshot reviews in section 3 stay valid on local snapshots with or without a PR.
- Integrate published branches with merge commits, not squash or rebase, so review evidence stays traceable to its base and tree SHAs.
- Merging a pull request publishes code; it never accepts a milestone. Acceptance is the owner's explicit statement, recorded in the backlog before the next milestone starts.

- Confirm the base commit and staged tree still match the reviewed snapshot. Before committing, confirm `git diff` shows no unstaged changes to the reviewed files, and that every required report names the current base commit and tree ID and carries all fields from the report shape; a report missing any of them counts as missing. A change to either requires a fresh snapshot and applicable gates. Use a commit subject that begins with the item ID and states the outcome. The commit body always records the checks run, the base commit, the tree ID, and the verdicts, so the evidence survives without the local `.delivery/` file. Verify the commit and the remaining working tree state, including that `git rev-parse <commit>^{tree}` equals the reviewed tree ID.
- Continue with the next ready item in the same milestone. A fresh session starts from the actual tree, backlog and history. Record a real blocker rather than marking progress complete based on intent or a pending check.
- When the agent-owned work is complete, set the milestone to `Awaiting acceptance` in the final work commit or a separate progress commit. Include any owner-run check that remains and keep its result open. The owner accepts the milestone and authorizes the next one. For example, the owner can say `I accept M0. Start M1.`, then run `/deliver M1`. Record that transition in the backlog before implementing the next milestone. The agent never marks a milestone Accepted and never starts the next milestone's items on its own judgment.

Keep the handoff in plain English:

```text
Milestone and status
What changed for the visitor
Where to try it or how to run it
Three things to try
Evidence and open questions
```

For example, when asking the owner to review repeat behaviour, give the working URL and one description to try twice. Describe what outcome counts as a different but still suitable pick. Show how to report feedback. Leave the owner's acceptance state open until they reply.

## Pilot the harness

Run this once with the intended OpenCode V2 installation and coding model, on a disposable branch in a fresh copy of the starter. Use a temporary backlog with two small self-contained items. Include a clear expected change and mark its first trial as requiring both reviews. Keep real project and production credentials out of this copy.

1. Run `/deliver`. See whether the intended agent chooses a ready item, obtains separate verdicts on the same snapshot, and creates a local commit. Check the session and Git log for that sequence.
2. Try a blocked run on a disposable branch. For instance, temporarily make one required review unavailable and use a task that explicitly requires it. Check that the agent reports which result is missing and leaves `HEAD` at the previous commit. A failing required check should also leave `HEAD` unchanged while it remains unresolved.
3. Start a new OpenCode session. Check that it resumes from the backlog and branch history without a recap of the previous chat. Check the owner handoff and reset the pilot branch when finished.

OpenCode project [commands](https://opencode.ai/docs/commands/), [agents](https://opencode.ai/docs/agents/) and [permissions](https://opencode.ai/docs/permissions/) provide the configuration used here. Check local and managed policy if a permitted development command is blocked. Run production steps from the owner's operations environment.
