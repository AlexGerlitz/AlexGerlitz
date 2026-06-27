#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass


DEFAULT_COMMITS_PER_REPO = 20


def marker(*parts: str) -> str:
    return "".join(parts)


@dataclass(frozen=True)
class RepoCheck:
    name_with_owner: str
    required_recent_subjects: tuple[str, ...] = ()
    commits_per_repo: int = DEFAULT_COMMITS_PER_REPO


REPOS: tuple[RepoCheck, ...] = (
    # The profile repo changes often while the funnel is refined; audit the wider
    # recent window for weak public subjects instead of pinning an old title.
    RepoCheck(
        "AlexGerlitz/AlexGerlitz",
        (),
        40,
    ),
    RepoCheck(
        "AlexGerlitz/drivedesk-core",
        ("Tighten DriveDesk Core review surface",),
    ),
    RepoCheck(
        "AlexGerlitz/ai-ops-workflow-kit",
        ("Harden reviewer acceptance capture",),
    ),
    RepoCheck(
        "AlexGerlitz/deploymate",
        ("Route DeployMate reviewers to proof snapshot",),
    ),
    RepoCheck(
        "AlexGerlitz/MPlusForm",
        ("Reduce domain noise in project intro",),
    ),
)


BAD_SUBJECT_PATTERNS: tuple[str, ...] = (
    r"^wip\b",
    r"^tmp\b",
    r"^test\b",
    r"quick\s+fix",
    marker(r"AI", r"-generated"),
    marker(r"Chat", r"GPT"),
    marker(r"AI", r"/Codex"),
    marker(r"generated", r"\s+by"),
    marker(r"vibe", r"\s+coding"),
    marker(r"prompt", r"\s+dump"),
    marker(r"hiring", r"\s+screen"),
    marker(r"inter", r"view"),
    marker(r"со", r"бес"),
)


def run_gh_api(path: str) -> object:
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI 'gh' is required for public commit title audit")

    completed = subprocess.run(
        ["gh", "api", path],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise RuntimeError(f"gh api {path!r} failed: {stderr or completed.returncode}")
    return json.loads(completed.stdout)


def fetch_recent_subjects(repo: RepoCheck) -> list[tuple[str, str, str]]:
    payload = run_gh_api(f"repos/{repo.name_with_owner}/commits?per_page={repo.commits_per_repo}")
    if not isinstance(payload, list):
        raise RuntimeError(f"{repo.name_with_owner}: unexpected commits API payload")

    subjects: list[tuple[str, str, str]] = []
    for item in payload:
        sha = str(item.get("sha", ""))[:7]
        commit = item.get("commit") or {}
        authored_at = ((commit.get("author") or {}).get("date")) or ""
        message = str(commit.get("message") or "")
        subject = message.splitlines()[0].strip()
        subjects.append((sha, authored_at, subject))
    return subjects


def check_repo(repo: RepoCheck) -> list[str]:
    errors: list[str] = []
    recent = fetch_recent_subjects(repo)

    if len(recent) < min(5, repo.commits_per_repo):
        errors.append(f"{repo.name_with_owner}: expected at least 5 recent commits, got {len(recent)}")

    recent_subjects = [subject for _, _, subject in recent]
    for required in repo.required_recent_subjects:
        if required not in recent_subjects:
            errors.append(f"{repo.name_with_owner}: missing recent public subject {required!r}")

    compiled = [(pattern, re.compile(pattern, re.IGNORECASE)) for pattern in BAD_SUBJECT_PATTERNS]
    for sha, authored_at, subject in recent:
        if not subject:
            errors.append(f"{repo.name_with_owner}@{sha}: empty public commit subject")
            continue
        if len(subject) > 72:
            errors.append(f"{repo.name_with_owner}@{sha}: public commit subject over 72 chars: {subject!r}")
        for label, regex in compiled:
            if regex.search(subject):
                errors.append(
                    f"{repo.name_with_owner}@{sha} {authored_at}: weak public commit subject {subject!r} ({label})"
                )

    return errors


def main() -> int:
    errors: list[str] = []
    try:
        for repo in REPOS:
            errors.extend(check_repo(repo))
    except Exception as exc:
        print(f"public commit title audit failed: {exc}")
        return 1

    if errors:
        print("public commit title audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("public commit title audit passed")
    for repo in REPOS:
        print(f"ok recent commits: {repo.name_with_owner}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
