# Remote AI Automation Services

I build remote-only backend, AI automation, integration, and DevOps systems for business
operations.

Clean web route: [Remote AI Automation Services](https://alexgerlitz.github.io/AlexGerlitz/services.html).

The best fit is a concrete business workflow that is currently too manual, too fragile, or too
unclear to scale. I use AI heavily to compress research, implementation, debugging, and
documentation time, but the final output still has to be inspectable: code, tests, logs, smoke
checks, deployment notes, and a handoff path.

Best immediate starts: AI workflow automation, CRM/ERP/API adapter, backend/platform slice, DevOps
recovery sprint, or DriveDesk AI Operator-style proof route.

Best-fit request shape: backend-owned state, data sources, integration boundaries, approval flow,
deployment/recovery path, or AI/RAG step that can be proven with logs, tests, docs, and a handoff.

LinkedIn Services request filter: if LinkedIn routes the request as Web Development or Custom
Software Development, I still treat it as a fit only when the work has backend/platform,
AI workflow, integration, DevOps, or internal-operations ownership. A website refresh, a student
assignment, a standalone game, or a generic mobile store is not the right request unless there is a
real backend/integration system to own.

Category routing note: [LinkedIn Service Page Fit](./LINKEDIN_SERVICE_PAGE_FIT.md) tracks the
exact service-category strategy so the live Services page attracts backend/platform, AI workflow,
integration, data, and DevOps requests instead of broad site/game/mobile tasks.

Not my target right now: isolated brochure/static websites, student/course assignments, standalone
game clones, or generic mobile/ecommerce apps without backend, integration, or operations
ownership.

## What I Can Build

| Service | Best for | Typical output |
| --- | --- | --- |
| DriveDesk AI Operator demo | Sales/support teams that need call or transcript analysis, lead scoring, follow-up drafts, approval, and CRM action. | RAG, call analysis JSON, Telegram approval, n8n orchestration, CRM sandbox adapter, audit/retry path, tests, runbook, screenshots/demo. |
| AI workflow / RAG MVP | Teams that read, search, summarize, classify, score, route, or approve too much manual work. | Ingestion, retrieval, summaries, scoring/routing, approval queues, API/admin workflow, tests, and runbook. |
| Internal operations platform | Businesses running operations through chats, spreadsheets, duplicated documents, or fragile admin routines. | FastAPI/PostgreSQL backend, records, roles, audit trail, tasks, notifications, admin workflows, Docker deploy path. |
| Integration adapter | 1C, CRM/ERP, banking/accounting, custom databases, webhooks, or public APIs that need reliable data flow. | Explicit contracts, mapping/validation, sync/retry/logging path, smoke checks, rollout notes, and debugging docs. |
| DevOps / release recovery | Self-hosted services that are hard to deploy, observe, back up, or recover. | Docker/CI gates, health checks, logs, backup/restore path, smoke tests, and recovery procedure. |
| Workflow teardown + working slice | Messy requirements where the first need is clarity plus proof. | Risk map, data model, integration boundaries, smallest working slice, and next implementation plan. |

## Fixed-Scope Entry Points

For concrete packages, timeboxes, and budget signals, see the
[Fixed-Scope AI Automation Offers](./FIXED_SCOPE_OFFERS.md).

Remote-only LinkedIn service page:
[linkedin.com/services/page/3153b734507b8a60ab](https://www.linkedin.com/services/page/3153b734507b8a60ab/)

### 1. Workflow Teardown + Working Slice

Input:

- current workflow, chat history, spreadsheet, screenshots, CRM export, API docs, or existing code;
- one practical success condition;
- access and constraints: stack, hosting, credentials, deadline, budget range, language.

Output:

- workflow and risk breakdown;
- first data model / integration map;
- smallest responsible working slice;
- verification plan;
- next-step implementation estimate.

### 2. DriveDesk AI Operator Demo

Good for sales/support workflows where calls, transcripts, documents, or CRM leads should become
RAG-backed analysis, lead scoring, follow-up drafts, approvals, and CRM actions.

Output can include:

- document/transcript/lead ingestion;
- RAG retrieval with citations;
- call analysis JSON;
- Telegram approval flow;
- n8n webhook orchestration;
- fake/sandbox CRM or Bitrix adapter with retries, idempotency, audit log, and dead-letter path;
- Docker Compose, CI, tests, screenshots, two-minute demo, runbook, and cost notes.

### 3. AI Ops / RAG Workflow MVP

Good for document processing, support tickets, transcripts, leads, orders, internal knowledge,
operator queues, or approval workflows.

Output can include:

- ingestion and retrieval;
- summaries, classification, scoring, or routing;
- approval states and operator handoff;
- API/admin surface;
- deterministic tests and smoke checks;
- deployment and runbook notes.

### 4. Integration Adapter

Good for CRM, ERP, 1C, banking/accounting boundaries, custom databases, public APIs, webhooks, and
manual import/export flows.

Output can include:

- source/target contract;
- mapping and validation rules;
- sync, retry, and error handling;
- logs and health checks;
- rollout and debugging notes.

### 5. Backend / Internal Tool Build

Good when a business needs an owned tool instead of another spreadsheet, chat process, or manual
operator routine.

Output can include:

- FastAPI/PostgreSQL backend;
- roles, permissions, records, audit trail, tasks, notifications, or admin workflows;
- Docker Compose runtime;
- tests, health checks, docs, and recovery notes.

### 6. DevOps / Recovery Hardening

Good when a service already exists but breaks during deployment, recovery, updates, or operations.

Output can include:

- Docker/service cleanup;
- GitHub Actions or release gate;
- logs, health checks, smoke checks, and evidence capture;
- backup/restore and rollback path;
- runbook for future operators.

## Proof

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) - public FastAPI/PostgreSQL
  platform foundation with RBAC, audit/outbox, adapter boundaries, OpenAPI, CI, docs, and demo.
- [DriveDesk AI Operator](./DRIVEDESK_AI_OPERATOR.md) - flagship AI sales/support workflow case:
  RAG, transcript analysis, lead scoring, Telegram approval, n8n, CRM adapter contracts, audit,
  retries, Docker, CI, runbook, and demo route.
- [Resume](./RESUME.md) - short role-fit profile and proof summary.
- [Skill evidence](https://alexgerlitz.github.io/AlexGerlitz/skill-evidence.html) - skills mapped
  to public repositories, docs, demos, CI, and runtime proof.
- [Remote role targets](./ROLE_TARGETS.md) - roles and search keywords that match the
  public proof.
- [Fixed-scope offers](./FIXED_SCOPE_OFFERS.md) - concrete project menu with expected inputs,
  outputs, timeboxes, and budget signals.
- [LinkedIn Services](https://www.linkedin.com/services/page/3153b734507b8a60ab/) - remote-only
  service page with DriveDesk AI Operator and AI Ops Workflow Kit proof samples.
- [LinkedIn Service Page Fit](./LINKEDIN_SERVICE_PAGE_FIT.md) - exact category strategy for
  filtering broad LinkedIn Services requests toward backend/platform, AI workflow, integration,
  data, and DevOps work.
- [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) - AI/RAG workflow backend
  backend with transcript analysis, approval queues, pgvector-ready storage, Docker, and tests.
- [DeployMate](https://github.com/AlexGerlitz/deploymate) - self-hosted deployment control panel
  direction with SSH runtime tooling, CI/CD, health checks, and runbooks.
- [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) - addon and sync pipeline work around
  validation boundaries, server-side trust checks, Windows automation, and docs.
- [Proof of work summary](./PROOF_OF_WORK.md) - the fast reviewer path.
- [Engineering case studies](https://alexgerlitz.github.io/AlexGerlitz/case-studies.html) - problem, build, evidence, and operating proof.
- [Skill evidence matrix](./SKILL_EVIDENCE.md) - GitHub-readable role keywords and skills mapped to
  public proof.

## How To Start

Send:

- the business process or problem;
- current tools, data sources, APIs, or code;
- what "done" means in practical terms;
- deadline, budget range, access limits, hosting constraints, stack, language, and handoff depth.

I will respond with the smallest responsible path to a working result: what can be proven first,
what is risky, what should wait, and what evidence will show that the result actually works.

The fastest route is the
[Remote AI Automation Services page](https://alexgerlitz.github.io/AlexGerlitz/services.html),
the [LinkedIn Services page](https://www.linkedin.com/services/page/3153b734507b8a60ab/), or the
[Start Conversation page](https://alexgerlitz.github.io/AlexGerlitz/start-conversation.html).
For a concrete project menu, use the [Fixed-Scope AI Automation Offers](./FIXED_SCOPE_OFFERS.md).
For concise first context, use the [Inbound Brief](https://alexgerlitz.github.io/AlexGerlitz/intake-brief.html).
