#!/usr/bin/env python3
from __future__ import annotations

import sys
import struct
import time
from dataclasses import dataclass, field
from html.parser import HTMLParser
import re
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
    social_preview: bool = False
    canonical_url: str | None = None
    pdf_pages: int | None = None
    png_dimensions: tuple[int, int] | None = None
    forbidden_bytes: tuple[bytes, ...] = field(default_factory=tuple)


class SocialPreviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.canonical = ""
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        elif tag == "meta":
            key = values.get("property") or values.get("name")
            content = values.get("content", "")
            if key and content:
                self.meta[key] = content

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def social_preview_errors(route: RouteCheck, text: str) -> list[str]:
    parser = SocialPreviewParser()
    parser.feed(text)
    expected_canonical = route.canonical_url or route.url
    errors: list[str] = []

    if parser.canonical != expected_canonical:
        errors.append(
            f"{route.name}: expected canonical {expected_canonical!r}, got {parser.canonical!r}"
        )

    required_meta = (
        "og:title",
        "og:description",
        "og:url",
        "og:image",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
    )
    for key in required_meta:
        value = parser.meta.get(key, "").strip()
        if not value:
            errors.append(f"{route.name}: missing social preview meta {key!r}")

    og_url = parser.meta.get("og:url", "")
    if og_url != expected_canonical:
        errors.append(f"{route.name}: expected og:url {expected_canonical!r}, got {og_url!r}")

    for key in ("og:image", "twitter:image"):
        image = parser.meta.get(key, "")
        if not image.startswith("https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"):
            errors.append(f"{route.name}: expected {key} to use social-card.png, got {image!r}")

    if parser.meta.get("twitter:card") != "summary_large_image":
        errors.append(
            f"{route.name}: expected twitter:card 'summary_large_image', got {parser.meta.get('twitter:card')!r}"
        )

    return errors


ROUTES: tuple[RouteCheck, ...] = (
    RouteCheck(
        "portfolio",
        "https://alexgerlitz.github.io/AlexGerlitz/",
        (
            "DriveDesk AI Operator",
            "Start conversation",
            "pinned proof repos",
            "Best immediate starts",
            "student/course assignments",
            "generic mobile/ecommerce apps without",
            "case-studies.html",
            "hiring-decision.html",
            "Open technical proof path",
            "skill-evidence.html",
            "services.html",
            "intake-brief.html",
            "Inbound brief",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "hiring-decision",
        "https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html",
        (
            "Hiring Decision - Alex Gerlitz",
            "One-minute hiring decision route",
            "I build backend-owned AI workflow and operations systems for real businesses.",
            "remote-only full-time roles",
            "Best-fit roles",
            "Main proof",
            "Hiring signal",
            "What I can own in the first month",
            "DriveDesk AI Operator",
            "Message on LinkedIn",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "proof-route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        (
            "DriveDesk AI Operator: backend-owned AI workflow proof",
            "FastAPI + PostgreSQL",
            "Remote role decision",
            "Project decision",
            "Technical proof decision",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
            "Profile funnel health",
            "skill-evidence.html",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "featured-drivedesk-alias",
        "https://alexgerlitz.github.io/AlexGerlitz/featured-drivedesk.html",
        (
            "DriveDesk AI Operator proof-route alias",
            'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
            '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
            "This proof-route alias opens",
        ),
    ),
    RouteCheck(
        "one-page-brief-alias",
        "https://alexgerlitz.github.io/AlexGerlitz/one-page-brief.html",
        (
            "DriveDesk AI Operator proof-route alias",
            'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
            '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
            "This proof-route alias opens",
        ),
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
        social_preview=True,
    ),
    RouteCheck(
        "projects",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        ("Selected Proof Projects", "AI Ops Workflow Kit - RAG"),
        social_preview=True,
    ),
    RouteCheck(
        "case-studies",
        "https://alexgerlitz.github.io/AlexGerlitz/case-studies.html",
        (
            "Engineering Case Studies",
            "Problem, build, evidence, and operating proof",
            "DriveDesk / Autoschool54 Operations Platform Direction",
            "AI Ops Workflow Kit",
            "DeployMate",
            "MPlusForm",
            "The operating loop",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "technical-proof",
        "https://alexgerlitz.github.io/AlexGerlitz/proof.html",
        (
            "Proof that can be inspected, not just claimed.",
            "verification-pack.html",
            "start-conversation.html",
            "LinkedIn Services",
            "case-studies.html",
            "Open engineering case studies",
            "After Review",
            "one success condition",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "proof-of-work-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/PROOF_OF_WORK.md",
        (
            "Proof of Work",
            "Fast Proof Review",
            "case-studies.html",
            "Start conversation",
            "Contact routes",
            "LinkedIn Services",
        ),
    ),
    RouteCheck(
        "role-fit",
        "https://alexgerlitz.github.io/AlexGerlitz/role-fit.html",
        (
            "AI Automation",
            "Backend / Platform",
            "Search-fit role targets",
            "skill-evidence.html",
            "Search-match stack",
            "Python Backend Engineer",
            "LLM Workflow / RAG Engineer",
            "n8n AI Workflow Engineer",
        ),
        social_preview=True,
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
        social_preview=True,
    ),
    RouteCheck(
        "role-fit-pack",
        "https://alexgerlitz.github.io/AlexGerlitz/application-pack.html",
        (
            "Public role fit",
            "Search-match stack",
            "skill-evidence.html",
            "AI Automation Engineer",
            "Backend / Platform Engineer",
            "LLM Workflow / RAG Engineer",
            "PDF resume",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "skill-evidence",
        "https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html",
        (
            "Skill-to-proof map",
            "Skills mapped to public proof.",
            "AI Automation / RAG",
            "Backend / Platform",
            "CRM / ERP Integration",
            "DevOps / Self-Hosting",
            "Best Skills To Evaluate",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "skill-evidence-md",
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
        "start-here-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/START_HERE.md",
        (
            "Start Here",
            "Skill Evidence",
            "Inbound Brief",
            "DriveDesk AI Operator proof route",
            "Role Fit Pack",
        ),
    ),
    RouteCheck(
        "services",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        (
            "Remote AI Automation Services - Alex Gerlitz",
            "Business workflows turned into owned backend systems.",
            "Best Immediate Starts",
            "Good Fit Filter",
            "Not my target right now: isolated brochure/static websites",
            "DriveDesk AI Operator Demo",
            "AI Workflow / RAG MVP",
            "CRM / ERP / API Adapter",
            "Proof-Backed Handoff",
            "GitHub-readable services page",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "services-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/SERVICES.md",
        (
            "Remote AI Automation Services",
            "https://alexgerlitz.github.io/AlexGerlitz/services.html",
            "remote-only backend, AI automation",
            "Best-fit request shape: backend-owned state",
            "Not my target right now: isolated brochure/static websites",
            "DriveDesk AI Operator demo",
            "Remote-only LinkedIn service page",
            "skill-evidence.html",
        ),
    ),
    RouteCheck(
        "inbound-brief",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        (
            "Inbound Brief - Alex Gerlitz",
            "Send enough context for a concrete engineering next step.",
            "Best Immediate Starts",
            "Good Fit Filter",
            "Not my target right now: onsite-only roles",
            "Remote Role",
            "Fixed-Scope Project",
            "Technical Review",
            "What I Send Back",
            "The smallest responsible first slice.",
            "GitHub-readable inbound brief",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "inbound-brief-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/INTAKE_BRIEF.md",
        (
            "Inbound Brief",
            "Best immediate starts",
            "Start conversation",
            "Contact routes",
            "LinkedIn Services",
            "student/course assignments",
            "generic mobile/ecommerce apps without",
            "For A Role",
            "For A Fixed-Scope Project",
        ),
    ),
    RouteCheck(
        "first-30-days",
        "https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html",
        ("First Month Delivery Plan", "First 48 Hours", "Week 2"),
        social_preview=True,
    ),
    RouteCheck(
        "fixed-scope-offers",
        "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html",
        ("Fixed-scope AI automation", "services.html", "Best first step", "USD 3,000-12,000", "USD 25,000+ by phase"),
        social_preview=True,
    ),
    RouteCheck(
        "start-conversation",
        "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
        (
            "Current Public Proof",
            "AI Operator case",
            "skill-evidence.html",
            "Open skill evidence",
            "intake-brief.html",
            "Inbound brief",
            "Best immediate starts",
            "Fast Decision Prompts",
            "whether a practical first slice can ship quickly",
            "student/course assignments",
            "Generic mobile/ecommerce apps without backend/integration ownership",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "contact-routes",
        "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html",
        (
            "Contact route for remote roles, fixed-scope projects, and proof reviews",
            "Send one role, workflow, or proof question",
            "Decision-Ready Signals",
            "Fast Decision Prompts",
            "which technical claim or risk should be validated",
            "Best immediate starts",
            "Message on LinkedIn",
            "skill-evidence.html",
            "Skill evidence",
            "intake-brief.html",
            "Inbound brief",
            "PDF resume",
            "First month plan",
            "Response Shape",
            "concrete next step instead of a generic intro call",
            "Smallest responsible working slice",
            "Claim-to-evidence map",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "contact-routes-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/INBOUND_RESPONSE_PACK.md",
        (
            "Contact Routes",
            "Fast fit checklist:",
            "student/course assignments",
            "generic mobile/ecommerce apps without",
            "with no way to verify success",
            "Fast Decision Prompts",
            "DriveDesk Proof Route",
        ),
    ),
    RouteCheck(
        "work-with-me-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/WORK_WITH_ME.md",
        (
            "Work With Me",
            "Fast fit checklist: remote-only work",
            "student/course assignments",
            "generic mobile/ecommerce apps without backend/integration ownership",
            "Workflow Teardown + Working Slice",
            "Integration Adapter",
        ),
    ),
    RouteCheck(
        "role-project-brief-md",
        "https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/main/ROLE_PROJECT_BRIEF.md",
        (
            "Role / Project Brief",
            "Remote AI automation, backend/platform and DevOps engineer building DriveDesk",
            "Not My Target",
            "Student/course assignments",
            "Generic mobile/ecommerce apps without backend/integration ownership",
            "AI Ops Workflow Kit reviewer snapshot",
        ),
    ),
    RouteCheck(
        "verification-pack",
        "https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html",
        ("Last checked: 2026-06-27.", "AI Ops public proof status", "DriveDesk Core"),
    ),
    RouteCheck(
        "resume-pdf",
        "https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        content_type="application/pdf",
        min_bytes=100_000,
        pdf_pages=1,
        forbidden_bytes=(
            b"file://",
            b"Users/alexgerlitz",
            b"Documents/Codex",
            b"new-chat",
            b"AI-generated",
            b"One-Page Brief",
        ),
    ),
    RouteCheck(
        "social-card-image",
        "https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route",
        content_type="image/png",
        min_bytes=10_000,
        png_dimensions=(1200, 630),
    ),
    RouteCheck(
        "linkedin-banner-image",
        "https://alexgerlitz.github.io/AlexGerlitz/assets/linkedin-banner.png",
        content_type="image/png",
        min_bytes=10_000,
        png_dimensions=(1584, 396),
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

    if route.pdf_pages is not None:
        if not body.startswith(b"%PDF-"):
            errors.append(f"{route.name}: missing PDF header for {route.url}")
        page_count = len(re.findall(rb"/Type\s*/Page\b", body))
        if page_count != route.pdf_pages:
            errors.append(f"{route.name}: expected {route.pdf_pages} PDF page(s), got {page_count}")

    if route.png_dimensions is not None:
        if not body.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append(f"{route.name}: missing PNG header for {route.url}")
        elif len(body) < 24 or body[12:16] != b"IHDR":
            errors.append(f"{route.name}: missing PNG IHDR for {route.url}")
        else:
            dimensions = struct.unpack(">II", body[16:24])
            if dimensions != route.png_dimensions:
                errors.append(
                    f"{route.name}: expected PNG dimensions {route.png_dimensions}, got {dimensions}"
                )

    for marker in route.forbidden_bytes:
        if marker in body:
            errors.append(
                f"{route.name}: forbidden byte marker {marker.decode('utf-8', 'replace')!r}"
            )

    if route.snippets:
        text = body.decode("utf-8", errors="replace")
        for snippet in route.snippets:
            if snippet not in text:
                errors.append(f"{route.name}: missing snippet {snippet!r} for {route.url}")

    if route.social_preview:
        text = body.decode("utf-8", errors="replace")
        errors.extend(social_preview_errors(route, text))

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
