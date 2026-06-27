# Enterprise Readiness

Public route: https://alexgerlitz.github.io/AlexGerlitz/enterprise-readiness.html

This is the proof route for international remote teams that need a reliable backend/platform owner, not a prompt-only or no-code workflow operator.

## What To Inspect

| Review signal | Public evidence | Why it matters |
| --- | --- | --- |
| Backend/platform ownership | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [Core review](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html), [Flagship platform](https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html) | FastAPI/PostgreSQL, roles, records, audit/outbox, adapters, OpenAPI, Docker, tests, CI, and public demo direction. |
| AI workflow engineering | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit), [Public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), [Live owner proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md) | RAG quality eval, transcript analysis, Telegram approval, CRM-safe handoff, live PostgreSQL/pgvector storage, and reviewer evidence. |
| Reliability and operations | [Verification pack](https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html), [DeployMate](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot), CI checks, runbooks, and smoke routes | Behavior is checked through commands, CI, health routes, release gates, docs, and recovery-oriented proof. |
| Privacy and integration discipline | [Privacy boundary](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PRIVACY_BOUNDARY.md), Bitrix dry-run contract, Telegram callback evidence, and CRM outbox state | Sensitive input, approvals, and CRM mutations are handled through explicit boundaries instead of hidden workflow glue. |
| Remote review clarity | [Start conversation](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html), [Role fit](https://alexgerlitz.github.io/AlexGerlitz/role-fit.html), [First month plan](https://alexgerlitz.github.io/AlexGerlitz/first-30-days.html), [PDF resume](https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-remote-ai-automation-resume.pdf) | Recruiters, hiring managers, and technical reviewers get a short path from role/project context to verifiable proof. |

## Operating Principle

I use AI tooling to move faster, but I keep responsibility for architecture, state, integration contracts, tests, deployment, docs, evidence, and shipped behavior.

The main engineering distinction: n8n can orchestrate events, while backend code owns state, RAG, approvals, adapter contracts, audit, retries, idempotency, and verification.

## Best Fit

- Remote backend/platform roles with Python, FastAPI, PostgreSQL, Docker, CI, integrations, internal tools, or DevOps ownership.
- AI automation roles where RAG, transcripts, approvals, CRM/ERP/API boundaries, and quality checks must be inspectable.
- Fixed-scope workflow projects where the output is a working slice with tests, logs, docs, runbook, and handoff route.

## Next Stronger Proof

Keep extending DriveDesk AI Operator with a visible observability dashboard, integration drill, real sandbox adapter proof, and a short demo video/GIF once the runtime is stable.
