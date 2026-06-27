# Enterprise Readiness

Public route: https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html

This is the proof route for international employer-grade review: teams that need a reliable backend/platform owner, not a prompt-only or no-code workflow operator.

## What To Inspect

| Review signal | Public evidence | Why it matters |
| --- | --- | --- |
| Backend/platform ownership | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Core review](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html), [Flagship platform](https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html) | FastAPI/PostgreSQL, roles, records, audit/outbox, adapters, OpenAPI, Docker, tests, CI, and public demo direction. |
| AI workflow engineering | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [Public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), [Live owner proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md) | RAG quality eval, transcript analysis, Telegram approval, CRM-safe handoff, live PostgreSQL/pgvector storage, and reviewer evidence. |
| Reliability and operations | [Verification pack](https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html), [DeployMate](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot), CI checks, runbooks, and smoke routes | Behavior is checked through commands, CI, health routes, release gates, docs, and recovery-oriented proof. |
| Privacy and integration discipline | [Privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md), Bitrix dry-run contract, Telegram callback evidence, and CRM outbox state | Sensitive input, approvals, and CRM mutations are handled through explicit boundaries instead of hidden workflow glue. |
| International team fit | [AI Backend Proof Pack](https://alexgerlitz.github.io/AlexGerlitz/ai-backend-proof-pack.html), [llms.txt](https://alexgerlitz.github.io/AlexGerlitz/llms.txt), [Verification pack](https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html), and [Start conversation](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html) | English-first docs, async review paths, explicit ownership boundaries, and compact evidence routes make the profile reviewable without a live walkthrough. |
| Remote review clarity | [Start conversation](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html), [Role fit](https://alexgerlitz.github.io/AlexGerlitz/role-fit.html), [First month plan](https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html), [PDF resume](https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf) | Recruiters, hiring managers, and technical reviewers get a short path from role/project context to verifiable proof. |

## International Employer Signals

- Qualification depth: backend/platform work, AI workflow engineering, CRM/ERP/API integration, DevOps, and support of real business infrastructure are tied to public proof.
- Enterprise constraints: privacy boundaries, approvals, audit trail, retries, idempotency, rollback thinking, and runbooks are visible instead of hidden behind workflow glue.
- Business-system context: DriveDesk focuses on documents, transcripts, leads, operator queues, CRM handoff, records, roles, payments, logs, backups, and recovery paths.
- Async review quality: English-first docs, proof routes, CI, smoke checks, and compact evidence make it possible to evaluate work across time zones.
- Team onboarding signal: first-month ownership, smallest responsible slice, verification plan, and handoff route are explicit before a project or role starts.

## Operating Principle

I use AI tooling to move faster, but I keep responsibility for architecture, state, integration contracts, tests, deployment, docs, evidence, and shipped behavior.

The main engineering distinction: n8n can orchestrate events, while backend code owns state, RAG, approvals, adapter contracts, audit, retries, idempotency, and verification.

## International Team Fit

- English-first public docs and proof routes so recruiters, hiring managers, and technical reviewers can inspect work asynchronously.
- Short evidence path: proof pack, flagship route, enterprise readiness, verification pack, resume, and current CI/live smoke status.
- Clear ownership boundaries: what the backend owns, what orchestration owns, what is dry-run/sandboxed, and what must be approved before external writes.
- Handoff discipline: tests, logs, runbooks, public-safe evidence, and smallest responsible first slice instead of vague "AI automation" claims.

## Best Fit

- Remote backend/platform roles with Python, FastAPI, PostgreSQL, Docker, CI, integrations, internal tools, or DevOps ownership.
- AI automation roles where RAG, transcripts, approvals, CRM/ERP/API boundaries, and quality checks must be inspectable.
- Fixed-scope workflow projects where the output is a working slice with tests, logs, docs, runbook, and handoff route.

## Next Stronger Proof

Keep extending DriveDesk AI Operator with a visible observability dashboard, integration drill, real sandbox adapter proof, and a short demo video/GIF once the runtime is stable.
