# DriveDesk Flagship Platform Direction

## Sharpest Current Demo: DriveDesk AI Operator

The main killer-demo direction is now [DriveDesk AI Operator](./DRIVEDESK_AI_OPERATOR.md): an AI
sales and support workflow platform.

Scenario:

```text
document, call transcript, external file export, or CRM lead
-> ingestion
-> RAG retrieval with citations
-> call analysis JSON
-> lead score / risks / missing info / tasks
-> follow-up draft
-> Telegram approval
-> CRM task/comment through adapter contract
```

The important selling point: I am not just gluing no-code nodes together. Backend owns state, RAG,
audit, retries, idempotency, quality checks, approvals, and integration contracts. n8n is the
orchestration layer.

DriveDesk is the long-term product direction behind my public proof projects: one remote-first
operating layer for real business workflows, integrations, AI assistance, deployment, observability,
and recovery.

The target is not a vague "integrates with everything" promise. The target is a platform that can
connect systems like CRM, ERP, 1C, banking/accounting tools, custom databases, documents, operator
queues, notifications, and admin workflows through explicit adapters, contracts, logs, tests, and
rollout steps.

## Why This Direction Matters

This direction combines the surfaces remote teams and founders usually need in one technical story:

- backend/platform ownership;
- integration architecture;
- AI workflow automation;
- DevOps and recovery discipline;
- product execution from messy business context to a working system.

Since March 2024, I have supported Autoschool54 digital infrastructure remotely and used that
operational context to shape DriveDesk. The private work is the real business context; the public
repos are the inspectable proof path.

## What DriveDesk Is Trying To Become

An operations platform where different roles can work from one reliable layer:

| Role / user | What the platform should make easier |
| --- | --- |
| Owner / manager | See current work, risks, money/status signals, unresolved issues, and audit history. |
| Operator / support | Handle records, tasks, documents, chats, approvals, and exceptions without manual handoff chaos. |
| Accountant / finance | Work through explicit banking/accounting boundaries, payment records, exports, and reconciliation steps. |
| Admin / coordinator | Manage schedules, users, permissions, notifications, files, and operational handoff. |
| Technical owner | Inspect integrations, logs, retries, health checks, releases, backups, and recovery paths. |

## Architecture Map

| Layer | Responsibility |
| --- | --- |
| Core backend | Tenants, users, roles, records, workflows, audit trail, outbox, OpenAPI surface. |
| Adapter layer | 1C, CRM, ERP, bank/accounting API, webhooks, custom database, spreadsheet, and file contracts. |
| Workflow layer | Tasks, approvals, status transitions, routing, notifications, operator queues, exception handling. |
| AI layer | Document/transcript/ticket analysis, summaries, retrieval, scoring, routing suggestions, draft actions. |
| Admin / operator UI | Human review, corrections, approval, search, dashboards, and operational controls. |
| DevOps layer | Docker, CI/release gates, health checks, logs, backups, smoke checks, rollback and recovery docs. |

## Current Public Proof

| Proof | What it demonstrates |
| --- | --- |
| [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) | FastAPI/PostgreSQL SaaS/backend foundation with tenants, RBAC, audit/outbox, adapter boundaries, OpenAPI, CI, docs, and public demo. |
| [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md) | One-command AI workflow demo: document/transcript/lead intake, retrieval, OpenAI/Claude/Gemini provider boundary, transcript/document analysis, lead scoring, approvals, Telegram callback approval, dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight, idempotent outbox drain, opt-in worker, deterministic tests, and integration boundaries. |
| [DeployMate](https://github.com/AlexGerlitz/deploymate) | DevOps/release proof: deployment control panel direction, SSH/runtime surface, health checks, release gates, runbooks, and incident handling. |
| [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) | Trust-boundary proof around sync, validation, client-side data, server checks, Windows automation, and operator docs. |
| [Verification Pack](./VERIFICATION_PACK.md) | Reviewer route through demos, CI, docs, role evidence, and operational proof. |

## How I Would Build The First Real Slice

1. Choose one valuable workflow instead of trying to automate the whole company at once.
2. Map the current tools, data sources, manual steps, failure modes, and access constraints.
3. Define the first records, roles, permissions, statuses, and audit events.
4. Build one adapter or import/export boundary with validation and traceability.
5. Add one operator workflow, AI assist step, or approval queue.
6. Deploy with Docker, smoke checks, logs, backup notes, and a recovery path.
7. Use the evidence from that slice to choose the next adapter or workflow.

Good first slices:

- DriveDesk AI Operator: transcript/lead upload, RAG, call analysis JSON, Telegram approval, and
  fake CRM/Bitrix adapter with idempotency, retries, audit log, and dead-letter handling;
- one CRM/1C/banking/custom database integration adapter;
- one document/ticket/order workflow with AI summarization and human approval;
- one internal admin panel replacing spreadsheet/chat operations;
- one deployment/recovery hardening sprint for an existing service;
- one operating dashboard with logs, health checks, statuses, and handoff notes.

## Stack Direction

- Python, FastAPI, PostgreSQL, Alembic, OpenAPI, pytest.
- Docker Compose, GitHub Actions, release gates, smoke checks, logs, backups, runbooks.
- LLM/RAG workflows, OpenAI/Claude/Gemini provider boundaries, document/transcript/lead processing, scoring, routing, approval queues.
- n8n webhook orchestration and Telegram approval around backend-owned workflows.
- API/webhook/custom database adapters, CRM/ERP/Bitrix/1C/banking/accounting boundaries.
- Admin/operator UI, roles, audit trail, notifications, reporting, and recovery workflow.

## Proof Review Context

For a role, the best fit is remote backend/platform, AI automation, integration, DevOps, or internal
tools work where I can own one operational slice end to end.

For a project, the strongest first step is one real workflow, the systems or data involved, and
one clear success condition.

I will respond with the smallest responsible first slice, risky assumptions, likely data model or
integration boundary, verification plan, and what should wait until the first working path proves
the direction.

## Links

- Visual page: https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html
- DriveDesk AI Operator: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-ai-operator.html
- Start conversation: https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html
- Portfolio: https://alexgerlitz.github.io/AlexGerlitz/
- DriveDesk Core: https://github.com/AlexGerlitz/drivedesk-core
