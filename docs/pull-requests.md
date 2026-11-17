# Pull requests

Owner-side checklist. A PR is the owner's vehicle for publishing or human review; the workflow never requires one (see `docs/delivery.md` section 4).

1. Owner: branch from a clean `main`. One topic per PR; keep harness work and product work separate.
2. Agent: run the matching checks, collect the required reviews on the identical base and tree, write commit bodies with base, tree, and verdicts.
3. Owner or agent: check `git diff origin/main...<branch> --stat` shows only the topic, and `--check` is clean.
4. Owner: push and open the PR with a short human description — what is inside, what was verified, what is explicitly not inside:

```text
## PR <n>: <topic in plain words>

<Scope: what is inside>
<Verification: checks and reviews in plain words>
<Not inside: explicit exclusions>
```

5. Owner: merge with a regular merge commit (no squash), so base and tree SHAs in commit bodies stay traceable (see `docs/delivery.md` section 4).
6. Owner: merge `main` into working branches, realign local `main`, delete the topic branch and obsolete backups — or ask the agent to prepare these steps locally without pushing.
