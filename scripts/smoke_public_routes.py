#!/usr/bin/env python3
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TIMEOUT_SECONDS = 20
USER_AGENT = "AlexGerlitz-public-profile-smoke/1.0"


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
        ("DriveDesk AI Operator", "Start conversation"),
    ),
    RouteCheck(
        "proof-route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        ("DriveDesk AI Operator: backend-owned AI workflow proof", "FastAPI + PostgreSQL"),
    ),
    RouteCheck(
        "projects",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        ("Selected Proof Projects", "AI Ops Workflow Kit - RAG"),
    ),
    RouteCheck(
        "role-fit",
        "https://alexgerlitz.github.io/AlexGerlitz/role-fit.html",
        ("AI Automation", "Backend / Platform"),
    ),
    RouteCheck(
        "fixed-scope-offers",
        "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html",
        ("Fixed-scope AI automation", "DriveDesk AI Operator Demo"),
    ),
    RouteCheck(
        "start-conversation",
        "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
        ("Current Public Proof", "AI Operator case"),
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


def main() -> int:
    errors: list[str] = []
    for route in ROUTES:
        errors.extend(check_route(route))

    if errors:
        print("public route smoke failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("public route smoke passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
