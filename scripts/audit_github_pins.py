#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass


PROFILE_LOGIN = "AlexGerlitz"


@dataclass(frozen=True)
class ExpectedPin:
    name_with_owner: str
    description_snippets: tuple[str, ...]
    language: str | None = None


EXPECTED_PINS: tuple[ExpectedPin, ...] = (
    ExpectedPin(
        "AlexGerlitz/drivedesk-core",
        ("Operations and integration platform", "FastAPI", "PostgreSQL", "OpenAPI"),
        "Python",
    ),
    ExpectedPin(
        "AlexGerlitz/ai-ops-workflow-kit",
        ("FastAPI AI workflow backend", "RAG", "approvals", "Telegram"),
        "Python",
    ),
    ExpectedPin(
        "AlexGerlitz/deploymate",
        ("Self-hosted Docker deployment control panel", "CI/CD", "runbooks"),
        "JavaScript",
    ),
    ExpectedPin(
        "AlexGerlitz/AlexGerlitz",
        ("AI Automation", "DriveDesk AI Operator", "FastAPI", "Docker"),
        "HTML",
    ),
    ExpectedPin(
        "AlexGerlitz/MPlusForm",
        ("validation-boundary automation proof", "Python sync pipeline", "Windows ops"),
        "Python",
    ),
)

QUERY = """
query($login: String!) {
  user(login: $login) {
    pinnedItems(first: 6, types: [REPOSITORY]) {
      totalCount
      nodes {
        ... on Repository {
          nameWithOwner
          description
          isPrivate
          isArchived
          primaryLanguage {
            name
          }
          url
        }
      }
    }
  }
}
"""


def run_gh_graphql() -> dict:
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI 'gh' is required for pinned repository audit")

    completed = subprocess.run(
        ["gh", "api", "graphql", "-f", f"login={PROFILE_LOGIN}", "-f", f"query={QUERY}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise RuntimeError(f"gh api graphql failed: {stderr or completed.returncode}")
    return json.loads(completed.stdout)


def check_pins(payload: dict) -> list[str]:
    errors: list[str] = []
    pinned = payload["data"]["user"]["pinnedItems"]
    nodes = pinned["nodes"]

    if pinned["totalCount"] < len(EXPECTED_PINS):
        errors.append(f"expected at least {len(EXPECTED_PINS)} pinned repositories, got {pinned['totalCount']}")

    actual_order = [node["nameWithOwner"] for node in nodes]
    expected_order = [pin.name_with_owner for pin in EXPECTED_PINS]
    if actual_order[: len(expected_order)] != expected_order:
        errors.append(f"unexpected pinned repository order: {actual_order!r}")

    by_name = {node["nameWithOwner"]: node for node in nodes}
    for expected in EXPECTED_PINS:
        node = by_name.get(expected.name_with_owner)
        if not node:
            errors.append(f"missing pinned repository: {expected.name_with_owner}")
            continue
        if node.get("isPrivate"):
            errors.append(f"{expected.name_with_owner}: must be public")
        if node.get("isArchived"):
            errors.append(f"{expected.name_with_owner}: must not be archived")
        description = node.get("description") or ""
        for snippet in expected.description_snippets:
            if snippet not in description:
                errors.append(f"{expected.name_with_owner}: description missing {snippet!r}")
        language = (node.get("primaryLanguage") or {}).get("name")
        if expected.language and language != expected.language:
            errors.append(f"{expected.name_with_owner}: expected language {expected.language!r}, got {language!r}")

    return errors


def main() -> int:
    try:
        payload = run_gh_graphql()
    except Exception as exc:
        print(f"github pins audit failed: {exc}")
        return 1

    errors = check_pins(payload)
    if errors:
        print("github pins audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("github pins audit passed")
    for pin in EXPECTED_PINS:
        print(f"ok pinned: {pin.name_with_owner}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
