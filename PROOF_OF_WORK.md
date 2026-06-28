# Proof of Work

This page is a technical proof shortcut. It shows what I can already prove publicly and what the
private Autoschool54/DriveDesk work demonstrates without exposing private business data.

## What This Proves

| Signal | Evidence |
| --- | --- |
| I can turn a messy business domain into a backend/platform foundation. | DriveDesk Core: tenant model, RBAC, audit/outbox, business records, workflow rules, adapter boundaries, OpenAPI/SDK, CI, docs, and public demo. |
| I can use AI-assisted execution without losing verification discipline. | AI Ops Workflow Kit: document/CRM/call intake, importable n8n workflow artifact, privacy redaction before RAG/approval/CRM handoff, RAG ingestion/retrieval, deterministic RAG quality eval with citations, LLM/transcription provider boundaries, transcript analysis, lead scoring, approval queue, Telegram callback approval, dry-run CRM handoff, idempotent outbox drain, reviewer acceptance report, opt-in worker, live PostgreSQL/pgvector runtime, API restart persistence proof, deterministic tests, Docker and integration boundaries. |
| I understand operations, deployment, and recovery, not only feature code. | DeployMate: self-hosted deployment control panel direction with Docker apps, VPS targets, SSH runtime tooling, logs, health checks, CI/CD, public-review gate, evidence bundle, review packet, and release safety docs. |
| I can design trust and validation boundaries around untrusted client data. | MPlusForm: addon + Python sync pipeline with server-side validation, approved public snapshots, Windows operation scripts, and handoff docs. |
| I can support real business infrastructure remotely. | Autoschool54 / DriveDesk private work: admin/operator workflows, Telegram bot, web admin, PostgreSQL, Docker Compose, backups, deploy workflow, release preflight, docs, and recovery thinking. |

## Public Proof Links

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) - backend/platform and integration foundation.
- [DriveDesk Core public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/)
- [DriveDesk Flagship Platform](https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html) - larger backend/platform direction that connects the AI Operator slice to adapters, workflows, audit/outbox, admin/operator surfaces, DevOps, observability, and recovery.
- [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) - document/CRM/call intake, importable n8n workflow artifact, privacy redaction boundary, RAG quality eval, LLM/transcription provider boundaries, reviewer acceptance report, approvals, Telegram callback, idempotent outbox worker, live PostgreSQL/pgvector persistence, and n8n/Telegram integration boundary.
- [AI Ops demo walkthrough](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md) - committed GIF route for transcript -> RAG -> approval -> CRM-safe handoff, generated from the public-safe offer demo.
- [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) - document intake -> call-audio transcription -> transcript -> RAG -> scoring -> approval -> Telegram callback -> outbox drain -> dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight.
- [DeployMate](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot) - self-hosted deployment control panel, DevOps/platform proof snapshot, evidence bundle, and release discipline.
- [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) - trust-model, validation-boundary, desktop automation proof.

## Reviewer Shortcuts

If you only have a few minutes, review these first:

- [DriveDesk Core README](https://github.com/AlexGerlitz/drivedesk-core) - fast backend/platform reviewer route.
- [DriveDesk Core case study](https://github.com/AlexGerlitz/drivedesk-core/blob/main/docs/public/PORTFOLIO_CASE_STUDY.md) - business problem, architecture, integration model, and evidence.
- [Verification pack](./VERIFICATION_PACK.md) - current CI/demo/recovery verification links.
- [Enterprise readiness](https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html) - international employer-grade review route for backend/platform ownership, integration discipline, reliability, privacy, and async proof.
- [AI Ops demo walkthrough](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md) - short visual path for transcript -> RAG -> approval -> CRM-safe handoff.
- [AI Ops public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md) - current AI Ops CI, live smoke, local gate, Pages route, and public boundary.
- [AI Ops privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md) - PII redaction before RAG retrieval, approval context, and CRM-safe handoff.
- [AI Ops reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md) - one-command acceptance pass across live API, live smoke, GitHub Actions, Pages links, and public PDF.
- [AI Ops live Postgres persistence proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/live-postgres-persistence.txt) - live `storage=postgres` proof where a marker survives API container restart.
- [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) - one-command AI automation reviewer path.
- [AI Ops live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md) - Telegram approval callback and CRM-safe boundary proof.
- [Engineering case studies](https://alexgerlitz.github.io/AlexGerlitz/case-studies.html) - narrative problem/build/evidence summaries.
- [AI Ops Workflow Kit README](https://github.com/AlexGerlitz/ai-ops-workflow-kit#60-second-reviewer-snapshot) - 60-second AI/RAG workflow reviewer path.
- [DeployMate engineering proof snapshot](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot) - repo-first DevOps/platform proof route.
- [MPlusForm README](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot) - trust-model and desktop automation reviewer path.
- [Skill evidence matrix](./SKILL_EVIDENCE.md) - role keywords mapped to public proof.
- [Work with me](./WORK_WITH_ME.md) - fixed-scope project entry points.
- [Role targets](./ROLE_TARGETS.md) - remote backend/platform/AI automation roles mapped to proof.

## Current Public Verification

Checked on 2026-06-28:

- DriveDesk Core public demo returns HTTP 200.
- DriveDesk Core `main` is green on `228943f`.
- DriveDesk Core public CI run succeeded on `228943f`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28296918663
- DriveDesk Core GitHub Pages deployment succeeded on `228943f`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28296918404
- DriveDesk Core scheduled public validation remains green: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28282542868
- DriveDesk Core latest scheduled public demo health run succeeded: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28291540179
- DriveDesk Core has a public fast reviewer route and public demo path.
- AI Ops Workflow Kit CI workflow is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml
- AI Ops reviewer acceptance report is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md
- AI Ops latest checked CI run succeeded on `56c03fe`: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28322174530
- AI Ops demo walkthrough is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md
- AI Ops live smoke passed on app SHA `1a83406` with `storage=postgres` and `rag_eval=2/2` at https://saleops.duckdns.org.
- AI Ops live PostgreSQL/pgvector persistence proof survived an API container restart: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/live-postgres-persistence.txt
- AI Ops public proof status is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- AI Ops privacy boundary is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md
- AI Ops live approval proof is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md
- AI Ops public proof status tracks live-runtime reachability, local public gate, committed runtime evidence, LLM provider fallback state, and transcription provider state without exposing secrets: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- DeployMate default branch `develop` is green on `b139a9a`.
- DeployMate CI succeeded on `b139a9a`, including the production-contract job: https://github.com/AlexGerlitz/deploymate/actions/runs/28296918571
- DeployMate latest public evidence bundle succeeded on `b139a9a`: https://github.com/AlexGerlitz/deploymate/actions/runs/28296941763
- DeployMate release maintenance status succeeded: https://github.com/AlexGerlitz/deploymate/actions/runs/28280948309
- DeployMate release-secrets audit is green for staging and production: https://github.com/AlexGerlitz/deploymate/actions/runs/28280638779
- Profile funnel has current default-branch checks for public audit, Pages deployment, and live smoke.
- Profile proof is guarded by Profile Funnel Audit, Pages deploy, and Live Profile Smoke on `main`.
- GitHub profile proof metadata audit runs inside Live Profile Smoke for pinned repositories: `drivedesk-core`, `ai-ops-workflow-kit`, `deploymate`, `AlexGerlitz`, and `MPlusForm`.
- Profile Funnel Audit workflow: https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/profile-audit.yml?query=branch%3Amain
- Profile Pages deployment history: https://github.com/AlexGerlitz/AlexGerlitz/actions?query=branch%3Amain+workflow%3Apages-build-deployment
- Live Profile Smoke workflow: https://github.com/AlexGerlitz/AlexGerlitz/actions/workflows/live-profile-smoke.yml?query=branch%3Amain
- Live Profile Smoke includes rendered GitHub profile checks for the bio, recruiter shortcut, LinkedIn contact path, and message reason router: https://github.com/AlexGerlitz
- Work With Me and Role Targets routes are published: https://alexgerlitz.github.io/AlexGerlitz/work-with-me.html and https://alexgerlitz.github.io/AlexGerlitz/role-targets.html
- MPlusForm has a public 60-second reviewer snapshot for trust-model and validation-boundary review.
- MPlusForm `main` is green on `e0e6876`.
- MPlusForm Public Verification succeeded on `e0e6876`: https://github.com/AlexGerlitz/MPlusForm/actions/runs/28296918568
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

Start here:

- [Start conversation](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html)
- [Contact routes](https://alexgerlitz.github.io/AlexGerlitz/inbound-response.html)
- [LinkedIn Services](https://www.linkedin.com/services/page/3153b734507b8a60ab/)
