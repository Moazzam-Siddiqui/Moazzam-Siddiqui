#!/usr/bin/env python3
"""Read-only daily health sampler for repositories owned by the authenticated user.

Private repository names and findings are never written to this public repository.
Only aggregate private-repository counts are included in the report.
"""
from __future__ import annotations

import base64
import json
import os
import random
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com"
TOKEN = os.environ.get("REPO_AUDIT_TOKEN")
LOGIN = os.environ.get("GITHUB_ACTOR", "").lower()
OUT = Path("reports")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "moazzam-repo-health-audit",
    "X-GitHub-Api-Version": "2022-11-28",
}


def api_get(path: str):
    request = Request(API + path, headers=HEADERS)
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 404:
            return None
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"GitHub API returned {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError(f"GitHub API request failed: {exc}") from exc


def list_owned_repositories():
    repos = []
    page = 1
    while True:
        batch = api_get(
            f"/user/repos?visibility=all&affiliation=owner&per_page=100&page={page}&sort=pushed"
        )
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response while listing repositories.")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [
        repo for repo in repos
        if repo.get("owner", {}).get("login", "").lower() == LOGIN
        and not repo.get("archived", False)
        and not repo.get("disabled", False)
    ]


def audit_repository(repo):
    full_name = repo["full_name"]
    encoded = quote(full_name, safe="/")
    findings = []

    readme = api_get(f"/repos/{encoded}/readme")
    if readme is None:
        findings.append("missing_readme")

    workflows = api_get(f"/repos/{encoded}/contents/.github/workflows")
    has_workflows = isinstance(workflows, list) and any(
        item.get("type") == "file" and item.get("name", "").endswith((".yml", ".yaml"))
        for item in workflows
    )
    if repo.get("language") and not has_workflows:
        findings.append("no_github_actions_workflow")

    if not repo.get("description"):
        findings.append("missing_description")
    if not repo.get("license"):
        findings.append("missing_license")

    pushed = repo.get("pushed_at")
    age_days = None
    if pushed:
        pushed_dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - pushed_dt).days
        if age_days >= 365:
            findings.append("no_push_in_365_days")

    return {
        "name": full_name,
        "visibility": repo.get("visibility", "unknown"),
        "fork": bool(repo.get("fork")),
        "language": repo.get("language"),
        "stars": repo.get("stargazers_count", 0),
        "last_push": pushed,
        "days_since_last_push": age_days,
        "findings": findings,
    }


def main():
    if not TOKEN:
        raise RuntimeError(
            "Missing REPO_AUDIT_TOKEN. Add a fine-grained token with Metadata: read "
            "and Contents: read access to the repositories you want scanned."
        )
    if not LOGIN:
        raise RuntimeError("Missing GITHUB_ACTOR; run this script from GitHub Actions.")

    # Stable daily selection: reruns on the same UTC day audit the same repositories.
    today = datetime.now(timezone.utc).date().isoformat()
    repos = list_owned_repositories()
    if not repos:
        raise RuntimeError("No active repositories owned by the authenticated account were found.")

    rng = random.Random(f"{LOGIN}:{today}")
    target_count = min(rng.randint(2, 12), len(repos))
    selected = rng.sample(repos, target_count)

    public_results = []
    private_findings = Counter()
    public_findings = Counter()
    private_scanned = 0
    public_scanned = 0

    for repo in selected:
        result = audit_repository(repo)
        if repo.get("private"):
            private_scanned += 1
            private_findings.update(result["findings"])
        else:
            public_scanned += 1
            public_findings.update(result["findings"])
            public_results.append(result)

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "account": LOGIN,
        "selection": {
            "eligible_active_owned_repositories": len(repos),
            "random_daily_target": target_count,
            "repositories_scanned": len(selected),
            "selection_is_stable_for_utc_day": True,
        },
        "summary": {
            "public_repositories_scanned": public_scanned,
            "private_repositories_scanned": private_scanned,
            "public_findings": dict(sorted(public_findings.items())),
            "private_findings_aggregate_only": dict(sorted(private_findings.items())),
        },
        "public_repository_details": public_results,
        "privacy_note": (
            "Private repository names, URLs, languages, and individual findings are "
            "intentionally excluded from this report because the controller repository is public."
        ),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{today}.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Audited {len(selected)} active owned repositories "
        f"({public_scanned} public, {private_scanned} private). "
        f"Public report: {path.as_posix()}"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Repository audit failed: {exc}", file=sys.stderr)
        sys.exit(1)
