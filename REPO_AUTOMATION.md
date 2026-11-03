# Daily GitHub repository automation

This controller performs a **read-only health audit** of a random sample of 2–12 active repositories owned by the account each day. It records a dated report in `reports/`.

It does not manufacture commits, edit application source code, install dependencies, merge pull requests, or write to the repositories being audited. The only automated commit is the useful dated audit report in this controller repository.

## What it checks

For each selected repository:

- Whether a README exists
- Whether a language-bearing repository has a GitHub Actions workflow
- Whether a repository description is set
- Whether a license is declared
- Whether the repository has had a push in the last 365 days

These are advisory signals, not automatic defects. For example, a project may intentionally have no CI workflow or license.

## Privacy

The profile repository is public. Reports therefore include individual details only for public repositories. Private repository names, URLs, languages, and individual findings are not written to the report or printed in workflow logs; private results are aggregated by finding type only.

## One-time setup

1. Create a **fine-grained personal access token** at https://github.com/settings/personal-access-tokens/new.
2. Select your account as the resource owner and grant access to **all repositories** you want included (or choose all repositories).
3. Grant repository permissions:
   - Metadata: Read-only
   - Contents: Read-only
4. Add the token to this repository under **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `REPO_AUDIT_TOKEN`
   - Value: the token you just created
5. Open **Actions → Daily repository health audit → Run workflow** for the first run.

The workflow's built-in `GITHUB_TOKEN` only needs Contents: Read and write for this controller repository. It is not used to access other repositories.

## Schedule and selection

The scheduled workflow starts daily at 07:43 UTC (13:13 India time). It deterministically selects a random number from 2–12 and a random sample for each UTC day, so manually rerunning it on the same day audits the same sample. GitHub may delay scheduled workflow starts during periods of high load.

Archived and disabled repositories are skipped. Forks are included in the read-only audit if they are active and owned by the account.

## Reports

Each successful run writes `reports/YYYY-MM-DD.json`. The report is committed only when its contents change.

## Extending safely

A later phase can add opt-in, repository-specific maintenance pull requests (for example, a verified documentation correction or a dependency update with passing tests). Keep those changes as pull requests for review. Do not enable unattended source-code rewrites or auto-merge across every repository.
