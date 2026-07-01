# Skill Evidence Matrix

This page maps role keywords and skills to public proof. It is designed for fast
technical review: pick the skill you care about, then open the proof that shows it in a real project.

For role-level matching, see [Remote Role Targets](./ROLE_TARGETS.md).

## Core Role Fit

| Role / search keyword | Evidence | Proof link |
| --- | --- | --- |
| Backend Engineer | FastAPI/PostgreSQL backend foundations, tenant model, RBAC, audit trail, outbox worker, business records, OpenAPI, tests. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Internal Tools Engineer | Operations workflow proof with adapter boundaries, SDK/OpenAPI surfaces, CI, docs, and public demo. | [DriveDesk Core fast review route](https://github.com/AlexGerlitz/drivedesk-core) |
| AI workflow / RAG proof | Document/transcript/lead intake, importable n8n workflow artifact, privacy redaction before RAG/approval/CRM handoff, RAG ingestion/retrieval, deterministic RAG quality eval with citations, OpenAI/Claude/Gemini provider boundary, call-audio transcription, transcript analysis, lead scoring, approval queues, Telegram callback approval, dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight, idempotent outbox drain, reviewer acceptance report, opt-in worker, deterministic local test paths, n8n/Telegram boundaries. | [AI Ops role requirements map](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md) |
| Support Engineer with Python | Docker runtime work, CI/CD, deployment control panel proof, health checks, logs, release gates, runbooks, recovery thinking. | [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| Integration Engineer | Explicit adapter contracts, mapping/validation mindset, CRM/ERP/1C/banking boundaries, webhooks, sync and rollout docs. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Internal Tools Engineer | Admin/operator workflow thinking, FastAPI/PostgreSQL backend surfaces, roles, records, tasks, audit, docs, deployment path. | [Proof of Work](./PROOF_OF_WORK.md) |
| Remote Operator / Builder | Autoschool54 backend/application-support work since March 2024, remote troubleshooting, workflows, docs, backups, deploy/recovery thinking. | [Role / Project Brief](./ROLE_PROJECT_BRIEF.md) |

## Skill-To-Proof Map

| Skill | What I can prove | Public evidence |
| --- | --- | --- |
| Python | Backend services, automation scripts, sync pipeline, tests, tooling. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) |
| FastAPI | Business backend foundations, AI workflow backend, service contracts. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| PostgreSQL | Business records, workflow state, PostgreSQL/pgvector-backed RAG storage, deployment data model. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| Vector Databases | RAG storage proof, PostgreSQL/pgvector-backed retrieval, source-context boundaries, and quality checks. | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DriveDesk AI Operator](./DRIVEDESK_AI_OPERATOR.md) |
| Docker / Docker Compose | Repeatable local/runtime packaging, app deployment proof, public demo and smoke flows. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| GitHub Actions / CI | Public CI, release checks, health/demo verification, repeatable proof instead of screenshots only. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| RAG / LLM Workflows | Document/transcript ingestion, call-audio transcription, privacy redaction before retrieval and handoff, deterministic RAG quality eval with expected sources and citations, OpenAI/Claude/Gemini-ready provider boundary, transcript analysis, scoring/routing, approval queue, Telegram callback approval, outbox drain, and CRM handoff foundations. | [AI Ops demo walkthrough](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md), [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md), [privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md) |
| Workflow Automation | Turning messy business processes into explicit states, records, tasks, approvals, notifications and operator handoff. | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [Proof of Work](./PROOF_OF_WORK.md) |
| Workflow Integration | Source/target contracts, API/webhook/database boundaries, sync/retry/logging paths, rollout notes, and recovery paths. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| API Integration | Adapter boundaries, contracts, mapping/validation, webhooks, and external-system integration proof. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| Customer Relationship Management (CRM) | CRM intake, lead/customer workflow proof, dry-run Bitrix CRM handoff, adapter contracts, field mapping, validation, retries, and audit logs. | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Enterprise Resource Planning (ERP) | ERP-style operations boundaries: records, roles, statuses, approvals, accounting/banking handoff proof, adapter contracts, mapping, validation, and rollout notes. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| CRM / ERP / 1C Boundaries | Integration proof for CRM/ERP/accounting/banking through explicit adapters and auditable workflows. | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Remote Services](./SERVICES.md) |
| Observability / Health Checks | Health checks, smoke checks, logs, release gates and evidence-driven verification. | [DeployMate](https://github.com/AlexGerlitz/deploymate), [Proof of Work](./PROOF_OF_WORK.md) |
| Runbooks / Handoff Docs | Operational documentation, recovery thinking, rollout notes, debugging paths. | [DeployMate](https://github.com/AlexGerlitz/deploymate), [Remote Services](./SERVICES.md) |
| Validation / Trust Boundaries | Untrusted client data separated from approved server-side snapshots, plus AI workflow redaction before RAG/approval/CRM boundaries. | [MPlusForm reviewer snapshot](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot), [public verification run](https://github.com/AlexGerlitz/MPlusForm/actions/runs/28296918568), [AI Ops privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md) |
| Windows Automation | Sync helper packaging and Windows operation scripts around a desktop-side automation flow. | [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) |

## AI-Native Delivery Discipline

| Signal | What I can prove | Public evidence |
| --- | --- | --- |
| Fast problem decomposition | I use AI tooling to turn unclear business requests into workflow maps, risky assumptions, first slices, and verification routes. | [Start conversation](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html), [Decision-ready contact](https://alexgerlitz.github.io/AlexGerlitz/decision-ready-contact.html) |
| Engineering ownership | AI tooling compresses discovery, implementation, debugging, docs, and review, while architecture, state, tests, privacy boundaries, deployment, logs, and shipped quality stay my responsibility. | [Hiring decision](https://alexgerlitz.github.io/AlexGerlitz/hiring-decision.html), [Enterprise readiness](https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html) |
| Verification habit | Outputs are checked through code inspection, tests, smoke routes, CI, live proof, docs, and runbooks instead of being trusted as generated text. | [Verification pack](https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html), [AI Ops reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md) |
| Full-cycle delivery | I can move from problem shape to backend slice, integration boundary, deployment path, operator handoff, and next-phase plan. | [First month plan](https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html), [DriveDesk proof route](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html) |

## Evidence By Project

| Project | Best evidence for | Fast review path |
| --- | --- | --- |
| DriveDesk Core | Backend automation and integration engineering, adapter boundaries, SaaS foundation, operations workflow proof. | [Fast review route](https://github.com/AlexGerlitz/drivedesk-core) |
| AI Ops Workflow Kit | AI automation, DriveDesk AI Operator-style RAG/transcript workflows, hiring signal brief, business scenario replay, first-slice playbook, committed demo GIF/walkthrough, deterministic RAG quality eval, privacy redaction before RAG/approval/CRM handoff, LLM/transcription provider boundaries, transcript processing, Telegram approvals, CRM-safe outbox handoff, retry/dead-letter behavior, live PostgreSQL/pgvector persistence, reviewer acceptance report, reviewer observability snapshot, live approval proof, CI, and integration boundaries. | [hiring signal brief](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/hiring-signal-brief.txt), [business scenario replay](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/business-scenario-replay.txt), [First Slice Playbook](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/FIRST_SLICE_PLAYBOOK.md), [demo walkthrough](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md), [public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), [live Postgres persistence proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/live-postgres-persistence.txt), [privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md), [reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md), [live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md), [latest CI run](https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28344277704), [repo](https://github.com/AlexGerlitz/ai-ops-workflow-kit) |
| DeployMate | Docker/CI handoff, self-hosting, deployment automation, health checks, runbooks, release discipline. | [Engineering proof snapshot](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot) |
| MPlusForm | Trust model, validation boundaries, Python/Lua/PowerShell automation, Windows operations, public verification gate. | [60-second reviewer snapshot](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot), [public verification run](https://github.com/AlexGerlitz/MPlusForm/actions/runs/28296918568) |

## Best Skills To Evaluate

These are the skills that best match the public proof above:

- AI Automation
- Backend Development
- Python
- FastAPI
- PostgreSQL
- Vector Databases
- Docker
- Docker/CI handoff
- GitHub Actions
- RAG
- Workflow Integration
- API Integration
- Customer Relationship Management (CRM)
- Enterprise Resource Planning (ERP)
- Workflow Automation
- Internal Tools
- Internal Tools Engineering
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
