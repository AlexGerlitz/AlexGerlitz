#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
import struct
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
    "drivedesk-proof-route.html",
    "drivedesk-ai-operator.html",
    "projects.html",
    "case-studies.html",
    "proof.html",
    "PROOF_OF_WORK.md",
    "first-30-days.html",
    "fixed-scope-offers.html",
    "services.html",
    "inbound-response.html",
    "intake-brief.html",
    "skill-evidence.html",
    "one-page-brief.html",
    "resume.html",
    "resume-pdf.html",
    "application-pack.html",
    "START_HERE.md",
    "APPLICATION_PACK.md",
    "RESUME.md",
    "SERVICES.md",
    "INBOUND_RESPONSE_PACK.md",
    "INTAKE_BRIEF.md",
    "WORK_WITH_ME.md",
    "SKILL_EVIDENCE.md",
    "ROLE_TARGETS.md",
    "AI_AUTOMATION_ROLE_FIT.md",
    "CASE_STUDIES.md",
    "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf",
    "assets/linkedin-banner.png",
    "assets/linkedin-banner.svg",
    "assets/social-card.png",
    "assets/social-card.svg",
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
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint, or DriveDesk AI Operator-style proof route.",
        "Decision routes",
        "Inbound / contact",
        "DriveDesk Proof Route",
        "AI-readable proof index",
        "https://alexgerlitz.github.io/AlexGerlitz/llms.txt",
        "hiring-decision.html",
        "skill evidence",
        "pinned proof repos",
        "Live owner proof",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "https://alexgerlitz.github.io/AlexGerlitz/projects.html",
        "https://alexgerlitz.github.io/AlexGerlitz/case-studies.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "https://alexgerlitz.github.io/AlexGerlitz/services.html",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
        "Inbound Brief",
        "remote-only full-time roles",
        "first month plan",
        "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html",
        "Fast fit checklist",
        "message me when the work is remote-only",
        "I am not positioning for onsite-only roles",
        "student/course assignments",
        "generic mobile/ecommerce apps without backend/integration ownership",
    ],
    "index.html": [
        '<link rel="icon" href="./assets/favicon.svg" type="image/svg+xml">',
        "./drivedesk-proof-route.html",
        "./hiring-decision.html",
        "./projects.html",
        "./case-studies.html",
        "https://www.linkedin.com/services/page/3153b734507b8a60ab/",
        "Now open for remote-only backend/platform",
        "Search-fit titles: Back End Developer, Python Developer",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter",
        "DriveDesk proof route",
        "Case studies",
        "Open technical proof path",
        "DriveDesk AI Operator",
        "./skill-evidence.html",
        "Skill evidence",
        "./services.html",
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
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
        'property="og:image:width" content="1200"',
        'property="og:image:height" content="630"',
        'name="twitter:card" content="summary_large_image"',
        "One-minute hiring decision route",
        "I build backend-owned AI workflow and operations systems for real businesses.",
        "remote-only full-time roles",
        "Best-fit roles",
        "Main proof",
        "Hiring signal",
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
    "role-fit.html": [
        "AI Ops proof status",
        "Live owner proof",
        "AI Ops CI workflow",
        "Search-fit role targets",
        "./skill-evidence.html",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
        "Python Backend Engineer",
        "LLM Workflow / RAG Engineer",
        "n8n AI Workflow Engineer",
        "./ROLE_TARGETS.md",
    ],
    "resume.html": [
        "<title>Resume - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/resume.html"',
        "DriveDesk AI Operator proof route",
        "Fast fit checklist: remote-only work with a concrete technical outcome",
        "Not my target right now: onsite-only roles",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
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
        "Remote AI automation, backend/platform, integration, and DevOps work.",
        "Fast fit checklist: remote-only work, concrete technical outcome",
        "Not my target right now: onsite-only roles",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
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
        "Role Fit Pack",
        "PDF Resume",
        "Fast Decision Signals",
        "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "useful first outcome: working slice with tests, docs, and handoff.",
    ],
    "APPLICATION_PACK.md": [
        "Role Fit Pack",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
        "Fast fit checklist: remote-only work, concrete technical outcome",
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
        "right now: onsite-only roles",
        "Artificial Intelligence Engineer with a workflow/backend focus",
        "PDF resume for application upload",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
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
        "Not my target right now: isolated brochure/static websites",
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
        "Best Immediate Starts",
        "Good Fit Filter",
        "Not my target right now: isolated brochure/static websites",
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
        "GitHub-readable services page",
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
    "skill-evidence.html": [
        "<title>Skill Evidence - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html"',
        "Skill-to-proof map",
        "Skills mapped to public proof.",
        "AI Automation / RAG",
        "Backend / Platform",
        "CRM / ERP Integration",
        "DevOps / Self-Hosting",
        "Best Skills To Evaluate",
        "./SKILL_EVIDENCE.md",
        "DriveDesk Core",
        "AI Ops Workflow Kit",
    ],
    "ROLE_TARGETS.md": [
        "Remote Role Targets",
        "Systems Integration Engineer",
        "Back End Developer / Python Developer",
        "Artificial Intelligence Engineer",
        "Customer Relationship Management (CRM) Engineer",
        "Enterprise Resource Planning (ERP) Engineer",
        "Vector Databases Engineer",
    ],
    "AI_AUTOMATION_ROLE_FIT.md": [
        "AI Automation Role Fit",
        "Vector Databases",
        "pgvector-ready storage",
        "CRM / Bitrix / API handoff",
        "Live owner proof",
        "Live Telegram approval evidence",
        "AI Ops CI workflow",
    ],
    "start-conversation.html": [
        "Current Public Proof",
        "Live owner proof",
        "AI Operator case",
        "./skill-evidence.html",
        "Open skill evidence",
        "./intake-brief.html",
        "Inbound brief",
        "Fast Decision Routes",
        "Fast Decision Signals",
        "./assets/copy-blocks.css",
        "./assets/copy-blocks.js",
        "DriveDesk proof route",
        "Useful first outcome: working slice with tests, docs, and handoff.",
        "Verification pack",
        "role fit and first-month ownership",
        "whether a practical first slice can ship quickly",
        "First month plan",
        "Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps recovery sprint, or DriveDesk AI Operator-style proof route.",
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
        "DeployMate - Self-hosted Docker Deployment Control Panel",
    ],
    "case-studies.html": [
        "<title>Engineering Case Studies - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/case-studies.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/case-studies.html"',
        "Problem, build, evidence, and operating proof",
        "DriveDesk / Autoschool54 Operations Platform Direction",
        "AI Ops Workflow Kit",
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
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
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
        "Message on LinkedIn",
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
    "first-30-days.html": [
        "<title>First Month Delivery Plan - Alex Gerlitz</title>",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:url" content="https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html"',
        'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
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
        "DriveDesk AI Operator proof-route alias",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "This proof-route alias opens",
    ],
    "featured-drivedesk.html": [
        "DriveDesk AI Operator proof-route alias",
        'rel="canonical" href="https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html"',
        '<meta http-equiv="refresh" content="0; url=./drivedesk-proof-route.html">',
        "This proof-route alias opens",
    ],
    "ONE_PAGE_BRIEF.md": [
        "DriveDesk AI Operator Proof Route Alias",
        "markdown alias points to the canonical public proof route",
        "DriveDesk AI Operator proof route",
        "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
    ],
    "resume-pdf.html": [
        "Proof route: alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "building DriveDesk AI Operator proof",
        "Search-fit titles: Back End Developer, Python Developer",
        "Fast fit: remote-only work with a concrete technical outcome",
        "Search-match stack: Python, FastAPI, PostgreSQL, Docker, RAG, n8n, Telegram, CRM/ERP/API",
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
        "role fit and first-month ownership",
        "whether a practical first slice can ship quickly",
        "best proof route: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html",
        "useful first outcome: working slice with tests, docs, and handoff.",
        "DriveDesk Proof Route",
        "Inbound brief",
        "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html",
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
        "Hiring decision route",
        "Skill evidence map",
        "Verification pack",
        "Remote-only backend, platform, DevOps, AI automation",
        "backend-owned AI workflows, CRM/ERP/API adapters",
        "AI Ops Workflow Kit",
        "LinkedIn Services",
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
        "https://alexgerlitz.github.io/AlexGerlitz/llms.txt",
    ],
}

SOCIAL_PREVIEW_PAGES = [
    "index.html",
    "hiring-decision.html",
    "drivedesk-proof-route.html",
    "projects.html",
    "case-studies.html",
    "role-fit.html",
    "skill-evidence.html",
    "proof.html",
    "fixed-scope-offers.html",
    "services.html",
    "start-conversation.html",
    "resume.html",
    "application-pack.html",
    "first-30-days.html",
    "inbound-response.html",
    "intake-brief.html",
]

SOCIAL_PREVIEW_SNIPPETS = [
    'property="og:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
    'property="og:image:secure_url" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
    'property="og:image:type" content="image/png"',
    'property="og:image:width" content="1200"',
    'property="og:image:height" content="630"',
    'property="og:image:alt"',
    'name="twitter:card" content="summary_large_image"',
    'name="twitter:image" content="https://alexgerlitz.github.io/AlexGerlitz/assets/social-card.png?v=2026-06-26-decision-route"',
    'name="twitter:image:alt"',
]

SITEMAP_LASTMOD_REQUIREMENTS = {
    "https://alexgerlitz.github.io/AlexGerlitz/": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/llms.txt": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/VERIFICATION_PACK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/PROOF_OF_WORK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/SKILL_EVIDENCE.md": "2026-06-26",
    "https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/INTAKE_BRIEF.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/INBOUND_RESPONSE_PACK.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/ROLE_PROJECT_BRIEF.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/START_HERE.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/fixed-scope-offers.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/services.html": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/SERVICES.md": "2026-06-27",
    "https://alexgerlitz.github.io/AlexGerlitz/WORK_WITH_ME.md": "2026-06-27",
}

CURRENT_EVIDENCE_SNIPPETS = {
    "VERIFICATION_PACK.md": [
        "Last checked: 2026-06-27.",
        "DriveDesk Core `main` is green on `633e92a`.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28278340108",
        "AI Ops latest checked CI run succeeded on `99667b9`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28203298763",
        "DeployMate default branch `develop` is green on `237b2c9`.",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "MPlusForm `main` is current on `9c55283`",
    ],
    "PROOF_OF_WORK.md": [
        "Checked on 2026-06-27:",
        "DriveDesk Core `main` is green on `633e92a`.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28278340108",
        "AI Ops latest checked CI run succeeded on `99667b9`",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28203298763",
        "DeployMate default branch `develop` is green on `237b2c9`.",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "MPlusForm `main` is current on `9c55283`.",
    ],
    "verification-pack.html": [
        "Last checked: 2026-06-27.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28278340108",
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28203298763",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28281348824",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309",
        "https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779",
        "<code>633e92a</code>",
        "<code>99667b9</code>",
        "<code>237b2c9</code>",
    ],
    "drivedesk-core-review.html": [
        "Public demo checked on 2026-06-27.",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868",
        "https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28278340108",
    ],
    "SKILL_EVIDENCE.md": [
        "https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28203298763",
    ],
}

PDF_ARTIFACTS = {
    "output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf": {
        "pages": 1,
        "required": [],
        "forbidden": [
            b"file://",
            b"Users/alexgerlitz",
            b"Documents/Codex",
            b"new-chat",
            b"27.06.",
            b"AI-generated",
            b"One-Page Brief",
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
