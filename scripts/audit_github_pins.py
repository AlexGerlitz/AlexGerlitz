#!/usr/bin/env python3
from __future__ import annotations

import base64
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
    homepage_url: str | None = None
    topics: tuple[str, ...] = ()
    readme_snippets: tuple[str, ...] = ()


EXPECTED_PINS: tuple[ExpectedPin, ...] = (
    ExpectedPin(
        "AlexGerlitz/drivedesk-core",
        ("Operations and CRM/ERP integration platform", "FastAPI", "PostgreSQL", "OpenAPI"),
        "Python",
        "https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/",
        (
            "backend",
            "fastapi",
            "postgresql",
            "integration-platform",
            "operations-platform",
            "platform-engineering",
            "systems-integration",
        ),
        (
            "public backend/platform foundation behind the DriveDesk AI",
            "Profile / contact route",
            "LinkedIn Recruiter Packet",
            "Decision-Ready Contact",
            "Shortest proof path",
            "https://www.linkedin.com/in/alex-gerlitz-a659ab3bb/",
            "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-python-backend-automation-resume.pdf",
            "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
            "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
            "60-Second Review",
            "FastAPI, PostgreSQL/Alembic",
            "Integration discipline",
            "Production proof",
        ),
    ),
    ExpectedPin(
        "AlexGerlitz/ai-ops-workflow-kit",
        (
            "AI sales/support workflow backend",
            "business scenario replay",
            "RAG",
            "transcript analysis",
            "Telegram approvals",
            "CRM handoff",
        ),
        "Python",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/business-scenario-replay.txt",
        (
            "ai-automation",
            "llm-workflows",
            "rag",
            "crm",
            "fastapi",
            "n8n",
            "telegram-bot",
            "workflow-automation",
            "backend-development",
            "platform-engineering",
        ),
        (
            "Production-minded reference implementation for AI workflow orchestration",
            "Profile / contact route",
            "LinkedIn Recruiter Packet",
            "Decision-Ready Contact",
            "Shortest proof path",
            "https://www.linkedin.com/in/alex-gerlitz-a659ab3bb/",
            "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-python-backend-automation-resume.pdf",
            "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
            "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
            "Message me first when there is one messy sales/support workflow",
            "DriveDesk AI Operator demo GIF",
            "Short visual route: [Demo walkthrough](docs/DEMO_WALKTHROUGH.md)",
            "60-Second Reviewer Snapshot",
            "Hiring relevance",
            "RAG/backend ownership",
            "human-in-the-loop workflow ownership",
            "Fast evaluation path",
        ),
    ),
    ExpectedPin(
        "AlexGerlitz/deploymate",
        ("Platform/DevOps recovery proof", "Docker deployment control panel", "CI/CD", "runbooks"),
        "JavaScript",
        "https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot",
        (
            "devops",
            "devops-recovery",
            "docker",
            "fastapi",
            "postgresql",
            "platform-engineering",
            "backend-development",
            "runbooks",
        ),
        (
            "Self-hosted Docker deployment control panel",
            "Profile / contact route",
            "LinkedIn Recruiter Packet",
            "Decision-Ready Contact",
            "Shortest proof path",
            "https://www.linkedin.com/in/alex-gerlitz-a659ab3bb/",
            "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-python-backend-automation-resume.pdf",
            "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
            "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
            "public DevOps/platform engineering proof surface",
            "Engineering Proof Snapshot",
            "Backend/platform ownership",
            "DevOps/release discipline",
        ),
    ),
    ExpectedPin(
        "AlexGerlitz/AlexGerlitz",
        ("AI Automation", "DriveDesk AI Operator", "LLM workflows", "CRM/ERP integrations", "FastAPI", "Docker"),
        "HTML",
        "https://alexgerlitz.github.io/AlexGerlitz/",
        (
            "ai-automation",
            "backend",
            "crm",
            "devops",
            "drivedesk",
            "erp",
            "llm-workflows",
            "pgvector",
            "rag",
            "systems-integration",
            "vector-databases",
            "workflow-automation",
        ),
        (
            "I build **DriveDesk** and public proof routes around Python/backend automation",
            "Fast public review",
            "Decision Snapshot",
            "DriveDesk AI Operator",
            "pinned proof repos",
        ),
    ),
    ExpectedPin(
        "AlexGerlitz/MPlusForm",
        ("validation-boundary automation proof", "Python sync pipeline", "Windows ops"),
        "Python",
        "https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot",
        (
            "python",
            "validation-boundary",
            "windows-automation",
            "sync-client",
            "business-automation",
            "systems-integration",
            "workflow-automation",
        ),
        (
            "validation-boundary and desktop-automation proof project",
            "Profile / contact route",
            "LinkedIn Recruiter Packet",
            "Decision-Ready Contact",
            "Shortest proof path",
            "https://www.linkedin.com/in/alex-gerlitz-a659ab3bb/",
            "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-python-backend-automation-resume.pdf",
            "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
            "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
            "60-Second Reviewer Snapshot",
            "trust-model",
            "untrusted local files",
            "server-approved snapshot data",
        ),
    ),
)

PROFILE_TEXT = {
    "name": ("Alex Gerlitz",),
    "bio": (
        "Python Backend Automation Engineer",
        "DriveDesk",
        "internal tools",
        "API/CRM integrations",
        "QA Automation Python",
        "RAG",
        "LLM workflows",
        "FastAPI",
        "Docker",
    ),
    "company": ("Autoschool54 / DriveDesk",),
    "location": ("Remote-only",),
    "websiteUrl": ("https://alexgerlitz.github.io/AlexGerlitz/",),
}

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    bio
    company
    location
    websiteUrl
    pinnedItems(first: 6, types: [REPOSITORY]) {
      totalCount
      nodes {
        ... on Repository {
          nameWithOwner
          description
          homepageUrl
          isPrivate
          isArchived
          primaryLanguage {
            name
          }
          repositoryTopics(first: 30) {
            nodes {
              topic {
                name
              }
            }
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


def run_gh_rest(path: str) -> dict:
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI 'gh' is required for pinned repository audit")

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


def fetch_readme_text(name_with_owner: str) -> str:
    payload = run_gh_rest(f"repos/{name_with_owner}/readme")
    encoded = payload.get("content") or ""
    encoding = payload.get("encoding")
    if encoding != "base64" or not encoded:
        raise RuntimeError(f"{name_with_owner}: unexpected README encoding {encoding!r}")
    return base64.b64decode(encoded).decode("utf-8", errors="replace")


def check_pins(payload: dict) -> list[str]:
    errors: list[str] = []
    user = payload["data"]["user"]
    pinned = user["pinnedItems"]
    nodes = pinned["nodes"]

    for field, snippets in PROFILE_TEXT.items():
        value = user.get(field) or ""
        for snippet in snippets:
            if snippet not in value:
                errors.append(f"profile {field}: missing {snippet!r}")

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
        if expected.homepage_url and node.get("homepageUrl") != expected.homepage_url:
            errors.append(
                f"{expected.name_with_owner}: expected homepage {expected.homepage_url!r}, got {node.get('homepageUrl')!r}"
            )
        topics = {
            topic_node["topic"]["name"]
            for topic_node in (node.get("repositoryTopics") or {}).get("nodes", [])
        }
        for topic in expected.topics:
            if topic not in topics:
                errors.append(f"{expected.name_with_owner}: missing topic {topic!r}")
        readme = fetch_readme_text(expected.name_with_owner)
        for snippet in expected.readme_snippets:
            if snippet not in readme:
                errors.append(f"{expected.name_with_owner}: README missing {snippet!r}")

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

    print("github profile metadata audit passed")
    for pin in EXPECTED_PINS:
        print(f"ok pinned: {pin.name_with_owner}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
