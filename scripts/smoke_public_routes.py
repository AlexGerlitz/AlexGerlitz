#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
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


def current_profile_ref() -> str:
    github_sha = os.environ.get("GITHUB_SHA", "").strip()
    if github_sha:
        return github_sha
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "main"
    return result.stdout.strip() or "main"


PROFILE_RAW_REF = current_profile_ref()


def profile_raw_url(path: str) -> str:
    return f"https://raw.githubusercontent.com/AlexGerlitz/AlexGerlitz/{PROFILE_RAW_REF}/{path}"


@dataclass(frozen=True)
class RouteCheck:
    name: str
    url: str
    snippets: tuple[str, ...] = field(default_factory=tuple)
    content_type: str | None = None
    min_bytes: int = 0
    social_preview: bool = False
    social_image_prefix: str = "https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png"
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
        if not image.startswith(route.social_image_prefix):
            errors.append(f"{route.name}: expected {key} to use {route.social_image_prefix}, got {image!r}")

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
            "Recruiter shortcut / 30-second screen",
            "LinkedIn recruiter packet",
            "linkedin-recruiter-packet.html",
            "Recruiter preferences",
            "recruiter-preferences.html",
            "Decision-ready contact",
            "decision-ready-contact.html",
            "AI backend proof pack",
            "ai-backend-proof-pack.html",
            "Enterprise readiness",
            "enterprise-readiness.html",
            "start-conversation.html",
            "role-targets.html",
            "skill-evidence.html",
            "Best match: backend/platform, AI automation, CRM/ERP/API integration, internal tools, or DevOps ownership.",
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
        "linkedin-recruiter-packet",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html",
        (
            "LinkedIn Recruiter Packet - Alex Gerlitz",
            "Fast route from profile view to technical decision.",
            "LinkedIn recruiter packet",
            "Job Title Filters",
            "Skill Filters",
            "Work Mode",
            "First Result",
            "International team fit comes through English-first docs, async proof routes, integration contracts, privacy boundaries, CI, runbooks, and operational handoff quality.",
            "What To Open First",
            "Enterprise Readiness",
            "First Message Shape",
            "Message on LinkedIn",
            "hiring-decision.html",
            "ai-backend-proof-pack.html",
            "enterprise-readiness.html",
            "verification-pack.html",
            "start-conversation.html",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        ),
        social_preview=True,
        social_image_prefix="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png",
    ),
    RouteCheck(
        "recruiter-preferences",
        "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
        (
            "Recruiter Preferences - Alex Gerlitz",
            "Open-to-Work alignment",
            "Recruiter preferences for remote backend, AI automation, integrations, and DevOps work.",
            "Open-To-Work Preference Set",
            "Job titles",
            "Location type",
            "Remote locations",
            "Employment types",
            "Recruiter Search Keywords",
            "First Contact Fit",
            "Best First Outcome",
            "Proof Map",
            "Not My Target",
            "International remote teams, Europe-compatible remote teams, US-compatible async teams, and distributed product/operations teams.",
            "Open to remote full-time roles and concrete fixed-scope projects.",
            "Message on LinkedIn",
            "linkedin-recruiter-packet.html",
            "hiring-decision.html",
            "ai-backend-proof-pack.html",
            "enterprise-readiness.html",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        ),
        social_preview=True,
        social_image_prefix="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png",
    ),
    RouteCheck(
        "decision-ready-contact",
        "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html",
        (
            "Decision-Ready Contact - Alex Gerlitz",
            "Decision-ready contact",
            "Turn a profile view into a concrete next step.",
            "fit read, risk check, smallest responsible first slice, proof route, and next step",
            "Remote Role",
            "Workflow / Integration",
            "Technical Proof Review",
            "Fixed-Scope Project",
            "What I Send Back",
            "Best First Links",
            "Fast Fit",
            "Message on LinkedIn",
            "linkedin-recruiter-packet.html",
            "recruiter-preferences.html",
            "hiring-decision.html",
            "drivedesk-proof-route.html",
            "ai-backend-proof-pack.html",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        ),
        social_preview=True,
        social_image_prefix="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png",
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
            "30-Second Screening Answer",
            "Strong match: remote backend/platform, AI workflow, CRM/ERP/API integration, internal tools, or DevOps reliability work.",
            "Open first: AI Backend Proof Pack",
            "Expected first result: one working slice with backend-owned state, tests, logs, docs, demo path, and handoff route.",
            "Message trigger: one role or workflow, one success condition, systems involved, ownership boundary, and timeline.",
            "What I can own in the first month",
            "DriveDesk AI Operator",
            "Message on LinkedIn",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "ai-readable-proof-index",
        "https://alexgerlitz.github.io/AlexGerlitz/llms.txt",
        (
            "# Alex Gerlitz - AI Automation / Backend / Platform Engineer",
            "I build backend-owned AI workflow and operations systems for real businesses",
            "DriveDesk AI Operator proof route",
            "AI Backend Proof Pack",
            "compact route through AI workflow, backend/platform, integration, DevOps, live proof, verification, and resume evidence",
            "Enterprise Readiness",
            "international employer-grade review route for architecture, state ownership, integration contracts, English-first docs, async proof paths, reliability, privacy, observability, CI, runbooks, and handoff quality",
            "DriveDesk Flagship Platform",
            "Hiring decision route",
            "LinkedIn Recruiter Packet",
            "search filters, 30-second fit, proof order, expected first result, first message context, and international remote-team proof routing",
            "Recruiter Preferences",
            "Open-to-Work alignment for job titles, remote work mode, employment types, recruiter search keywords, proof order, and first contact fit.",
            "Decision-Ready Contact",
            "minimum first context, fit read, risk check, smallest responsible first slice, proof route, and next step.",
            "Start conversation",
            "recruiter shortcut, role-target links, PDF resume, proof route, and the fastest contact path",
            "Selected proof projects",
            "DriveDesk Core, AI Ops Workflow Kit, DeployMate, and MPlusForm",
            "Skill evidence map",
            "Verification pack",
            "AI Backend Proof Pack Markdown",
            "Enterprise Readiness Markdown",
            "Search-Fit Role Targets",
            "LinkedIn recruiter search alignment",
            "Python, FastAPI, PostgreSQL, Docker, GitHub Actions, RAG, Vector Databases",
            "LLM Workflow / RAG Engineer",
            "remote-only full-time roles or concrete fixed-scope projects",
            "First-month ownership",
            "backend-owned AI workflows, CRM/ERP/API adapters",
            "Recruiter shortcut: for a remote role, start with LinkedIn Recruiter Packet, Recruiter Preferences, Hiring decision route, Remote role targets, Skill evidence, and the PDF resume.",
            "Best match: backend/platform, AI automation, CRM/ERP/API integration, internal tools, or DevOps ownership.",
            "validation-boundary and trust-model automation proof",
            "LinkedIn Services",
            "The main signal is not no-code node wiring.",
        ),
        content_type="text/plain",
        min_bytes=2000,
    ),
    RouteCheck(
        "proof-route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        (
            "DriveDesk AI Operator: backend-owned AI workflow proof",
            "FastAPI + PostgreSQL",
            '"@type": "ProfilePage"',
            '"jobTitle": "AI Automation / Backend / Platform Engineer"',
            '"Transcript analysis"',
            '"name": "Start conversation"',
            "Message on LinkedIn",
            "AI backend proof pack",
            "AI Backend Proof Pack",
            "compact route through AI workflow, backend/platform, integration, DevOps, live proof, and resume evidence",
            "Remote role signal",
            "Workflow project signal",
            "DriveDesk proof route",
            "Enterprise readiness",
            "international remote-team review of architecture, state, integration contracts, reliability, privacy, CI, runbooks, and handoff quality",
            "Useful first outcome: working slice with tests, docs, and handoff.",
            "Remote role decision",
            "Project decision",
            "Technical proof decision",
            "public runtime runs with `storage=postgres`",
            "restart persistence",
            "RAG quality eval",
            "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
            "Profile funnel health",
            "skill-evidence.html",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "ai-backend-proof-pack",
        "https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html",
        (
            "AI Backend Proof Pack - Alex Gerlitz",
            "Featured proof pack",
            "AI workflow and backend/platform proof in one route.",
            "The core signal: I do not just connect workflow nodes.",
            "FastAPI/PostgreSQL",
            "RAG and transcripts",
            "CRM/ERP adapters",
            "Role Shortlist",
            "Backend / Platform Engineer",
            "AI Automation / RAG Engineer",
            "Integration Engineer",
            "DevOps / Self-Hosting Engineer",
            "Internal Tools Engineer",
            "Technical Proof Review",
            "First result: one backend slice with contract, tests, docs, and deployment path.",
            "First result: claim-to-evidence map, risks, smallest responsible slice, and verification route.",
            "Proof Order",
            "DriveDesk Proof Route",
            "Enterprise Readiness",
            "AI Ops live owner proof",
            "Live PostgreSQL/pgvector proof",
            "Verification Pack",
            "PDF Resume",
            "Role Shortlist",
            "Backend / Platform Engineer",
            "AI Automation / RAG Engineer",
            "Integration Engineer",
            "DevOps / Self-Hosting Engineer",
            "Internal Tools Engineer",
            "Technical Proof Review",
            "claim-to-evidence map, risks, smallest responsible slice, and verification route.",
            "Strong Match",
            "Useful First Context",
            "Why This Is Different",
            "Message on LinkedIn",
            "drivedesk-proof-route.html",
            "enterprise-readiness.html",
            "verification-pack.html",
        ),
        social_preview=True,
        social_image_prefix="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png",
    ),
    RouteCheck(
        "ai-backend-proof-pack-md",
        profile_raw_url("AI_BACKEND_PROOF_PACK.md"),
        (
            "AI Backend Proof Pack",
            "I do not just connect workflow nodes.",
            "DriveDesk Proof Route",
            "Enterprise Readiness",
            "AI Ops live owner proof",
            "Live PostgreSQL/pgvector proof",
            "Verification Pack",
            "PDF Resume",
            "Strong Match",
            "Useful First Context",
        ),
    ),
    RouteCheck(
        "enterprise-readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        (
            "Enterprise Readiness - Alex Gerlitz",
            "Proof for teams that need a reliable backend/platform owner.",
            "AI backend proof pack",
            "ai-backend-proof-pack.html",
            "international employer-grade team can inspect",
            "architecture, state ownership, integration contracts, reliability, privacy, observability, CI, runbooks, and handoff quality",
            "International Employer Signals",
            "Qualification depth: backend/platform work, AI workflow engineering, CRM/ERP/API integration, DevOps, and support of real business infrastructure are tied to public proof.",
            "Enterprise constraints: privacy boundaries, approvals, audit trail, retries, idempotency, rollback thinking, and runbooks are visible instead of hidden behind workflow glue.",
            "Async review quality: English-first docs, proof routes, CI, smoke checks, and compact evidence make it possible to evaluate work across time zones.",
            "English-first docs",
            "Async review path",
            "Evidence Matrix",
            "Backend/platform ownership",
            "AI workflow engineering",
            "Privacy and integration discipline",
            "International team fit",
            "llms.txt",
            "async review paths",
            "smallest responsible first slice instead of vague AI automation claims",
            "Remote review clarity",
            "Not Just No-Code Glue",
            "Next Stronger Proof",
            "drivedesk-proof-route.html",
            "verification-pack.html",
            "start-conversation.html",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "enterprise-readiness-md",
        profile_raw_url("ENTERPRISE_READINESS.md"),
        (
            "Enterprise Readiness",
            "international employer-grade review",
            "International Employer Signals",
            "Qualification depth",
            "Enterprise constraints",
            "Async review quality",
            "Backend/platform ownership",
            "AI workflow engineering",
            "Reliability and operations",
            "Privacy and integration discipline",
            "International team fit",
            "English-first docs",
            "async review paths",
            "Handoff discipline",
            "I use AI tooling to move faster",
            "n8n can orchestrate events, while backend code owns state",
            "Next Stronger Proof",
        ),
    ),
    RouteCheck(
        "flagship-platform",
        "https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html",
        (
            "DriveDesk Flagship Platform",
            "DriveDesk AI Operator",
            "Core Backend",
            "Integration Layer",
            "AI Operator Layer",
            "DevOps Layer",
            "Business Outcome",
            "How I Would Start",
            "DriveDesk Core",
            "AI Ops Workflow Kit",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "featured-drivedesk-entry",
        "https://alexgerlitz.github.io/AlexGerlitz/featured-drivedesk.html",
        (
            "DriveDesk AI Operator proof route",
            'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
            '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
            "Open the current proof route",
            "backend-owned AI workflows, RAG, transcript analysis, approvals",
        ),
    ),
    RouteCheck(
        "one-page-brief-entry",
        "https://alexgerlitz.github.io/AlexGerlitz/one-page-brief.html",
        (
            "DriveDesk AI Operator proof route",
            'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
            '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
            "Open the current proof route",
            "backend-owned AI workflows, RAG, transcript analysis, approvals",
        ),
    ),
    RouteCheck(
        "ai-operator-case",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-ai-operator.html",
        (
            "DriveDesk AI Operator: AI sales and support workflow platform",
            "RAG + Analysis",
            "deterministic RAG quality eval with citations",
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
        (
            "Selected Proof Projects",
            "AI Ops Workflow Kit - RAG",
            "RAG eval 2/2",
            "MPlusForm - Validation Boundary / Desktop Automation Proof",
            "Public verification workflow",
        ),
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
            "RAG retrieval with quality eval",
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
        profile_raw_url("PROOF_OF_WORK.md"),
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
            "role-targets.html",
            "skill-evidence.html",
            "Search-match stack",
            "Python Backend Engineer",
            "LLM Workflow / RAG Engineer",
            "n8n AI Workflow Engineer",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "role-targets",
        "https://alexgerlitz.github.io/AlexGerlitz/role-targets.html",
        (
            "Remote Role Targets - Alex Gerlitz",
            "Search-fit roles mapped to proof.",
            '"@type": "ProfilePage"',
            '"@type": "Person"',
            '"@type": "ItemList"',
            '"jobTitle": "AI Automation / Backend / Platform Engineer"',
            '"knowsAbout"',
            "Remote Backend Engineer",
            "Back End Developer",
            "Python Developer",
            "Python Backend Engineer",
            "AI Automation Engineer",
            "Artificial Intelligence Engineer",
            "LLM Workflow Engineer",
            "RAG Workflow Engineer",
            "Backend Development",
            "Platform Engineering",
            "Workflow Automation",
            "Systems Integration",
            "CRM / ERP Integrations",
            "Docker Compose",
            "GitHub Actions",
            "Recruiter Search Snapshot",
            "LinkedIn Recruiter Search Alignment",
            "Job title filters",
            "Work mode",
            "Skill filters",
            "First proof route",
            "Back End Developer, Python Developer, AI Automation Engineer, Artificial Intelligence Engineer, Platform Engineer, DevOps Engineer, Integration Engineer.",
            "Python, FastAPI, PostgreSQL, Docker, GitHub Actions, RAG, Vector Databases, CRM, ERP, Systems Integration, API Integration, n8n, Telegram, DevOps, OpenAPI, pgvector.",
            "First message trigger: send one remote role or one business workflow",
            "AI / LLM Workflows",
            "Integration Engineer",
            "DevOps Engineer",
            "First Month Ownership",
            "Not My Current Target",
            "GitHub-readable version",
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
            "RAG retrieval with deterministic quality eval",
            "Backend / Platform",
            "CRM / ERP Integration",
            "DevOps / Self-Hosting",
            "Best Skills To Evaluate",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "skill-evidence-md",
        profile_raw_url("SKILL_EVIDENCE.md"),
        (
            "Skill Evidence Matrix",
            "Vector Databases",
            "deterministic RAG quality eval",
            "Systems Integration",
            "Customer Relationship Management (CRM)",
            "Enterprise Resource Planning (ERP)",
        ),
    ),
    RouteCheck(
        "role-targets",
        profile_raw_url("ROLE_TARGETS.md"),
        (
            "Remote Role Targets",
            "Recruiter Search Snapshot",
            "LinkedIn Recruiter Search Alignment",
            "Job title filters",
            "Skill filters",
            "First message trigger",
            "Systems Integration Engineer",
            "AI Automation / Backend / Platform Engineer",
            "Backend Development",
            "Platform Engineering",
            "Workflow Automation",
            "CRM / ERP Integrations",
            "Customer Relationship Management (CRM) Engineer",
            "Enterprise Resource Planning (ERP) Engineer",
            "Vector Databases Engineer",
        ),
    ),
    RouteCheck(
        "start-here-md",
        profile_raw_url("START_HERE.md"),
        (
            "Start Here",
            "LinkedIn Recruiter Packet",
            "Recruiter Preferences",
            "Decision-Ready Contact",
            "Skill Evidence",
            "Inbound Brief",
            "AI Backend Proof Pack",
            "AI_BACKEND_PROOF_PACK.md",
            "Enterprise Readiness",
            "ENTERPRISE_READINESS.md",
            "DriveDesk AI Operator proof route",
            "Role Fit Pack",
            "Fast Decision Signals",
            "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
            "useful first outcome: working slice with tests, docs, and handoff.",
            "linkedin-recruiter-packet.html",
            "recruiter-preferences.html",
            "decision-ready-contact.html",
        ),
    ),
    RouteCheck(
        "decision-ready-contact-md",
        profile_raw_url("DECISION_READY_CONTACT.md"),
        (
            "Decision-Ready Contact",
            "Send This Minimum Context",
            "Remote role",
            "Workflow / integration",
            "Technical proof review",
            "Fixed-scope project",
            "What I Send Back",
            "Fit read",
            "Risk check",
            "First slice",
            "Proof route",
            "Next step",
            "Best First Links",
            "Fast Fit",
        ),
    ),
    RouteCheck(
        "recruiter-preferences-md",
        profile_raw_url("RECRUITER_PREFERENCES.md"),
        (
            "Recruiter Preferences",
            "Open-To-Work Preference Set",
            "Job titles",
            "Location type",
            "Remote locations",
            "Employment types",
            "Recruiter Search Keywords",
            "International remote teams, Europe-compatible remote teams, US-compatible async teams, and distributed product/operations teams.",
            "Open to remote full-time roles and concrete fixed-scope projects.",
            "Proof Map",
            "First Contact Fit",
            "Not My Target",
        ),
    ),
    RouteCheck(
        "linkedin-recruiter-packet-md",
        profile_raw_url("LINKEDIN_RECRUITER_PACKET.md"),
        (
            "LinkedIn Recruiter Packet",
            "30-Second Fit",
            "Search Alignment",
            "Job title filters",
            "Skill filters",
            "International team fit: English-first docs, async proof routes, integration contracts, privacy boundaries, CI, runbooks, and operational handoff quality.",
            "What To Open First",
            "Enterprise Readiness",
            "First Message Shape",
            "Expected first result: one working slice with backend-owned state, tests, logs, docs, demo path, and handoff route.",
        ),
    ),
    RouteCheck(
        "services",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        (
            "Remote AI Automation Services - Alex Gerlitz",
            "Business workflows turned into owned backend systems.",
            '"@type": "Service"',
            '"hasOfferCatalog"',
            '"@id": "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html#offer-catalog"',
            "Best Immediate Starts",
            "Good Fit Filter",
            "LinkedIn Services Request Filter",
            "If LinkedIn routes the request as Web Development, Application Development, or Custom Software Development",
            "LinkedIn Service Page Fit",
            "Not my target right now: isolated brochure/static websites",
            "Fast First Message",
            "Message on LinkedIn",
            "Send one remote role or one messy workflow",
            "Remote role signal",
            "Project signal",
            "Useful first outcome: working slice with tests, logs, docs, and handoff.",
            "DriveDesk AI Operator Demo",
            "AI Workflow / RAG MVP",
            "CRM / ERP / API Adapter",
            "Proof-Backed Handoff",
            "GitHub-readable services page",
            "LinkedIn service page fit",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "work-with-me",
        "https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html",
        (
            "Work With Me - Alex Gerlitz",
            "Send one remote role or one messy workflow.",
            "Best Immediate Starts",
            "Remote Role",
            "Fixed-Scope Project",
            "Technical Proof",
            "What I Can Own",
            "Fast Fit Filter",
            "generic mobile/ecommerce apps without backend/integration ownership",
            "GitHub-readable version",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "services-md",
        profile_raw_url("SERVICES.md"),
        (
            "Remote AI Automation Services",
            "https://alexgerlitz.github.io/AlexGerlitz/services.html",
            "remote-only backend, AI automation",
            "Best-fit request shape: backend-owned state",
            "LinkedIn Services request filter",
            "if LinkedIn routes the request as Web Development, Application",
            "LinkedIn Service Page Fit",
            "./LINKEDIN_SERVICE_PAGE_FIT.md",
            "Not my target right now: isolated brochure/static websites",
            "DriveDesk AI Operator demo",
            "Remote-only LinkedIn service page",
            "skill-evidence.html",
        ),
    ),
    RouteCheck(
        "linkedin-service-page-fit-md",
        profile_raw_url("LINKEDIN_SERVICE_PAGE_FIT.md"),
        (
            "LinkedIn Service Page Fit",
            "Current LinkedIn Services categories observed on 2026-06-27",
            "Current live service-page assets observed on 2026-06-27",
            "media: DriveDesk AI Operator proof route and AI Ops Workflow Kit proof route",
            "Read-only category picker observed on 2026-06-27",
            "Technical Support` is a fallback",
            "broad-category routing can attract website refresh, standalone game, and generic",
            "system ownership: backend/platform, AI workflow, integration, DevOps, data, internal operations",
            "Keep:",
            "Remove:",
            "Primary add set:",
            "Exact LinkedIn Category Package",
            "remove `Web Development`",
            "remove `Application Development`",
            "Target saved package: 10 services total",
            "backend/platform, AI workflow, integration, data, and DevOps work",
            "Do not save a category set that removes the backend/platform/integration routing surface completely.",
            "test a narrower category set",
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
        profile_raw_url("INTAKE_BRIEF.md"),
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
        (
            "Fixed-scope AI automation",
            '"@type": "OfferCatalog"',
            '"priceCurrency": "USD"',
            '"minPrice": 25000',
            "services.html",
            "Best first step",
            "USD 3,000-12,000",
            "USD 25,000+ by phase",
        ),
        social_preview=True,
    ),
    RouteCheck(
        "start-conversation",
        "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
        (
            "Current Public Proof",
            '"jobTitle": "AI Automation / Backend / Platform Engineer"',
            '"knowsAbout"',
            "AI Operator case",
            "Recruiter Shortcut",
            "Best-fit remote titles: Back End Developer, Python Developer, AI Automation Engineer",
            "Artificial Intelligence Engineer with a workflow/backend focus",
            "Search-match stack: Python, FastAPI, PostgreSQL, Docker Compose, RAG, n8n, Telegram",
            "Remote role targets",
            "skill-evidence.html",
            "Open skill evidence",
            "role-targets.html",
            "hiring-decision.html",
            "intake-brief.html",
            "Inbound brief",
            "Best immediate starts",
            "Ready-to-Send Openings",
            "Can you review fit and suggest the smallest responsible first slice?",
            "Can you map the first working slice, integration risks, and verification path?",
            "Which repo, live check, and first-month slice should we start from?",
            "Fast Decision Routes",
            "Fast Decision Signals",
            "DriveDesk proof route",
            "Useful first outcome: working slice with tests, docs, and handoff.",
            "LinkedIn Services",
            "For fixed-scope project requests, the shortest route",
            "fixed-scope-offers.html",
            "Verification pack",
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
            "Fast Decision Routes",
            "Fast Decision Signals",
            "DriveDesk proof route",
            "Useful first outcome: working slice with tests, docs, and handoff.",
            "Verification pack",
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
        profile_raw_url("INBOUND_RESPONSE_PACK.md"),
        (
            "Contact Routes",
            "Fast fit checklist:",
            "student/course assignments",
            "generic mobile/ecommerce apps without",
            "with no way to verify success",
            "Fast Decision Routes",
            "Fast Decision Signals",
            "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
            "useful first outcome: working slice with tests, docs, and handoff.",
            "DriveDesk Proof Route",
        ),
    ),
    RouteCheck(
        "work-with-me-md",
        profile_raw_url("WORK_WITH_ME.md"),
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
        profile_raw_url("ROLE_PROJECT_BRIEF.md"),
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
        (
            "Last checked: 2026-06-27.",
            "AI Ops public proof status",
            "DriveDesk Core",
            "AI backend proof pack",
            "compact path through role fit, enterprise readiness, live proof, verification, and resume evidence",
            "Enterprise readiness",
            "international remote-team signals",
        ),
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
        "recruiter-card-image",
        "https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-27-recruiter-route",
        content_type="image/png",
        min_bytes=10_000,
        png_dimensions=(1200, 630),
    ),
    RouteCheck(
        "ai-backend-proof-pack-card-image",
        "https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-27-proof-pack",
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
        "ai-ops-live-postgres-persistence",
        "https://raw.githubusercontent.com/AlexGerlitz/ai-ops-workflow-kit/main/docs/evidence/live-postgres-persistence.txt",
        ("storage_after=postgres", "query_after_restart_source_found=true", "postgres_public_listener=false"),
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
