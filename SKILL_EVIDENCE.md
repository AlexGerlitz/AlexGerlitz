# Skill Evidence Matrix

This page maps role keywords and skills to public proof. It is designed for fast
technical review: pick the skill you care about, then open the proof that shows it in a real project.

For role-level matching, see [Remote Role Targets](./ROLE_TARGETS.md).

## Core Role Fit

| Role / search keyword | Evidence | Proof link |
| --- | --- | --- |
| Backend Engineer | FastAPI/PostgreSQL backend foundations, tenant model, RBAC, audit trail, outbox worker, business records, OpenAPI, tests. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Platform Engineer | Operations platform direction with adapter boundaries, SDK/OpenAPI surfaces, CI, docs, and public demo. | [DriveDesk Core fast review route](https://github.com/AlexGerlitz/drivedesk-core) |
| AI Automation Engineer | Document/transcript/lead intake, importable n8n workflow artifact, RAG ingestion/retrieval, OpenAI/Claude/Gemini provider boundary, call-audio transcription, transcript analysis, lead scoring, approval queues, Telegram callback approval, dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight, idempotent outbox drain, reviewer acceptance report, opt-in worker, deterministic local test paths, n8n/Telegram boundaries. | [AI Ops role requirements map](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md) |
| DevOps Engineer | Docker runtime work, CI/CD, deployment control panel direction, health checks, logs, release gates, runbooks, recovery thinking. | [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| Integration Engineer | Explicit adapter contracts, mapping/validation mindset, CRM/ERP/1C/banking boundary direction, webhooks, sync and rollout docs. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Internal Tools Engineer | Admin/operator workflow thinking, FastAPI/PostgreSQL backend surfaces, roles, records, tasks, audit, docs, deployment path. | [Proof of Work](./PROOF_OF_WORK.md) |
| Remote Operator / Builder | Autoschool54 digital infrastructure support since March 2024, remote troubleshooting, workflows, docs, backups, deploy/recovery thinking. | [Role / Project Brief](./ROLE_PROJECT_BRIEF.md) |

## Skill-To-Proof Map

| Skill | What I can prove | Public evidence |
| --- | --- | --- |
| Python | Backend services, automation scripts, sync pipeline, tests, tooling. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) |
| FastAPI | Business backend foundations, AI workflow backend, service contracts. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| PostgreSQL | Business records, workflow state, pgvector-ready storage direction, deployment data model. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| Docker / Docker Compose | Repeatable local/runtime packaging, app deployment direction, public demo and smoke flows. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| GitHub Actions / CI | Public CI, release checks, health/demo verification, repeatable proof instead of screenshots only. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| RAG / LLM Workflows | Document/transcript ingestion, call-audio transcription, retrieval, OpenAI/Claude/Gemini-ready provider boundary, transcript analysis, scoring/routing, approval queue, Telegram callback approval, outbox drain, and CRM handoff foundations. | [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) |
| Workflow Automation | Turning messy business processes into explicit states, records, tasks, approvals, notifications and operator handoff. | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [Proof of Work](./PROOF_OF_WORK.md) |
| API Integration | Adapter boundaries, contracts, mapping/validation, webhooks and external-system integration direction. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| CRM / ERP / 1C Boundaries | Product direction for CRM/ERP/accounting/banking integration through explicit adapters and auditable workflows. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| Observability / Health Checks | Health checks, smoke checks, logs, release gates and evidence-driven verification. | [DeployMate](https://github.com/AlexGerlitz/deploymate), [Proof of Work](./PROOF_OF_WORK.md) |
| Runbooks / Handoff Docs | Operational documentation, recovery thinking, rollout notes, debugging paths. | [DeployMate](https://github.com/AlexGerlitz/deploymate), [Remote Services](./SERVICES.md) |
| Validation / Trust Boundaries | Untrusted client data separated from approved server-side snapshots and documented validation ownership. | [MPlusForm reviewer snapshot](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot) |
| Windows Automation | Sync helper packaging and Windows operation scripts around a desktop-side automation flow. | [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) |

## Evidence By Project

| Project | Best evidence for | Fast review path |
| --- | --- | --- |
| DriveDesk Core | Backend/platform engineering, adapter boundaries, SaaS foundation, operations platform direction. | [Fast review route](https://github.com/AlexGerlitz/drivedesk-core) |
| AI Ops Workflow Kit | AI automation, DriveDesk AI Operator-style RAG/transcript workflows, LLM/transcription provider boundaries, transcript processing, Telegram approvals, outbox worker handoff, reviewer acceptance report, live approval proof, CI, and integration boundaries. | [Public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), [reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md), [live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md), [latest CI run](https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28170669049), [repo](https://github.com/AlexGerlitz/ai-ops-workflow-kit) |
| DeployMate | DevOps, self-hosting, deployment automation, health checks, runbooks, release discipline. | [Reviewer package](https://github.com/AlexGerlitz/deploymate#reviewer-package) |
| MPlusForm | Trust model, validation boundaries, Python/Lua/PowerShell automation, Windows operations. | [60-second reviewer snapshot](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot) |

## Best Skills To Evaluate

These are the skills that best match the public proof above:

- AI Automation
- Backend Development
- Python
- FastAPI
- PostgreSQL
- Docker
- DevOps
- GitHub Actions
- RAG
- API Integration
- Workflow Automation
- Internal Tools
- Platform Engineering
- Observability
- Technical Documentation
- Runbooks
- Data Validation
- Windows Automation

## How To Test Fit Quickly

Give me one of these:

- a messy operator workflow;
- an API, database, CRM, ERP, 1C, or banking boundary;
- a document/call-audio/transcript/ticket flow that needs AI assistance;
- a self-hosted service with deployment, logging, backup, or recovery pain;
- an internal tool idea that currently lives in chats or spreadsheets.

I will map the problem to a small working slice, identify the risky assumptions, and show what can
be proven first with code, tests, logs, smoke checks, and docs.
