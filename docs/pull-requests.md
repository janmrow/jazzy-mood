# Pull requests

Light checklist for future PRs. A PR is the owner's vehicle for publishing or human review; the workflow never requires one.

1. Branch from a clean `main`. One topic per PR; keep harness work and product work in separate PRs.
2. Before push: run the matching checks, collect the required reviews on the identical base and tree, and write commit bodies with base, tree, and verdicts.
3. Check `git diff origin/main...<branch> --stat` shows only the topic, and `--check` is clean.
4. Push and open the PR with a short human description: what is inside, what was verified, what is explicitly not inside.
5. Merge with a regular merge commit (no squash), so base and tree SHAs in commit bodies stay traceable.
6. After merge: merge `main` into working branches, realign local `main`, delete the topic branch and obsolete backups.
