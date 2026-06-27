#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
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
    r"Short LinkedIn Notes",
    r"Fast Decision Prompts",
    r"decision prompts",
    r"contact route now",
    r"now gives",
    r"proof-route alias",
    r"markdown alias",
    r"What To Send",
    r"Current workflow:",
    r"Systems involved:",
    r"Systems/data:",
    r"Data sources:",
    r"Budget range:",
    r"Closest proof route:",
    r"Evidence available:",
    r"Output needed:",
    r"Useful link:",
    r"\[role title\]",
    r"\[stack\]",
    r"\[workflow/system\]",
    r"\[timeline\]",
    r"\[business process\]",
    r"\[CRM/ERP/API/docs/database\]",
    r"\[what should work\]",
    r"\[deadline/budget/hosting/access\]",
    r"\[repo/system/workflow\]",
    r"\[claim or risk\]",
    r"\[CI/logs/demo/docs\]",
    r"\[fix plan/proof route/first slice\]",
    marker(r"AI", r"/Codex"),
    marker(r"AI", r"-generated"),
    marker(r"Remote AI Automation", r" / Backend / DevOps"),
    marker(r"Chat", r"GPT"),
    marker(r"generated", r" by"),
    marker(r"Legacy", r" route"),
    marker(r"proof", r" route moved"),
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
    "hiring-decision.html",
    "linkedin-recruiter-packet.html",
    "recruiter-preferences.html",
    "decision-ready-contact.html",
    "flagship-platform.html",
    "drivedesk-proof-route.html",
    "drivedesk-ai-operator.html",
    "projects.html",
    "case-studies.html",
    "proof.html",
    "role-targets.html",
    "PROOF_OF_WORK.md",
    "first-30-days.html",
    "fixed-scope-offers.html",
    "services.html",
    "linkedin-service-page-fit.html",
    "work-with-me.html",
    "inbound-response.html",
    "intake-brief.html",
    "skill-evidence.html",
    "one-page-brief.html",
    "resume.html",
    "resume-pdf.html",
    "application-pack.html",
    "START_HERE.md",
    "LINKEDIN_RECRUITER_PACKET.md",
    "RECRUITER_PREFERENCES.md",
    "DECISION_READY_CONTACT.md",
    "APPLICATION_PACK.md",
    "RESUME.md",
    "SERVICES.md",
    "INBOUND_RESPONSE_PACK.md",
    "INTAKE_BRIEF.md",
    "WORK_WITH_ME.md",
    "SKILL_EVIDENCE.md",
    "ROLE_TARGETS.md",
    "FLAGSHIP_PLATFORM.md",
    "LINKEDIN_SERVICE_PAGE_FIT.md",
    "AI_AUTOMATION_ROLE_FIT.md",
    "CASE_STUDIES.md",
    "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    "assets/linkedin-banner.png",
    "assets/linkedin-banner.svg",
    "assets/social-card.png",
    "assets/social-card.svg",
    "assets/recruiter-card.png",
    "assets/recruiter-card.svg",
    "assets/ai-backend-proof-pack-card.png",
    "assets/ai-backend-proof-pack-card.svg",
    "assets/favicon.svg",
    "llms.txt",
    "sitemap.xml",
    "robots.txt",
]

REQUIRED_TEXT = {
    "README.md": [
        "actions/workflows/profile-audit.yml/badge.svg?branch=main",
        "actions/workflows/live-profile-smoke.yml/badge.svg?branch=main",
        "Now open for **remote-only full-time roles**",
        "Search-fit titles: Back End Developer, Python Developer",
        "LinkedIn recruiter search alignment",
        "Python, FastAPI, PostgreSQL, Docker, GitHub Actions, RAG, Vector Databases",
        "CRM/ERP/API integration, Systems Integration, DevOps, OpenAPI, n8n, Telegram, or pgvector",
        "Recruiter shortcut / 30-second screen",
        "LinkedIn Recruiter Packet",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html",
        "shortlist signal, risk reduction, AI execution proof, and message triggers",
        "Recruiter Preferences",
        "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
        "https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html",
        "https://alexgerlitz.github.io/AlexGerlitz/role-targets.html",
        "https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html",
        "Best match: backend/platform, AI automation, CRM/ERP/API integration, internal tools, or DevOps ownership.",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint, or DriveDesk AI Operator-style proof route.",
        "Fast public review",
        "AI Backend Proof Pack",
        "https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html",
        "Enterprise Readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        "Flagship Platform",
        "Decision routes",
        "Decision-Ready Contact",
        "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html",
        "Inbound / contact",
        "DriveDesk Proof Route",
        "Selected Proof Projects",
        "hiring-decision.html",
        "Live owner proof",
        "deterministic RAG quality eval",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        "https://alexgerlitz.github.io/AlexGerlitz/case-studies.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        "https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        "Inbound Brief",
        "remote-only full-time roles",
        "first month plan",
        "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html",
        "Fast fit checklist",
        "The larger [DriveDesk Flagship Platform]",
        "message me when the work is remote-only",
        "I am not positioning for onsite-only roles",
        "student/course assignments",
        "generic mobile/ecommerce apps without backend/integration ownership",
    ],
    "index.html": [
        '<link rel="icon" href="./assets/favicon.svg" type="image/svg+xml">',
        "./drivedesk-proof-route.html",
        "./ai-backend-proof-pack.html",
        "./enterprise-readiness.html",
        "./hiring-decision.html",
        "./projects.html",
        "./case-studies.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "Now open for remote-only backend/platform",
        "Search-fit titles: Back End Developer, Python Developer",
        "Recruiter shortcut / 30-second screen",
        "./linkedin-recruiter-packet.html",
        "LinkedIn recruiter packet",
        "Search filters, shortlist signal, risk reduction, AI execution proof and message triggers.",
        "./recruiter-preferences.html",
        "Recruiter preferences",
        "./decision-ready-contact.html",
        "Decision-ready contact",
        "Best match: backend/platform, AI automation, CRM/ERP/API integration, internal tools, or DevOps ownership.",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter",
        "./role-targets.html",
        "DriveDesk proof route",
        "AI backend proof pack",
        "Case studies",
        "Flagship platform",
        "./flagship-platform.html",
        "Open technical proof path",
        "Enterprise readiness",
        "DriveDesk AI Operator",
        "./skill-evidence.html",
        "Skill evidence",
        "./services.html",
        "./work-with-me.html",
        "Services",
        "./intake-brief.html",
        "Inbound brief",
        "Live owner proof",
        "Live route smoke",
        "pinned proof repos",
        "First month plan",
        "Fast fit checklist",
        "remote-only work with a concrete success condition",
        "onsite-only roles, pure prompt/content tasks",
        "student/course assignments",
        "generic mobile/ecommerce apps without",
    ],
    "hiring-decision.html": [
        "<title>Hiring Decision - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
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
        "Why To Shortlist Me",
        "I turn messy business workflows into backend-owned systems with records, state, integrations, logs, tests, docs, and handoff.",
        "Risk I Reduce",
        "Hidden no-code state becomes backend-owned records, audit, retries, idempotency, and recovery notes.",
        "Where I Fit In A Team",
        "What I can own in the first month",
        "Fast fit checklist",
        "backend-owned AI workflow, CRM/ERP/API integration",
        "Not my current target: onsite-only roles",
        "DriveDesk AI Operator",
        "Message on LinkedIn",
        "./output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        "./start-conversation.html",
        "./intake-brief.html",
    ],
    "linkedin-recruiter-packet.html": [
        "<title>LinkedIn Recruiter Packet - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "LinkedIn recruiter packet",
        "Fast route from profile view to technical decision.",
        "Visible Open-to-Work Titles",
        "Search Expansion Titles",
        "Skill Filters",
        "Work Mode",
        "First Result",
        "International team fit comes through English-first docs, async proof routes, integration contracts, privacy boundaries, CI, runbooks, and operational handoff quality.",
        "Shortlist Signal",
        "Messy business workflows become backend-owned systems with records, state, integrations, logs, tests, docs, and handoff.",
        "Risk Reduction",
        "Hidden automation state becomes explicit records, audit, retries, idempotency, privacy boundaries, and recovery notes.",
        "AI Execution Proof",
        "AI speeds research, implementation, docs, and debugging while engineering ownership stays with me.",
        "When To Message Me",
        "Business workflow where documents, transcripts, leads, tickets, or operator actions need RAG, analysis, scoring, approval, and system handoff.",
        "Integration work where CRM, ERP, 1C, banking, or API systems need explicit adapter contracts, retries, idempotency, audit, and recovery notes.",
        "DevOps/platform situation where Docker, CI, self-hosting, logs, health checks, backups, or runbooks need a verified recovery path.",
        "What To Open First",
        "Enterprise Readiness",
        "First Message Shape",
        "Expected first result",
        "Message on LinkedIn",
        "./hiring-decision.html",
        "./ai-backend-proof-pack.html",
        "./skill-evidence.html",
        "./enterprise-readiness.html",
        "./verification-pack.html",
        "./start-conversation.html",
        "./output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    ],
    "recruiter-preferences.html": [
        "<title>Recruiter Preferences - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "Open-to-Work alignment",
        "Recruiter preferences for remote backend, AI automation, integrations, and DevOps work.",
        "Open-To-Work Preference Set",
        "Visible LinkedIn Open-to-Work titles",
        "Search expansion titles",
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
        "./linkedin-recruiter-packet.html",
        "./hiring-decision.html",
        "./ai-backend-proof-pack.html",
        "./enterprise-readiness.html",
        "./output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    ],
    "decision-ready-contact.html": [
        "<title>Decision-Ready Contact - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
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
        "./linkedin-recruiter-packet.html",
        "./recruiter-preferences.html",
        "./hiring-decision.html",
        "./drivedesk-proof-route.html",
        "./ai-backend-proof-pack.html",
        "./enterprise-readiness.html",
        "./output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    ],
    "role-fit.html": [
        "AI Ops proof status",
        "Live owner proof",
        "RAG retrieval with quality eval",
        "AI Ops CI workflow",
        "Search-fit role targets",
        "./role-targets.html",
        "./skill-evidence.html",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "Python Backend Engineer",
        "LLM Workflow / RAG Engineer",
        "n8n AI Workflow Engineer",
        "./ROLE_TARGETS.md",
    ],
    "role-targets.html": [
        "<title>Remote Role Targets - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/role-targets.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/role-targets.html"',
        "Search-fit roles mapped to proof.",
        '"@type": "ProfilePage"',
        '"@type": "Person"',
        '"@type": "ItemList"',
        '"jobTitle": "AI Automation / Backend / Platform Engineer"',
        '"knowsAbout"',
        "remote-only full-time roles and concrete fixed-scope work",
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
        "Backend Engineer",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
        "First Month Ownership",
        "Skill evidence map",
        "Not My Current Target",
        "generic mobile/ecommerce apps without backend/integration ownership",
        "./ROLE_TARGETS.md",
    ],
    "resume.html": [
        "<title>Resume - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/resume.html"',
        "DriveDesk AI Operator proof route",
        "Fast fit checklist: remote-only work with a concrete technical outcome",
        "Shortlist signal: messy business workflows become backend-owned systems with records, state, integrations, logs, tests, docs, and handoff.",
        "Risk I reduce: hidden automation state, brittle no-code glue, unclear adapter boundaries, missing logs, and unverified AI-assisted output.",
        "Not my target right now: onsite-only roles",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "PDF resume",
        "Remote-only backend, platform, DevOps, and AI automation roles.",
        "Back End Developer / Python Developer roles around APIs",
        "CRM, ERP, 1C, accounting, banking, webhook, and API integration adapters.",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "Vector Databases",
    ],
    "application-pack.html": [
        "<title>Role Fit Pack - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/application-pack.html"',
        'property="og:title" content="AI Automation / Backend / Platform Role Fit - Alex Gerlitz"',
        'name="twitter:title" content="AI Automation / Backend / Platform Role Fit - Alex Gerlitz"',
        "Remote AI automation, backend/platform, integration, and DevOps work.",
        "deterministic RAG quality eval",
        "Fast fit checklist: remote-only work, concrete technical outcome",
        "Shortlist signal: messy business workflows become backend-owned systems with records, state, integrations, logs, tests, docs, and handoff.",
        "Risk I reduce: hidden automation state, brittle no-code glue, unclear adapter boundaries, missing logs, and unverified AI-assisted output.",
        "Not my target right now: onsite-only roles",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "./skill-evidence.html",
        "AI Automation Engineer",
        "Backend / Platform Engineer",
        "LLM Workflow / RAG Engineer",
        "PDF resume",
    ],
    "START_HERE.md": [
        "2-minute decision route",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Fast fit checklist: message me when the work is remote-only",
        "Not my target right now: onsite-only roles",
        "student/course assignments",
        "generic mobile/ecommerce apps without backend/integration ownership",
        "with no way to verify success",
        "DriveDesk AI Operator proof route",
        "Skill Evidence",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        "LinkedIn Services",
        "Inbound Brief",
        "LinkedIn Recruiter Packet",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html",
        "Recruiter Preferences",
        "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
        "Decision-Ready Contact",
        "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html",
        "AI Backend Proof Pack",
        "compact route through AI workflow, backend/platform, integration, DevOps, CI, runbooks, and resume proof",
        "Enterprise Readiness",
        "international employer-grade review of architecture, state, integration contracts, English-first docs, reliability, privacy, CI, runbooks, and handoff quality",
        "Role Fit Pack",
        "PDF Resume",
        "Fast Decision Signals",
        "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "useful first outcome: working slice with tests, docs, and handoff.",
        "./ENTERPRISE_READINESS.md",
        "./AI_BACKEND_PROOF_PACK.md",
    ],
    "LINKEDIN_RECRUITER_PACKET.md": [
        "LinkedIn Recruiter Packet",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html",
        "30-Second Fit",
        "Visible LinkedIn Open-to-Work titles: Back End Developer, Artificial Intelligence Engineer, Python Developer, Platform Engineer, DevOps Engineer.",
        "Search expansion titles: AI Automation Engineer, Integration Engineer, LLM Workflow / RAG Engineer",
        "Search Alignment",
        "Job title filters",
        "Skill filters",
        "Shortlist signal: messy business workflows become backend-owned systems with records, state, integrations, logs, tests, docs, and handoff.",
        "Risk reduction: hidden automation state becomes explicit records, audit, retries, idempotency, privacy boundaries, and recovery notes.",
        "AI-assisted execution signal: AI speeds research, implementation, docs, and debugging while engineering ownership stays with me.",
        "International team fit: English-first docs, async proof routes, integration contracts, privacy boundaries, CI, runbooks, and operational handoff quality.",
        "What To Open First",
        "Enterprise Readiness",
        "First Message Shape",
        "Expected first result: one working slice with backend-owned state, tests, logs, docs, demo path, and handoff route.",
    ],
    "RECRUITER_PREFERENCES.md": [
        "Recruiter Preferences",
        "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
        "Open-To-Work Preference Set",
        "Visible LinkedIn Open-to-Work titles",
        "Search expansion titles",
        "Location type",
        "Remote locations",
        "Employment types",
        "Recruiter Search Keywords",
        "International remote teams, Europe-compatible remote teams, US-compatible async teams, and distributed product/operations teams.",
        "Open to remote full-time roles and concrete fixed-scope projects.",
        "Proof Map",
        "First Contact Fit",
        "Not My Target",
    ],
    "DECISION_READY_CONTACT.md": [
        "Decision-Ready Contact",
        "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html",
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
        "Enterprise Readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        "Fast Fit",
    ],
    "ai-backend-proof-pack.html": [
        "<title>AI Backend Proof Pack - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        "Public proof pack",
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
        "./drivedesk-proof-route.html",
        "./enterprise-readiness.html",
        "./verification-pack.html",
    ],
    "AI_BACKEND_PROOF_PACK.md": [
        "AI Backend Proof Pack",
        "https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html",
        "I do not just connect workflow nodes.",
        "DriveDesk Proof Route",
        "Enterprise Readiness",
        "AI Ops live owner proof",
        "Live PostgreSQL/pgvector proof",
        "Verification Pack",
        "PDF Resume",
        "Strong Match",
        "Useful First Context",
    ],
    "enterprise-readiness.html": [
        "<title>Enterprise Readiness - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html"',
        "Enterprise readiness",
        "Proof for teams that need a reliable backend/platform owner.",
        "./ai-backend-proof-pack.html",
        "AI backend proof pack",
        "international employer-grade team can inspect",
        "architecture, state ownership, integration contracts, reliability, privacy, observability, CI, runbooks, and handoff quality",
        "International Employer Signals",
        "Qualification depth: backend/platform work, AI workflow engineering, CRM/ERP/API integration, DevOps, and support of real business infrastructure are tied to public proof.",
        "Enterprise constraints: privacy boundaries, approvals, audit trail, retries, idempotency, rollback thinking, and runbooks are visible instead of hidden behind workflow glue.",
        "Async review quality: English-first docs, proof routes, CI, smoke checks, and compact evidence make it possible to evaluate work across time zones.",
        "English-first docs",
        "Async review path",
        "DriveDesk AI Operator",
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
        "Message on LinkedIn",
        "./drivedesk-proof-route.html",
        "./verification-pack.html",
        "./start-conversation.html",
    ],
    "ENTERPRISE_READINESS.md": [
        "Enterprise Readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
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
    ],
    "APPLICATION_PACK.md": [
        "Role Fit Pack",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "Fast fit checklist: remote-only work, concrete technical outcome",
        "Shortlist signal: messy business workflows become backend-owned systems with records, state,",
        "Risk I reduce: hidden automation state, brittle",
        "Not my target right now: onsite-only roles",
        "AI Automation Engineer",
        "Backend / Platform Engineer",
        "LLM Workflow / RAG Engineer",
        "PDF resume",
    ],
    "RESUME.md": [
        "Remote-only AI automation, backend/platform, and DevOps engineer",
        "Search-fit role titles: Back End Developer, Python Developer",
        "Fast fit checklist: remote-only work with a concrete technical outcome",
        "Shortlist signal: I turn messy business workflows into backend-owned systems with records, state,",
        "Risk I reduce: hidden automation state, brittle",
        "right now: onsite-only roles",
        "Artificial Intelligence Engineer with a workflow/backend focus",
        "PDF resume for application upload",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "AI Automation Engineer",
        "Integration Engineer",
        "Remote Role Targets",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "vector",
    ],
    "SERVICES.md": [
        "Remote AI Automation Services",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        "remote-only backend, AI automation",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Best-fit request shape: backend-owned state, data sources, integration boundaries",
        "LinkedIn Services request filter",
        "if LinkedIn routes the request as Web Development, Application",
        "LinkedIn Services Fit",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
        "Not my target right now: isolated brochure/static websites",
        "Fast first message: send one remote role or one messy workflow",
        "Remote role signal",
        "Project signal",
        "useful first outcome: working slice with tests, logs, docs, and handoff.",
        "DriveDesk AI Operator demo",
        "Remote-only LinkedIn service page",
        "Fixed-Scope AI Automation Offers",
        "https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html",
        "GitHub-readable role keywords and skills mapped to",
    ],
    "services.html": [
        "<title>Remote AI Automation Services - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/services.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/services.html"',
        "Business workflows turned into owned backend systems.",
        '"@type": "Service"',
        '"@id": "https://alexgerlitz.github.io/AlexGerlitz/services.html#remote-ai-automation-services"',
        '"hasOfferCatalog"',
        '"@id": "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html#offer-catalog"',
        "Best Immediate Starts",
        "Good Fit Filter",
        "LinkedIn Services Request Filter",
        "If LinkedIn routes the request as Web Development, Application Development, or Custom Software Development",
        "LinkedIn Services Fit",
        "./linkedin-service-page-fit.html",
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
        "Internal Operations Platform",
        "DevOps / Recovery Sprint",
        "Workflow Teardown + Working Slice",
        "Proof-Backed Handoff",
        "Backend-owned state, audit, retries, idempotency, and adapter contracts.",
        "./fixed-scope-offers.html",
        "./intake-brief.html",
        "./SERVICES.md",
        "./linkedin-service-page-fit.html",
        "GitHub-readable services page",
    ],
    "linkedin-service-page-fit.html": [
        "<title>LinkedIn Services Fit - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html"',
        '"@id": "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html#service-fit"',
        "Broad service labels, narrow engineering ownership.",
        "Cloud Application Development, Web Development, Application Development, Custom Software Development, Information Management, or IT Consulting",
        "Best-Fit Service Requests",
        "Backend-Owned AI Workflow",
        "CRM / ERP / API Integration",
        "Internal Operations Platform",
        "DevOps / Recovery Sprint",
        "Data Workflow",
        "Workflow Teardown",
        "Not The Right Request",
        "Useful First Context",
        "What I Can Send Back",
        "Smallest responsible working slice",
        "Proof Route",
        "Open LinkedIn Services",
        "./services.html",
        "./fixed-scope-offers.html",
        "./drivedesk-proof-route.html",
        "./enterprise-readiness.html",
    ],
    "LINKEDIN_SERVICE_PAGE_FIT.md": [
        "LinkedIn Service Page Fit",
        "Public fit filter for LinkedIn Services requests.",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
        "The live LinkedIn Services categories are broad routing labels.",
        "Best-Fit Service Requests",
        "Backend-owned AI workflow",
        "CRM/ERP/1C/banking/accounting/API/database integration",
        "FastAPI/PostgreSQL backend",
        "Broad Category Filter",
        "Cloud Application Development, Web Development",
        "Custom Software Development, Information Management, or IT Consulting",
        "Useful First Context",
        "What I Can Send Back",
        "Smallest responsible working slice",
        "Enterprise readiness",
        "backend/platform, AI workflow, integration, data, DevOps, and internal-operations ownership",
    ],
    "work-with-me.html": [
        "<title>Work With Me - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html"',
        "Send one remote role or one messy workflow.",
        "I build backend-owned AI workflow and operations systems for real businesses",
        "Best Immediate Starts",
        "AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint",
        "Remote Role",
        "Fixed-Scope Project",
        "Technical Proof",
        "What I Can Own",
        "FastAPI/PostgreSQL backend",
        "RAG ingestion, retrieval, citations",
        "CRM/ERP/API/1C/banking/accounting adapter contracts",
        "AI-assisted execution",
        "Fast Fit Filter",
        "remote-only role or fixed-scope work",
        "student/course assignments",
        "generic mobile/ecommerce apps without backend/integration ownership",
        "./WORK_WITH_ME.md",
    ],
    "SKILL_EVIDENCE.md": [
        "Skill Evidence Matrix",
        "Vector Databases",
        "deterministic RAG quality eval",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "AI-Assisted Execution Discipline",
        "Fast problem decomposition",
        "Engineering ownership",
        "Verification habit",
        "Full-cycle delivery",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
    ],
    "skill-evidence.html": [
        "<title>Skill Evidence - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html"',
        "Skill-to-proof map",
        "Skills mapped to public proof.",
        "AI Automation / RAG",
        "RAG retrieval with deterministic quality eval",
        "Backend / Platform",
        "CRM / ERP Integration",
        "DevOps / Self-Hosting",
        "Best Skills To Evaluate",
        "AI-Assisted Execution Discipline",
        "Fast Problem Decomposition",
        "Verification Habit",
        "Full-Cycle Delivery",
        "The engineering responsibility stays with me: architecture, state, integration boundaries, privacy, verification, deployment, logs, runbooks, and shipped quality.",
        "./SKILL_EVIDENCE.md",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
    ],
    "ROLE_TARGETS.md": [
        "Remote Role Targets",
        "Systems Integration Engineer",
        "Recruiter Search Snapshot",
        "LinkedIn Recruiter Search Alignment",
        "Job title filters",
        "Skill filters",
        "First message trigger",
        "AI Automation / Backend / Platform Engineer",
        "Backend Development",
        "Platform Engineering",
        "Workflow Automation",
        "CRM / ERP Integrations",
        "Bitrix24 / CRM Adapter Work",
        "Docker Compose",
        "GitHub Actions",
        "Back End Developer / Python Developer",
        "Artificial Intelligence Engineer",
        "Customer Relationship Management (CRM) Engineer",
        "Enterprise Resource Planning (ERP) Engineer",
        "Vector Databases Engineer",
    ],
    "AI_AUTOMATION_ROLE_FIT.md": [
        "AI Automation Role Fit",
        "Vector Databases",
        "PostgreSQL/pgvector-backed storage",
        "CRM / Bitrix / API handoff",
        "Live owner proof",
        "Live Telegram approval evidence",
        "AI Ops CI workflow",
    ],
    "start-conversation.html": [
        "Current Public Proof",
        '"jobTitle": "AI Automation / Backend / Platform Engineer"',
        '"knowsAbout"',
        "Live owner proof",
        "AI Operator case",
        "Recruiter Shortcut",
        "Best-fit remote titles: Back End Developer, Python Developer, AI Automation Engineer",
        "Artificial Intelligence Engineer with a workflow/backend focus",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker Compose, RAG, n8n, Telegram",
        "Remote role targets",
        "./skill-evidence.html",
        "Open skill evidence",
        "./role-targets.html",
        "./hiring-decision.html",
        "./intake-brief.html",
        "./enterprise-readiness.html",
        "Enterprise readiness",
        "Inbound brief",
        "Fast Decision Routes",
        "Fast Decision Signals",
        "./assets/copy-blocks.css",
        "./assets/copy-blocks.js",
        "DriveDesk proof route",
        "Useful first outcome: working slice with tests, docs, and handoff.",
        "LinkedIn Services",
        "For fixed-scope project requests, the shortest route",
        "./fixed-scope-offers.html",
        "Verification pack",
        "role fit and first-month ownership",
        "whether a practical first slice can ship quickly",
        "First month plan",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint, or DriveDesk AI Operator-style proof route.",
        "Ready-to-Send Openings",
        "Can you review fit and suggest the smallest responsible first slice?",
        "Can you map the first working slice, integration risks, and verification path?",
        "Which repo, live check, and first-month slice should we start from?",
        "Fast Fit Checklist",
        "Message me when the work is remote-only",
        "Strong match",
        "Useful first proof",
        "Not my target",
        "student/course assignments",
        "Generic mobile/ecommerce apps without backend/integration ownership",
        "Undefined outcomes with no way to verify success.",
        "What I Send Back",
        "The smallest responsible first slice.",
    ],
    "inbound-response.html": [
        "<title>Contact Routes - Alex Gerlitz</title>",
        "Contact route for remote roles, fixed-scope projects, and proof reviews",
        "Send one role, workflow, or proof question",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html"',
        "Decision-Ready Signals",
        "Fast Decision Routes",
        "Fast Decision Signals",
        "./assets/copy-blocks.css",
        "./assets/copy-blocks.js",
        "DriveDesk proof route",
        "Useful first outcome: working slice with tests, docs, and handoff.",
        "Verification pack",
        "which technical claim or risk should be validated",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Message on LinkedIn",
        "PDF resume",
        "First month plan",
        "DriveDesk AI Operator proof route",
        "./enterprise-readiness.html",
        "Enterprise readiness",
        "./skill-evidence.html",
        "Skill evidence",
        "./intake-brief.html",
        "Inbound brief",
        "Response Shape",
        "concrete next step instead of a generic intro call",
        "Smallest responsible working slice",
        "Claim-to-evidence map",
    ],
    "intake-brief.html": [
        "<title>Inbound Brief - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html"',
        "Send enough context for a concrete engineering next step.",
        "Best Immediate Starts",
        "AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint, or DriveDesk AI Operator-style proof route.",
        "Remote Role",
        "Fixed-Scope Project",
        "Technical Review",
        "What I Send Back",
        "The smallest responsible first slice.",
        "Relevant repo, page, demo, CI run, doc, or smoke route.",
        "./enterprise-readiness.html",
        "Enterprise readiness",
        "./INTAKE_BRIEF.md",
        "GitHub-readable inbound brief",
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
        "RAG eval 2/2",
        "DeployMate - Self-hosted Docker Deployment Control Panel",
        "MPlusForm - Validation Boundary / Desktop Automation Proof",
        "Public verification workflow",
        "Trust model",
    ],
    "case-studies.html": [
        "<title>Engineering Case Studies - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/case-studies.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/case-studies.html"',
        "Problem, build, evidence, and operating proof",
        "DriveDesk / Autoschool54 Operations Platform Direction",
        "AI Ops Workflow Kit",
        "RAG retrieval with quality eval",
        "DeployMate",
        "MPlusForm",
        "The operating loop",
        "./CASE_STUDIES.md",
    ],
    "proof.html": [
        "<title>Technical Proof Path - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/proof.html"',
        "Proof that can be inspected, not just claimed.",
        "./verification-pack.html",
        "./start-conversation.html",
        "LinkedIn Services",
        "./case-studies.html",
        "Open engineering case studies",
        "After Review",
        "one success condition",
    ],
    "PROOF_OF_WORK.md": [
        "Proof of Work",
        "Public Proof Links",
        "Reviewer Shortcuts",
        "https://alexgerlitz.github.io/AlexGerlitz/case-studies.html",
        "Fast Proof Review",
        "Start conversation",
        "Contact routes",
        "Enterprise readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        "LinkedIn Services",
    ],
    "CASE_STUDIES.md": [
        "Engineering Case Studies",
        "https://alexgerlitz.github.io/AlexGerlitz/case-studies.html",
        "DriveDesk / Autoschool54 Operations Platform Direction",
        "AI Ops Workflow Kit",
        "DeployMate",
        "MPlusForm",
        "Common Pattern",
    ],
    "drivedesk-proof-route.html": [
        "<title>DriveDesk AI Operator - Proof Route</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        '"@type": "ProfilePage"',
        '"jobTitle": "AI Automation / Backend / Platform Engineer"',
        '"knowsAbout"',
        '"Transcript analysis"',
        '"name": "Start conversation"',
        "./assets/copy-blocks.css",
        "./assets/copy-blocks.js",
        "Clean public proof route",
        "public runtime runs with `storage=postgres`",
        "restart persistence",
        "RAG quality eval",
        "Message on LinkedIn",
        "./ai-backend-proof-pack.html",
        "AI Backend Proof Pack",
        "compact route through AI workflow, backend/platform, integration, DevOps, live proof, and resume evidence",
        "./enterprise-readiness.html",
        "international remote-team review of architecture, state, integration contracts, reliability, privacy, CI, runbooks, and handoff quality",
        "Remote role signal",
        "Workflow project signal",
        "DriveDesk proof route",
        "Useful first outcome: working slice with tests, docs, and handoff.",
        "Remote role decision",
        "Project decision",
        "Technical proof decision",
        "./output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
        "./inbound-response.html",
        "Profile funnel health",
        "./skill-evidence.html",
        "First month plan",
    ],
    "flagship-platform.html": [
        "<title>DriveDesk Flagship Platform - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html"',
        "DriveDesk starts with an AI sales and support workflow operator.",
        "Core Backend",
        "Integration Layer",
        "AI Operator Layer",
        "DevOps Layer",
        "Business Outcome",
        "How I Would Start",
        "Good First Slices",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
        "DeployMate",
        "For Remote Roles",
    ],
    "first-30-days.html": [
        "<title>First Month Delivery Plan - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "First 48 Hours",
        "Week 2",
        "What I Need To Start",
    ],
    "fixed-scope-offers.html": [
        "backed by DriveDesk AI Operator proof",
        '"@type": "OfferCatalog"',
        '"@id": "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html#offer-catalog"',
        '"priceCurrency": "USD"',
        '"minPrice": 25000',
        "./drivedesk-proof-route.html",
        "./services.html",
        "Open DriveDesk proof route",
        "LinkedIn Services",
        "Best first step",
        "Workflow Teardown + Working Slice",
        "USD 3,000-12,000",
        "USD 25,000+ by phase",
    ],
    "one-page-brief.html": [
        "DriveDesk AI Operator - Proof Route",
        "DriveDesk AI Operator proof route",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "Open the current proof route",
        "backend-owned AI workflows, RAG, transcript analysis, approvals",
    ],
    "featured-drivedesk.html": [
        "DriveDesk AI Operator proof route",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "Open the current proof route",
        "backend-owned AI workflows, RAG, transcript analysis, approvals",
    ],
    "ONE_PAGE_BRIEF.md": [
        "DriveDesk AI Operator Proof Route",
        "Canonical public proof route",
        "DriveDesk AI Operator proof route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
    ],
    "resume-pdf.html": [
        "Proof route: alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "Start: alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
        "Services fit: alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
        "focused on DriveDesk AI Operator",
        "Search-fit titles: Back End Developer, Python Developer",
        "Fast fit: remote-only work with a concrete technical outcome",
        "Shortlist signal: backend-owned state, integrations, logs, tests, docs, and handoff.",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, Docker Compose, RAG, n8n, Telegram",
        "fixed-scope automation",
        "Systems Integration",
        "Customer Relationship Management (CRM)",
        "Enterprise Resource Planning (ERP)",
        "vector databases",
    ],
    "assets/social-card.svg": [
        "DriveDesk AI Operator - Proof Route",
        "Backend-owned AI workflow proof",
        "Start conversation / PDF resume / role fit / verification",
        "Role decision",
        "Project decision",
        "Technical proof",
        "drivedesk-proof-route.html",
    ],
    "assets/recruiter-card.svg": [
        "Recruiter Preferences - Alex Gerlitz",
        "RECRUITER FIT / AI AUTOMATION + BACKEND PLATFORM",
        "Recruiter",
        "Preferences",
        "Open-to-Work alignment / DriveDesk proof / PDF resume",
        "Full-time / contract",
        "RAG / CRM-ERP",
        "alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
    ],
    "assets/ai-backend-proof-pack-card.svg": [
        "AI Backend Proof Pack - Alex Gerlitz",
        "LINKEDIN FEATURED / AI WORKFLOWS + BACKEND PLATFORM",
        "RAG workflows / FastAPI + PostgreSQL / CRM adapters / Docker + CI",
        "alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html",
    ],
    "assets/linkedin-banner.svg": [
        "Alex Gerlitz LinkedIn banner",
        "DriveDesk AI Operator",
        "REMOTE AI AUTOMATION / BACKEND / PLATFORM",
        "RAG + LLM workflows + CRM/ERP integrations",
        "FastAPI / PostgreSQL / Docker / n8n / Telegram / CI / runbooks",
        "alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
    ],
    "INBOUND_RESPONSE_PACK.md": [
        "Contact Routes",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Fast fit checklist:",
        "strongest match: remote-only work with a concrete technical outcome",
        "not my target right now: onsite-only roles",
        "student/course assignments",
        "generic mobile/ecommerce apps without",
        "with no way to verify success",
        "Fast Decision Routes",
        "Fast Decision Signals",
        "Enterprise review",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        "International employer-grade route for backend/platform ownership",
        "role fit and first-month ownership",
        "whether a practical first slice can ship quickly",
        "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "useful first outcome: working slice with tests, docs, and handoff.",
        "DriveDesk Proof Route",
        "Inbound brief",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        "Enterprise readiness",
        "https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html",
        "LinkedIn Services",
    ],
    "INTAKE_BRIEF.md": [
        "Inbound Brief",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Fast fit checklist:",
        "remote-only role or fixed-scope work",
        "not a fit right now: onsite-only roles",
        "student/course assignments",
        "generic mobile/ecommerce apps without",
        "Start conversation",
        "Contact routes",
        "LinkedIn Services",
        "For A Role",
        "For A Fixed-Scope Project",
    ],
    "WORK_WITH_ME.md": [
        "Work With Me",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps",
        "Fast fit checklist: remote-only work",
        "student/course assignments",
        "generic mobile/ecommerce apps without backend/integration ownership",
        "Workflow Teardown + Working Slice",
        "Integration Adapter",
    ],
    "llms.txt": [
        "# Alex Gerlitz - AI Automation / Backend / Platform Engineer",
        "I build backend-owned AI workflow and operations systems for real businesses",
        "DriveDesk AI Operator proof route",
        "AI Backend Proof Pack",
        "compact route through AI workflow, backend/platform, integration, DevOps, live proof, verification, and resume evidence",
        "Enterprise Readiness",
        "international employer-grade review route for architecture, state ownership, integration contracts, English-first docs, async proof paths, reliability, privacy, observability, CI, runbooks, and handoff quality",
        "DriveDesk Flagship Platform",
        "Hiring decision route",
        "one-minute role fit, why to shortlist me, risk reduction, strongest proof, first-month ownership, and contact route",
        "LinkedIn Recruiter Packet",
        "search filters, 30-second fit, proof order, message triggers, expected first result, shortlist signal, risk reduction, AI-assisted execution proof, and international remote-team proof routing",
        "Recruiter Preferences",
        "Open-to-Work alignment for job titles, remote work mode, employment types, recruiter search keywords, proof order, and first contact fit.",
        "Decision-Ready Contact",
        "minimum first context, fit read, risk check, smallest responsible first slice, proof route, and next step.",
        "Start conversation",
        "recruiter shortcut, role-target links, PDF resume, proof route, and the fastest contact path",
        "Selected proof projects",
        "DriveDesk Core, AI Ops Workflow Kit, DeployMate, and MPlusForm",
        "Remote role targets",
        "Work with me",
        "Skill evidence map",
        "AI-assisted execution discipline",
        "Verification pack",
        "AI Backend Proof Pack Markdown",
        "Enterprise Readiness Markdown",
        "LinkedIn Services Fit",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
        "Remote-only backend, platform, DevOps, AI automation",
        "Search-Fit Role Targets",
        "LinkedIn recruiter search alignment",
        "Python, FastAPI, PostgreSQL, Docker, GitHub Actions, RAG, Vector Databases",
        "LLM Workflow / RAG Engineer",
        "remote-only full-time roles or concrete fixed-scope projects",
        "First-month ownership",
        "backend-owned AI workflows, CRM/ERP/API adapters",
        "Recruiter shortcut: for a remote role, start with LinkedIn Recruiter Packet, Recruiter Preferences, Hiring decision route, Remote role targets, Skill evidence, and the PDF resume.",
        "Best match: backend/platform, AI automation, CRM/ERP/API integration, internal tools, or DevOps ownership.",
        "AI Ops Workflow Kit",
        "validation-boundary and trust-model automation proof",
        "public verification",
        "https://github.com/AlexGerlitz/MPlusForm/actions/runs/28285062880",
        "LinkedIn Services",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
        "The main signal is not no-code node wiring.",
    ],
    "ROLE_PROJECT_BRIEF.md": [
        "Role / Project Brief",
        "Remote AI automation, backend/platform and DevOps engineer building DriveDesk",
        "Not My Target",
        "Student/course assignments",
        "Generic mobile/ecommerce apps without backend/integration ownership",
        "DriveDesk proof route",
        "AI Ops Workflow Kit reviewer snapshot",
    ],
    "sitemap.xml": [
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html",
        "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html",
        "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html",
        "https://alexgerlitz.github.io/AlexGerlitz/LINKEDIN_RECRUITER_PACKET.md",
        "https://alexgerlitz.github.io/AlexGerlitz/RECRUITER_PREFERENCES.md",
        "https://alexgerlitz.github.io/AlexGerlitz/DECISION_READY_CONTACT.md",
        "https://alexgerlitz.github.io/AlexGerlitz/llms.txt",
        "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
    ],
}

SOCIAL_PREVIEW_PAGES = [
    "index.html",
    "hiring-decision.html",
    "linkedin-recruiter-packet.html",
    "recruiter-preferences.html",
    "decision-ready-contact.html",
    "drivedesk-proof-route.html",
    "projects.html",
    "case-studies.html",
    "role-fit.html",
    "role-targets.html",
    "skill-evidence.html",
    "proof.html",
    "fixed-scope-offers.html",
    "services.html",
    "linkedin-service-page-fit.html",
    "work-with-me.html",
    "start-conversation.html",
    "resume.html",
    "application-pack.html",
    "first-30-days.html",
    "inbound-response.html",
    "intake-brief.html",
    "ai-backend-proof-pack.html",
    "enterprise-readiness.html",
]

SOCIAL_PREVIEW_SNIPPETS = [
    'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
    'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
    'property="og:image:type" content="image/png"',
    'property="og:image:width" content="1200"',
    'property="og:image:height" content="630"',
    'property="og:image:alt"',
    'name="twitter:card" content="summary_large_image"',
    'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-28-platform-card"',
    'name="twitter:image:alt"',
]

SOCIAL_PREVIEW_PAGE_SNIPPETS = {
    "linkedin-recruiter-packet.html": [
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:type" content="image/png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'property="og:image:alt"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'name="twitter:image:alt"',
    ],
    "recruiter-preferences.html": [
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:type" content="image/png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'property="og:image:alt"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'name="twitter:image:alt"',
    ],
    "decision-ready-contact.html": [
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'property="og:image:type" content="image/png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'property="og:image:alt"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/recruiter-card.png?v=2026-06-28-recruiter-card"',
        'name="twitter:image:alt"',
    ],
    "ai-backend-proof-pack.html": [
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        'property="og:image:type" content="image/png"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'property="og:image:alt"',
        'name="twitter:card" content="summary_large_image"',
        'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/ai-backend-proof-pack-card.png?v=2026-06-28-proof-pack"',
        'name="twitter:image:alt"',
    ],
}

SITEMAP_LASTMOD_REQUIREMENTS = {
    "https://alexgerlitz.github.io/AlexGerlitz/": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/linkedin-recruiter-packet.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/recruiter-preferences.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/llms.txt": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/role-targets.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/VERIFICATION_PACK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/PROOF_OF_WORK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/SKILL_EVIDENCE.md": "2026-06-26",
    "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/INTAKE_BRIEF.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/INBOUND_RESPONSE_PACK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/ROLE_PROJECT_BRIEF.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/START_HERE.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/LINKEDIN_RECRUITER_PACKET.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/RECRUITER_PREFERENCES.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/DECISION_READY_CONTACT.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/services.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/SERVICES.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/LINKEDIN_SERVICE_PAGE_FIT.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/WORK_WITH_ME.md": "2026-06-27",
}

CURRENT_EVIDENCE_SNIPPETS = {
    "VERIFICATION_PACK.md": [
        "Last checked: 2026-06-27.",
        "DriveDesk Core `main` is green on `633e92a`.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28284702693",
        "AI Ops latest checked CI run succeeded on `a10092a`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28291596272",
        "AI Ops live smoke passed on app SHA `1a83406` with `storage=postgres`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/live-postgres-persistence.txt",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md",
        "DeployMate default branch `develop` is green on `237b2c9`.",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "Profile funnel has current default-branch checks for public audit, Pages deployment, and live smoke.",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/profile-audit.yml?query=branch%3Amain",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions?query=branch%3Amain+workflow%3Apages-build-deployment",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/live-profile-smoke.yml?query=branch%3Amain",
        "MPlusForm `main` is green on `f7b952c`",
        "https://github.com/AlexGerlitz/MPlusForm/actions/runs/28285062880",
    ],
    "PROOF_OF_WORK.md": [
        "Checked on 2026-06-27:",
        "DriveDesk Core `main` is green on `633e92a`.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28284702693",
        "AI Ops latest checked CI run succeeded on `a10092a`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28291596272",
        "AI Ops live smoke passed on app SHA `1a83406` with `storage=postgres`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/live-postgres-persistence.txt",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md",
        "DeployMate default branch `develop` is green on `237b2c9`.",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "Profile funnel has current default-branch checks for public audit, Pages deployment, and live smoke.",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/profile-audit.yml?query=branch%3Amain",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions?query=branch%3Amain+workflow%3Apages-build-deployment",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/live-profile-smoke.yml?query=branch%3Amain",
        "MPlusForm `main` is green on `f7b952c`.",
        "https://github.com/AlexGerlitz/MPlusForm/actions/runs/28285062880",
    ],
    "verification-pack.html": [
        "Last checked: 2026-06-27.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28284702693",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28291596272",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/profile-audit.yml?query=branch%3Amain",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions?query=branch%3Amain+workflow%3Apages-build-deployment",
        "https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/live-profile-smoke.yml?query=branch%3Amain",
        "https://github.com/AlexGerlitz/MPlusForm/actions/runs/28285062880",
        "<code>633e92a</code>",
        "<code>a10092a</code>",
        "<code>1a83406</code>",
        "<code>storage=postgres</code>",
        "<code>237b2c9</code>",
        "<code>f7b952c</code>",
    ],
    "drivedesk-core-review.html": [
        "Public demo checked on 2026-06-27.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28284702693",
    ],
    "SKILL_EVIDENCE.md": [
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28291596272",
    ],
}

PDF_ARTIFACTS = {
    "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf": {
        "pages": 1,
        "required": [],
        "text_required": [
            "PostgreSQL/pgvector-backed workflows",
            "live PostgreSQL/pgvector persistence",
            "FastAPI, PostgreSQL/pgvector, Docker, document APIs, n8n, Telegram",
            "Shortlist signal: backend-owned state, integrations, logs, tests, docs, and handoff.",
            "Start: alexgerlitz.github.io/AlexGerlitz/start-conversation.html",
            "Services fit: alexgerlitz.github.io/AlexGerlitz/linkedin-service-page-fit.html",
            "AI Ops Workflow Kit",
        ],
        "forbidden": [
            b"file://",
            b"Users/alexgerlitz",
            b"Documents/Codex",
            b"new-chat",
            b"27.06.",
            b"AI-generated",
            b"One-Page Brief",
        ],
        "text_forbidden": [
            "pgvector-ready",
            "file://",
            "Users/alexgerlitz",
            "Documents/Codex",
        ],
    },
}


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


class JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_json_ld = False
        self._current: list[str] = []
        self.blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        values = dict(attrs)
        if values.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._current = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_json_ld:
            self.blocks.append("".join(self._current).strip())
            self._in_json_ld = False
            self._current = []


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


def check_required_text_key_shape(errors: list[str]) -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "REQUIRED_TEXT" for target in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            return
        seen: set[str] = set()
        duplicates: set[str] = set()
        for key in node.value.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if key.value in seen:
                    duplicates.add(key.value)
                seen.add(key.value)
        for duplicate in sorted(duplicates):
            errors.append(f"REQUIRED_TEXT duplicate key: {duplicate}")
        return


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
        snippets = SOCIAL_PREVIEW_PAGE_SNIPPETS.get(relative, SOCIAL_PREVIEW_SNIPPETS)
        for snippet in snippets:
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


def check_json_ld_blocks(errors: list[str]) -> None:
    for path in sorted(ROOT.glob("*.html")):
        parser = JsonLdParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for index, block in enumerate(parser.blocks, start=1):
            if not block:
                errors.append(f"{path.name}: empty JSON-LD block #{index}")
                continue
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}: invalid JSON-LD block #{index}: {exc}")


def check_png_dimensions(errors: list[str], relative: str, expected: tuple[int, int]) -> None:
    path = ROOT / relative
    if not path.exists():
        return
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append(f"{relative}: not a PNG")
        return
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != expected:
        errors.append(f"{relative}: expected {expected[0]}x{expected[1]}, got {width}x{height}")


def check_png_size(errors: list[str]) -> None:
    check_png_dimensions(errors, "assets/social-card.png", (1200, 630))
    check_png_dimensions(errors, "assets/recruiter-card.png", (1200, 630))
    check_png_dimensions(errors, "assets/ai-backend-proof-pack-card.png", (1200, 630))
    check_png_dimensions(errors, "assets/linkedin-banner.png", (1584, 396))


def check_sitemap_lastmods(errors: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml: invalid XML: {exc}")
        return

    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    dates: dict[str, str] = {}
    for url_node in root.findall("sm:url", namespace):
        loc_node = url_node.find("sm:loc", namespace)
        lastmod_node = url_node.find("sm:lastmod", namespace)
        if loc_node is None or not loc_node.text:
            continue
        dates[loc_node.text] = lastmod_node.text if lastmod_node is not None and lastmod_node.text else ""

    for loc, expected in SITEMAP_LASTMOD_REQUIREMENTS.items():
        actual = dates.get(loc)
        if actual is None:
            errors.append(f"sitemap.xml: missing loc: {loc}")
        elif actual != expected:
            errors.append(f"sitemap.xml: expected lastmod {expected} for {loc}, got {actual}")


def check_current_evidence_snippets(errors: list[str]) -> None:
    for relative, snippets in CURRENT_EVIDENCE_SNIPPETS.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing current evidence file: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative}: missing current evidence snippet: {snippet}")


def check_pdf_artifacts(errors: list[str]) -> None:
    pdftotext = shutil.which("pdftotext")
    for relative, spec in PDF_ARTIFACTS.items():
        path = ROOT / relative
        if not path.exists():
            errors.append(f"missing PDF artifact: {relative}")
            continue
        data = path.read_bytes()
        if not data.startswith(b"%PDF-"):
            errors.append(f"{relative}: missing PDF header")
        if len(data) < 50_000:
            errors.append(f"{relative}: unexpectedly small PDF artifact")
        page_count = len(re.findall(rb"/Type\s*/Page\b", data))
        expected_pages = int(spec["pages"])
        if page_count != expected_pages:
            errors.append(f"{relative}: expected {expected_pages} page(s), got {page_count}")
        for needle in spec["required"]:
            if needle not in data:
                errors.append(f"{relative}: missing PDF byte marker: {needle.decode('utf-8', 'replace')}")
        for needle in spec["forbidden"]:
            if needle in data:
                errors.append(f"{relative}: forbidden PDF byte marker: {needle.decode('utf-8', 'replace')}")
        if pdftotext is None:
            errors.append(f"{relative}: pdftotext is required for PDF text validation")
            continue
        completed = subprocess.run(
            [pdftotext, str(path), "-"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )
        if completed.returncode != 0:
            errors.append(f"{relative}: pdftotext failed: {completed.stderr.strip()}")
            continue
        text = completed.stdout
        for needle in spec["text_required"]:
            if needle not in text:
                errors.append(f"{relative}: missing PDF text marker: {needle}")
        for needle in spec["text_forbidden"]:
            if needle in text:
                errors.append(f"{relative}: forbidden PDF text marker: {needle}")


def main() -> int:
    errors: list[str] = []
    check_required_text_key_shape(errors)
    check_required_files(errors)
    check_bad_filenames(errors)
    check_bad_patterns(errors)
    check_legacy_proof_route_references(errors)
    check_required_text(errors)
    check_social_preview_metadata(errors)
    check_profile_readme_shape(errors)
    check_local_html_links(errors)
    check_json_ld_blocks(errors)
    check_png_size(errors)
    check_pdf_artifacts(errors)
    check_sitemap_lastmods(errors)
    check_current_evidence_snippets(errors)

    if errors:
        print("public profile audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("public profile audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
