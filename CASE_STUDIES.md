# Engineering Case Studies

Public HTML route: [case-studies.html](https://alexgerlitz.github.io/AlexGerlitz/case-studies.html).

This page is the narrative layer behind the proof links. It shows how I think about messy business
problems, AI-native delivery, backend/platform design, integrations, DevOps, and operational
handoff.

## Case 1: DriveDesk / Autoschool54 Operations Platform Direction

### Problem

A real business operation does not fail because it lacks one more script. It fails because work is
spread across chats, documents, schedules, payments, accounts, manual checks, support questions,
admin routines, and fragile deployment/recovery paths.

Since March 2024, I have supported Autoschool54's digital infrastructure remotely and used that
operational context to shape DriveDesk: one operations layer for internal workflows, records,
documents, integrations, notifications, AI assistance, deployment, observability, and recovery.

### Build

The public proof is DriveDesk Core: a backend/platform foundation that keeps the architecture
inspectable instead of relying on vague universal-integration claims.

Built proof includes:

- tenant-aware backend boundaries;
- RBAC and audit trail;
- outbox/worker pattern for async business operations;
- business records and workflow rules;
- adapter boundaries for future CRM/ERP/accounting/banking integrations;
- OpenAPI/SDK surfaces;
- Docker, pytest, CI, docs, and public demo.

### Evidence

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core)
- [DriveDesk Core fast review route](https://github.com/AlexGerlitz/drivedesk-core)
- [DriveDesk Core public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/)
- [Proof of work summary](./PROOF_OF_WORK.md)

### What This Proves

I can turn a vague operational domain into explicit backend boundaries, reviewable contracts,
runtime checks, docs, and a public demonstration path.

## Case 2: AI Ops Workflow Kit

### Problem

AI automation is often presented as a chat wrapper. Real operational AI work needs more structure:
documents or transcripts come in, retrieval has to be repeatable, summaries and routing have to be
reviewable, and higher-risk outputs need approval states instead of blind automation.

### Build

AI Ops Workflow Kit turns that into a backend pattern for AI-native operations automation: document intake, RAG retrieval, OpenAI/Claude/Gemini provider boundary, transcript analysis, approvals, and CRM handoff boundaries.

Built proof includes:

- document ingestion and retrieval direction;
- transcript analysis;
- approval queue, Telegram callback approval, and explicit state transitions;
- idempotent outbox drain and opt-in worker handoff;
- PostgreSQL/pgvector-backed storage direction;
- deterministic local embedding path for repeatable tests;
- Docker runtime;
- n8n and Telegram integration boundaries.

### Evidence

- [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit)
- [AI Ops Workflow Kit reviewer snapshot](https://github.com/AlexGerlitz/ai-ops-workflow-kit#60-second-reviewer-snapshot)
- [Skill evidence matrix](./SKILL_EVIDENCE.md)

### What This Proves

I can use an AI-native delivery loop while keeping workflow state, approval boundaries, tests, and
integration surfaces explicit.

## Case 3: DeployMate

### Problem

Self-hosted systems are not only code. They need deployment paths, target servers, logs, health
checks, environment handling, CI/CD, and recovery thinking. If that layer is weak, the product feels
fragile even when features exist.

### Build

DeployMate is a self-hosted deployment control panel direction focused on making deployment and
operations reviewable.

Built proof includes:

- FastAPI/Next.js/PostgreSQL product direction;
- Docker app deployment model;
- VPS/SSH runtime tooling direction;
- logs, health checks, admin flows, and release docs;
- CI/CD and public proof route cleanup;
- repo-first public review path after removing dead external-site dependency.

### Evidence

- [DeployMate](https://github.com/AlexGerlitz/deploymate)
- [DeployMate engineering proof snapshot](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot)
- [Remote services](./SERVICES.md)

### What This Proves

I understand the operational side of shipping: deployability, observability, release discipline,
health checks, runbooks, and recovery paths matter as much as feature code.

## Case 4: MPlusForm

### Problem

Desktop/client-side data is not automatically trustworthy. If a workflow includes local files,
addons, sync helpers, or Windows automation, the architecture needs a clear boundary between
untrusted client evidence and approved server-side state.

### Build

MPlusForm is an addon and sync-pipeline proof around validation and trust boundaries.

Built proof includes:

- Lua addon surface;
- Python sync pipeline direction;
- server-side trust validation layer;
- approved public snapshot concept;
- Windows operation scripts and handoff docs;
- reviewer snapshot for fast inspection.

### Evidence

- [MPlusForm](https://github.com/AlexGerlitz/MPlusForm)
- [MPlusForm reviewer snapshot](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot)
- [Skill evidence matrix](./SKILL_EVIDENCE.md)

### What This Proves

I can design validation boundaries around untrusted data and document a workflow so another operator
can inspect and run it.

## Common Pattern

Across these projects, the pattern is the same:

- start from a messy real workflow;
- identify the risky assumptions;
- build the smallest responsible working slice;
- make the boundaries explicit;
- verify with tests, CI, logs, smoke checks, or public demos;
- leave docs and runbooks so the result can be operated after the first demo.

That is the proof: AI tooling speed paired with engineering ownership.
