# Proof of Work

This page is a technical proof shortcut. It shows what I can already prove publicly and what the
private Autoschool54/DriveDesk work demonstrates without exposing private business data.

## What This Proves

| Signal | Evidence |
| --- | --- |
| I can turn a messy business domain into a backend/platform foundation. | DriveDesk Core: tenant model, RBAC, audit/outbox, business records, workflow rules, adapter boundaries, OpenAPI/SDK, CI, docs, and public demo. |
| I can use AI as an engineering multiplier without losing verification discipline. | AI Ops Workflow Kit: document/CRM/call intake, importable n8n workflow artifact, RAG ingestion/retrieval, LLM/transcription provider boundaries, transcript analysis, lead scoring, approval queue, Telegram callback approval, dry-run CRM handoff, idempotent outbox drain, reviewer acceptance report, opt-in worker, pgvector-ready storage, deterministic tests, Docker and integration boundaries. |
| I understand operations, deployment, and recovery, not only feature code. | DeployMate: self-hosted deployment control panel direction with Docker apps, VPS targets, SSH runtime tooling, logs, health checks, CI/CD, and release safety docs. |
| I can design trust and validation boundaries around untrusted client data. | MPlusForm: addon + Python sync pipeline with server-side validation, approved public snapshots, Windows operation scripts, and handoff docs. |
| I can support real business infrastructure remotely. | Autoschool54 / DriveDesk private work: admin/operator workflows, Telegram bot, web admin, PostgreSQL, Docker Compose, backups, deploy workflow, release preflight, docs, and recovery thinking. |

## Public Proof Links

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) - backend/platform and integration foundation.
- [DriveDesk Core public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/)
- [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) - document/CRM/call intake, importable n8n workflow artifact, RAG, LLM/transcription provider boundaries, reviewer acceptance report, approvals, Telegram callback, idempotent outbox worker, and n8n/Telegram integration boundary.
- [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) - document intake -> call-audio transcription -> transcript -> RAG -> scoring -> approval -> Telegram callback -> outbox drain -> dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight.
- [DeployMate](https://github.com/AlexGerlitz/deploymate) - self-hosted deployment control panel and release discipline.
- [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) - trust-model, validation-boundary, desktop automation proof.

## Reviewer Shortcuts

If you only have a few minutes, review these first:

- [DriveDesk Core README](https://github.com/AlexGerlitz/drivedesk-core) - fast backend/platform reviewer route.
- [DriveDesk Core case study](https://github.com/AlexGerlitz/drivedesk-core/blob/main/docs/public/PORTFOLIO_CASE_STUDY.md) - business problem, architecture, integration model, and evidence.
- [Verification pack](./VERIFICATION_PACK.md) - current CI/demo/incident verification links.
- [AI Ops public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md) - current AI Ops CI, live smoke, local gate, Pages route, and public boundary.
- [AI Ops reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md) - one-command acceptance pass across live API, live smoke, GitHub Actions, Pages links, and public PDF.
- [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) - one-command AI automation reviewer path.
- [AI Ops live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md) - Telegram approval callback and CRM-safe boundary proof.
- [Engineering case studies](./CASE_STUDIES.md) - narrative problem/build/evidence summaries.
- [AI Ops Workflow Kit README](https://github.com/AlexGerlitz/ai-ops-workflow-kit#60-second-reviewer-snapshot) - 60-second AI/RAG workflow reviewer path.
- [DeployMate README](https://github.com/AlexGerlitz/deploymate#reviewer-package) - repo-first DevOps/platform reviewer package.
- [MPlusForm README](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot) - trust-model and desktop automation reviewer path.
- [Skill evidence matrix](./SKILL_EVIDENCE.md) - role keywords mapped to public proof.
- [Work with me](./WORK_WITH_ME.md) - fixed-scope project entry points.

## Current Public Verification

Checked on 2026-06-25:

- DriveDesk Core public demo returns HTTP 200.
- DriveDesk Core latest public CI run succeeded on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553622
- DriveDesk Core latest GitHub Pages deployment succeeded on `1c04111`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553066
- DriveDesk Core public demo health run was successful on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28161509901
- DriveDesk Core public scheduled validation succeeded on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28155499567
- DriveDesk Core has a public fast reviewer route and public demo path.
- AI Ops Workflow Kit CI workflow is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml
- AI Ops reviewer acceptance report is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md
- AI Ops latest checked CI run succeeded on `9099b52`: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28172015560
- AI Ops public proof status is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- AI Ops live approval proof is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md
- AI Ops public proof status tracks live-runtime reachability, local public gate, committed runtime evidence, LLM provider fallback state, and transcription provider state without exposing secrets: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- DeployMate release-gate and production-contract verification passed on the latest release-audit
  repair run; staging deploy and scheduled release-secrets audit remain open owner-confirmed
  known_hosts recovery items.
- MPlusForm has a public 60-second reviewer snapshot for trust-model and validation-boundary review.
- Public proof repositories are reachable.

## DriveDesk Core Case Study

DriveDesk Core is the public foundation for the DriveDesk direction: one operational
layer for CRM/ERP/accounting/banking integrations, documents, tasks, notifications, AI workflows,
deployment, observability, and recovery.

The important part is not "integrates with everything" as a slogan. The important part is the
engineering shape:

- explicit adapter contracts instead of hidden glue;
- tenant-aware backend boundaries;
- RBAC and audit trail for operational accountability;
- outbox/worker pattern for async business processes;
- OpenAPI/SDK surfaces for integration and review;
- Docker/CI/docs so the system can be run and verified;
- public demo so the work is inspectable without private data.

That maps directly to the work I want: business-process automation, internal tools, AI/RAG
workflows, integration adapters, backend/platform systems, DevOps hardening, and remote fixed-scope
projects where the output must be operated after the first demo.

## Fast Proof Review

Give me:

- one messy workflow;
- one success condition;
- the systems/data involved;
- the hard constraints: access, deadline, budget, stack, hosting, compliance, language.

I will break the problem down, identify risky assumptions, propose the smallest responsible build,
and show what can be proven quickly with tests, logs, smoke checks, docs, and a working slice.
