#!/usr/bin/env python3
from __future__ import annotations

import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".html", ".md", ".svg", ".xml", ".txt"}
SKIP_DIRS = {".git", "tmp", "output"}
README_MAX_LINES = 80


def marker(*parts: str) -> str:
    return "".join(parts)


LEGACY_PROOF_ROUTE = marker("featured", "-drivedesk.html")
LEGACY_PROOF_ROUTE_ALLOWED = {
    LEGACY_PROOF_ROUTE,
}
DEPLOYMATE_LEGACY_ANCHOR = "deploymate#reviewer-package"


BAD_FILENAMES = {
    marker("hiring", "-screen.html"),
}

BAD_PATTERNS = [
    marker(r"Forwardable", r" summary"),
    marker(r"first", r"-message"),
    marker(r"first", r" message template"),
    marker(r"technical", r" screening"),
    marker(r"Hiring", r" Screen"),
    r"Useful Contact Context",
    r"What To Send",
    r"Current workflow:",
    r"Systems involved:",
    r"Data sources:",
    r"Budget range:",
    marker(r"AI", r"/Codex"),
    marker(r"AI", r"-generated"),
    marker(r"Chat", r"GPT"),
    marker(r"generated", r" by"),
    marker(r"building", r" toward"),
    marker(r"inter", r"view"),
    marker(r"со", r"бес"),
    marker(r"Alex Gerlitz", r" is"),
    marker(r"This", r" candidate"),
    marker(r"the", r" candidate"),
]

REQUIRED_FILES = [
    "README.md",
    "index.html",
    "drivedesk-proof-route.html",
    "drivedesk-ai-operator.html",
    "projects.html",
    "first-30-days.html",
    "fixed-scope-offers.html",
    "inbound-response.html",
    "one-page-brief.html",
    "resume.html",
    "resume-pdf.html",
    "application-pack.html",
    "START_HERE.md",
    "APPLICATION_PACK.md",
    "RESUME.md",
    "SKILL_EVIDENCE.md",
    "ROLE_TARGETS.md",
    "AI_AUTOMATION_ROLE_FIT.md",
    "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    "assets/social-card.png",
    "assets/social-card.svg",
    "assets/favicon.svg",
    "sitemap.xml",
    "robots.txt",
]

REQUIRED_TEXT = {
    "README.md": [
        "actions/workflows/profile-audit.yml/badge.svg?branch=main",
        "actions/workflows/live-profile-smoke.yml/badge.svg?branch=main",
        "DriveDesk Proof Route",
        "pinned proof repos",
        "Live owner proof",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "remote-only full-time roles",
        "first month plan",
        "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html",
    ],
    "index.html": [
        '<link rel="icon" href="./assets/favicon.svg" type="image/svg+xml">',
        "./drivedesk-proof-route.html",
        "./projects.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "DriveDesk proof route",
        "DriveDesk AI Operator",
        "Live owner proof",
        "Live route smoke",
        "pinned proof repos",
        "First month plan",
    ],
    "role-fit.html": [
        "AI Ops proof status",
        "Live owner proof",
        "AI Ops CI workflow",
        "Search-fit role targets",
        "Python Backend Engineer",
        "LLM Workflow / RAG Engineer",
        "n8n AI Workflow Engineer",
        "./ROLE_TARGETS.md",
    ],
    "resume.html": [
        "<title>Resume - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/resume.html"',
        "DriveDesk AI Operator proof route",
        "PDF resume",
        "Remote-only backend, platform, DevOps, and AI automation roles.",
        "CRM, ERP, 1C, accounting, banking, webhook, and API integration adapters.",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "Vector Databases",
    ],
    "application-pack.html": [
        "<title>Role Fit Pack - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/application-pack.html"',
        "Remote AI automation, backend/platform, integration, and DevOps work.",
        "AI Automation Engineer",
        "Backend / Platform Engineer",
        "LLM Workflow / RAG Engineer",
        "PDF resume",
    ],
    "START_HERE.md": [
        "2-minute decision route",
        "DriveDesk AI Operator proof route",
        "LinkedIn Services",
        "Role Fit Pack",
        "PDF Resume",
    ],
    "APPLICATION_PACK.md": [
        "Role Fit Pack",
        "AI Automation Engineer",
        "Backend / Platform Engineer",
        "LLM Workflow / RAG Engineer",
        "PDF resume",
    ],
    "RESUME.md": [
        "Remote-only AI automation, backend/platform, and DevOps engineer",
        "PDF resume for application upload",
        "AI Automation Engineer",
        "Integration Engineer",
        "Remote Role Targets",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "vector",
    ],
    "SKILL_EVIDENCE.md": [
        "Skill Evidence Matrix",
        "Vector Databases",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
    ],
    "ROLE_TARGETS.md": [
        "Remote Role Targets",
        "Systems Integration Engineer",
        "Customer Relationship Management (CRM) Engineer",
        "Enterprise Resource Planning (ERP) Engineer",
        "Vector Databases Engineer",
    ],
    "AI_AUTOMATION_ROLE_FIT.md": [
        "AI Automation Role Fit",
        "Vector Databases",
        "pgvector-ready storage",
        "CRM / Bitrix / API handoff",
    ],
    "start-conversation.html": [
        "Current Public Proof",
        "Live owner proof",
        "AI Operator case",
        "First month plan",
    ],
    "inbound-response.html": [
        "<title>Contact Routes - Alex Gerlitz</title>",
        "Decision-ready contact routes with PDF resume",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html"',
        "Decision-Ready Signals",
        "Message on LinkedIn",
        "PDF resume",
        "First month plan",
        "DriveDesk AI Operator proof route",
    ],
    "drivedesk-ai-operator.html": [
        "Live owner proof",
        "Open public proof status",
        "Open CI workflow",
    ],
    "projects.html": [
        "<title>Selected Proof Projects - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/projects.html"',
        "DriveDesk AI Operator / AI Sales & Support Workflow Platform",
        "DriveDesk Core - Operations & Integration Platform",
        "AI Ops Workflow Kit - RAG, Transcript Analysis, Approval & CRM Handoff",
        "DeployMate - Self-hosted Docker Deployment Control Panel",
    ],
    "AI_AUTOMATION_ROLE_FIT.md": [
        "Live owner proof",
        "Live Telegram approval evidence",
        "AI Ops CI workflow",
    ],
    "drivedesk-proof-route.html": [
        "<title>DriveDesk AI Operator - Proof Route</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "Clean public proof route",
        "Profile funnel health",
        "First month plan",
    ],
    "first-30-days.html": [
        "<title>First Month Delivery Plan - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "First 48 Hours",
        "Week 2",
        "What I Need To Start",
    ],
    "fixed-scope-offers.html": [
        "backed by DriveDesk AI Operator proof",
        "./drivedesk-proof-route.html",
        "Open DriveDesk proof route",
        "Best first step",
        "Workflow Teardown + Working Slice",
        "USD 3,000-12,000",
        "USD 25,000+ by phase",
    ],
    "one-page-brief.html": [
        "DriveDesk AI Operator - Proof Route",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "strongest public proof route",
    ],
    "featured-drivedesk.html": [
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "The current proof route",
    ],
    "ONE_PAGE_BRIEF.md": [
        "legacy markdown route",
        "DriveDesk AI Operator proof route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
    ],
    "resume-pdf.html": [
        "Proof route: alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "building DriveDesk AI Operator proof",
        "fixed-scope automation",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "vector databases",
    ],
    "assets/social-card.svg": [
        "DriveDesk AI Operator - Proof Route",
        "Backend-owned AI workflow proof",
        "Documents + transcripts / RAG + citations / scoring / approvals / CRM handoff",
    ],
    "sitemap.xml": [
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
    ],
}

SOCIAL_PREVIEW_PAGES = [
    "index.html",
    "drivedesk-proof-route.html",
    "projects.html",
    "role-fit.html",
    "fixed-scope-offers.html",
    "start-conversation.html",
    "resume.html",
    "application-pack.html",
    "first-30-days.html",
    "inbound-response.html",
]

SOCIAL_PREVIEW_SNIPPETS = [
    'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"',
    'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"',
    'property="og:image:type" content="image/png"',
    'property="og:image:width" content="1200"',
    'property="og:image:height" content="630"',
    'property="og:image:alt"',
    'name="twitter:card" content="summary_large_image"',
    'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"',
    'name="twitter:image:alt"',
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.links.append((attr, value))


def iter_public_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).exists():
            errors.append(f"missing required file: {relative}")


def check_bad_filenames(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.name in BAD_FILENAMES:
            errors.append(f"{relative}: weak public filename")


def check_bad_patterns(errors: list[str]) -> None:
    compiled = [(pattern, re.compile(pattern, re.IGNORECASE)) for pattern in BAD_PATTERNS]
    for path in iter_public_text_files():
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "grid-template" in line:
                continue
            for label, regex in compiled:
                if regex.search(line):
                    errors.append(f"{relative}:{line_no}: weak public wording: {label}")


def check_legacy_proof_route_references(errors: list[str]) -> None:
    for path in iter_public_text_files():
        relative = str(path.relative_to(ROOT))
        if relative in LEGACY_PROOF_ROUTE_ALLOWED:
            continue
        text = path.read_text(encoding="utf-8")
        if LEGACY_PROOF_ROUTE in text:
            errors.append(f"{relative}: use drivedesk-proof-route.html instead of legacy proof route")
        if relative != "one-page-brief.html" and "one-page-brief.html" in text:
            errors.append(f"{relative}: use drivedesk-proof-route.html instead of one-page brief route")
        if relative != "ONE_PAGE_BRIEF.md" and "ONE_PAGE_BRIEF.md" in text:
            errors.append(f"{relative}: use drivedesk-proof-route.html instead of ONE_PAGE_BRIEF.md")
        if DEPLOYMATE_LEGACY_ANCHOR in text:
            errors.append(f"{relative}: use deploymate#engineering-proof-snapshot instead of legacy DeployMate anchor")


def check_required_text(errors: list[str]) -> None:
    for relative, snippets in REQUIRED_TEXT.items():
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative}: missing required text: {snippet}")


def check_social_preview_metadata(errors: list[str]) -> None:
    for relative in SOCIAL_PREVIEW_PAGES:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing social preview page: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in SOCIAL_PREVIEW_SNIPPETS:
            if snippet not in text:
                errors.append(f"{relative}: missing social preview metadata: {snippet}")


def check_profile_readme_shape(errors: list[str]) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        return
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    if line_count > README_MAX_LINES:
        errors.append(f"README.md: expected at most {README_MAX_LINES} lines for profile overview, got {line_count}")


def check_local_html_links(errors: list[str]) -> None:
    for path in sorted(ROOT.glob("*.html")):
        parser = LinkParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for attr, value in parser.links:
            if value.startswith(("#", "mailto:", "tel:", "http://", "https://", "data:")):
                continue
            local = value.split("#", 1)[0].split("?", 1)[0]
            if not local:
                continue
            target = (path.parent / unquote(local)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if not target.exists():
                errors.append(f"{path.name}: missing local {attr} target: {value}")


def check_png_size(errors: list[str]) -> None:
    path = ROOT / "assets/social-card.png"
    if not path.exists():
        return
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append("assets/social-card.png: not a PNG")
        return
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1200, 630):
        errors.append(f"assets/social-card.png: expected 1200x630, got {width}x{height}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_bad_filenames(errors)
    check_bad_patterns(errors)
    check_legacy_proof_route_references(errors)
    check_required_text(errors)
    check_social_preview_metadata(errors)
    check_profile_readme_shape(errors)
    check_local_html_links(errors)
    check_png_size(errors)

    if errors:
        print("public profile audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("public profile audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
