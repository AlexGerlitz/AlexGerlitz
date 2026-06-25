#!/usr/bin/env python3
from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TIMEOUT_SECONDS = 20
USER_AGENT = "AlexGerlitz-public-profile-smoke/1.0"
LIVE_RETRY_ATTEMPTS = 6
LIVE_RETRY_DELAY_SECONDS = 10


@dataclass(frozen=True)
class RouteCheck:
    name: str
    url: str
    snippets: tuple[str, ...] = field(default_factory=tuple)
    content_type: str | None = None
    min_bytes: int = 0


ROUTES: tuple[RouteCheck, ...] = (
    RouteCheck(
        "portfolio",
        "https://alexgerlitz.github.io/AlexGerlitz/",
        ("DriveDesk AI Operator", "Start conversation", "pinned proof repos", "Best immediate starts"),
    ),
    RouteCheck(
        "proof-route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        ("DriveDesk AI Operator: backend-owned AI workflow proof", "FastAPI + PostgreSQL", "Profile funnel health"),
    ),
    RouteCheck(
        "ai-operator-case",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-ai-operator.html",
        (
            "DriveDesk AI Operator: AI sales and support workflow platform",
            "RAG + Analysis",
            "Telegram approval flow",
            "CRM adapter",
            "Backend Ownership",
            "Production Proof",
        ),
    ),
    RouteCheck(
        "projects",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        ("Selected Proof Projects", "AI Ops Workflow Kit - RAG"),
    ),
    RouteCheck(
        "role-fit",
        "https://alexgerlitz.github.io/AlexGerlitz/role-fit.html",
        (
            "AI Automation",
            "Backend / Platform",
            "Search-fit role targets",
            "Python Backend Engineer",
            "LLM Workflow / RAG Engineer",
            "n8n AI Workflow Engineer",
        ),
    ),
    RouteCheck(
        "resume",
        "https://alexgerlitz.github.io/AlexGerlitz/resume.html",
        (
            "Role-fit resume",
            "DriveDesk AI Operator proof route",
            "PDF resume",
            "Remote-only backend, platform, DevOps, and AI automation roles.",
        ),
    ),
    RouteCheck(
        "role-fit-pack",
        "https://alexgerlitz.github.io/AlexGerlitz/application-pack.html",
        (
            "Public role fit",
            "AI Automation Engineer",
            "Backend / Platform Engineer",
            "LLM Workflow / RAG Engineer",
            "PDF resume",
        ),
    ),
    RouteCheck(
        "skill-evidence",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/SKILL_EVIDENCE.md",
        (
            "Skill Evidence Matrix",
            "Vector Databases",
            "Systems Integration",
            "Customer Relationship Management (CRM)",
            "Enterprise Resource Planning (ERP)",
        ),
    ),
    RouteCheck(
        "role-targets",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/ROLE_TARGETS.md",
        (
            "Remote Role Targets",
            "Systems Integration Engineer",
            "Customer Relationship Management (CRM) Engineer",
            "Enterprise Resource Planning (ERP) Engineer",
            "Vector Databases Engineer",
        ),
    ),
    RouteCheck(
        "services-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/SERVICES.md",
        (
            "Remote AI Automation Services",
            "remote-only backend, AI automation",
            "DriveDesk AI Operator demo",
            "Remote-only LinkedIn service page",
        ),
    ),
    RouteCheck(
        "first-30-days",
        "https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html",
        ("First Month Delivery Plan", "First 48 Hours", "Week 2"),
    ),
    RouteCheck(
        "fixed-scope-offers",
        "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html",
        ("Fixed-scope AI automation", "Best first step", "USD 3,000-12,000", "USD 25,000+ by phase"),
    ),
    RouteCheck(
        "start-conversation",
        "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
        ("Current Public Proof", "AI Operator case", "Best immediate starts"),
    ),
    RouteCheck(
        "contact-routes",
        "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html",
        (
            "Decision-ready contact routes with PDF resume",
            "Decision-Ready Signals",
            "Best immediate starts",
            "Message on LinkedIn",
            "PDF resume",
            "First month plan",
        ),
    ),
    RouteCheck(
        "verification-pack",
        "https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html",
        ("AI Ops public proof status", "DriveDesk Core"),
    ),
    RouteCheck(
        "resume-pdf",
        "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        content_type="application/pdf",
        min_bytes=100_000,
    ),
    RouteCheck(
        "drivedesk-core-demo",
        "https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/",
        ("DriveDesk", "Operations"),
    ),
    RouteCheck(
        "ai-ops-public-proof-status",
        "https://raw.githubusercontent.com/AlexGerlitz/ai-ops-workflow-kit/main/docs/PUBLIC_PROOF_STATUS.md",
        ("Public Proof Status", "AI Ops Workflow Kit"),
    ),
    RouteCheck(
        "ai-ops-reviewer-acceptance",
        "https://raw.githubusercontent.com/AlexGerlitz/ai-ops-workflow-kit/main/docs/REVIEWER_ACCEPTANCE_REPORT.md",
        ("Reviewer Acceptance Report", "public AI Ops proof surface"),
    ),
    RouteCheck(
        "ai-ops-live-owner-proof",
        "https://raw.githubusercontent.com/AlexGerlitz/ai-ops-workflow-kit/main/docs/LIVE_OWNER_PROOF.md",
        ("Live Owner Proof", "Telegram"),
    ),
)


def fetch(route: RouteCheck) -> tuple[int, str, bytes]:
    request = Request(route.url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        status = response.status
        content_type = response.headers.get("content-type", "")
        body = response.read()
    return status, content_type, body


def check_route(route: RouteCheck) -> list[str]:
    errors: list[str] = []
    try:
        status, content_type, body = fetch(route)
    except HTTPError as exc:
        return [f"{route.name}: HTTP {exc.code} for {route.url}"]
    except URLError as exc:
        return [f"{route.name}: URL error for {route.url}: {exc.reason}"]
    except TimeoutError:
        return [f"{route.name}: timed out after {TIMEOUT_SECONDS}s for {route.url}"]

    if status != 200:
        errors.append(f"{route.name}: expected HTTP 200, got {status}")

    if route.content_type and route.content_type not in content_type:
        errors.append(
            f"{route.name}: expected content-type containing {route.content_type!r}, got {content_type!r}"
        )

    if route.min_bytes and len(body) < route.min_bytes:
        errors.append(f"{route.name}: expected at least {route.min_bytes} bytes, got {len(body)}")

    if route.snippets:
        text = body.decode("utf-8", errors="replace")
        for snippet in route.snippets:
            if snippet not in text:
                errors.append(f"{route.name}: missing snippet {snippet!r}")

    if not errors:
        print(f"ok {route.name}: {route.url}")
    return errors


def has_retryable_pages_lag(errors: list[str]) -> bool:
    return any(
        "alexgerlitz.github.io" in error
        and (
            "missing snippet" in error
            or "HTTP 404" in error
            or "URL error" in error
            or "timed out" in error
        )
        for error in errors
    )


def main() -> int:
    errors: list[str] = []
    for attempt in range(1, LIVE_RETRY_ATTEMPTS + 1):
        errors = []
        for route in ROUTES:
            errors.extend(check_route(route))

        if not errors:
            print("public route smoke passed")
            return 0

        if attempt < LIVE_RETRY_ATTEMPTS and has_retryable_pages_lag(errors):
            print(
                "public route smoke found retryable Pages lag; "
                f"retrying in {LIVE_RETRY_DELAY_SECONDS}s "
                f"({attempt}/{LIVE_RETRY_ATTEMPTS})"
            )
            time.sleep(LIVE_RETRY_DELAY_SECONDS)
            continue

        break

    if errors:
        print("public route smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())
