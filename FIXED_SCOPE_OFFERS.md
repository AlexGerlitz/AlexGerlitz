# Fixed-Scope AI Automation Offers

Concrete project menu for remote AI automation, backend automation, integration, and Docker/CI handoff work.
The fastest proof route is [DriveDesk AI Operator - Proof Route](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-proof-route.html).
The fastest business-facing proof before scope is [AI Ops Business Scenario Replay](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/business-scenario-replay.txt).

These are fixed-scope project signals, not employment salary numbers and not hourly rates. Final
pricing depends on access, urgency, data quality, reliability requirements, deployment depth, and
handoff expectations. If the scope is unclear, the right first step is a smaller paid slice with one
success condition.

## Best First Step

If the scope is unclear, start with **Workflow Teardown + Working Slice**: one workflow, one success
condition, one small working path, and a clear decision on whether to expand.

If the workflow is already clear, choose the closest offer below and send the offer name, current
workflow, systems involved, one success condition, constraints, and what must not break.

Proposal-ready first message:

```text
Offer: closest offer name.
Workflow: what happens today and where it breaks.
Systems: CRM, ERP, 1C, API, documents, calls, transcripts, database, hosting, or repo involved.
Success: one observable result.
Constraints: access, deadline, budget range, and what must not break.
Proof route: business scenario replay or DriveDesk proof route.
```

## Proof-Backed Offer Router

Use this when the business problem is clear enough to choose a starting package. Each route has a
public proof map, so the first message can point to an inspectable implementation pattern instead of
a vague automation request.

- **AI workflow / RAG:** choose DriveDesk AI Operator Proof Slice or AI Ops / RAG Workflow MVP. Proof:
  [AI Ops Hiring Signal Brief](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/hiring-signal-brief.txt),
  [AI Ops Business Scenario Replay](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/evidence/business-scenario-replay.txt)
  and [AI Ops Employer Trigger Proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/EMPLOYER_TRIGGER_PROOF.md).
- **CRM/ERP/API integration:** choose Integration Adapter MVP. Proof:
  [AI Ops Employer Trigger Proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/EMPLOYER_TRIGGER_PROOF.md)
  and [Skill Evidence](./SKILL_EVIDENCE.md).
- **Backend automation and integration ownership:** choose Internal Operations Platform Slice. Proof:
  [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) and
  [Enterprise Readiness](./ENTERPRISE_READINESS.md).
- **Docker/CI reliability:** choose Docker/CI Release Recovery Sprint. Proof:
  [DeployMate proof](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot) and
  [Verification Pack](./VERIFICATION_PACK.md).

## Fast Menu

| Offer | Best for | Timebox | Budget signal | Public proof |
| --- | --- | --- | --- | --- |
| Workflow Teardown + Working Slice | Messy workflow, unclear requirements, scattered tools, manual operator work. | 2-5 days | USD 750-2,500 | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [case studies](https://alexgerlitz.github.io/AlexGerlitz/case-studies.html) |
| DriveDesk AI Operator Proof Slice | Sales/support call, transcript, document, or CRM lead workflow that needs RAG, scoring, follow-up, approval, and CRM action. | 1-3 weeks | USD 3,000-12,000 | [DriveDesk AI Operator](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-ai-operator.html), [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) |
| AI Ops / RAG Workflow MVP | Documents, transcripts, tickets, leads, orders, approvals, internal knowledge. | 1-3 weeks | USD 3,000-10,000 | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) |
| Integration Adapter MVP | CRM/ERP/1C/banking/accounting/API/custom database sync boundary. | 1-4 weeks | USD 4,000-15,000 | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core), [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) |
| Docker/CI Release Recovery Sprint | Self-hosted service that is hard to deploy, observe, back up, or recover. | 3-10 days | USD 2,000-8,000 | [DeployMate](https://github.com/AlexGerlitz/deploymate) |
| Internal Operations Platform Slice | Owned backend/admin workflow instead of spreadsheets, chats, or fragile routines. | 2-6 weeks | USD 8,000-30,000 | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| DriveDesk-Style Operating Layer | Multi-system operations layer with phased CRM/ERP/1C/bank/admin integrations. | Phased | USD 25,000+ by phase | [flagship backend workflow](https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html) |

## 1. Workflow Teardown + Working Slice

Use this when the problem is valuable but not clean enough for a full build quote.

Input:

- current workflow, screenshots, spreadsheet, chat history, CRM export, docs, code, or API notes;
- one practical success condition;
- access constraints, deadline, budget range, hosting, language, and handoff needs.

Output:

- workflow map and risky assumptions;
- first data model or integration boundary;
- smallest responsible working slice;
- verification plan and next implementation estimate.

Good success condition:

```text
After this slice, one operator can upload/export the current source data, see normalized records,
and run one end-to-end check without manual transfer work.
```

## 2. DriveDesk AI Operator Proof Slice

Use this when a sales, support, or operations team needs an AI workflow around calls, transcripts,
documents, leads, approvals, and CRM follow-up.

Possible output:

- document/transcript/CRM lead ingestion;
- RAG retrieval with citations;
- call analysis JSON: summary, objections, next step, lead score, risks, missing info;
- Telegram approval for follow-up drafts;
- n8n webhook orchestration;
- fake/sandbox Bitrix or CRM adapter with real contract, retries, idempotency, and dead-letter path;
- Docker Compose, CI, tests, screenshots, two-minute demo, runbook, and metrics/cost notes.

Good success condition:

```text
Given one transcript or CRM lead, the system produces a cited analysis, asks for human approval in
Telegram, then creates a sandbox CRM task/comment with an audit trail and retry/idempotency proof.
```

## 3. AI Ops / RAG Workflow MVP

Use this when people waste time reading, searching, summarizing, scoring, routing, or approving
information.

Possible output:

- document/transcript/ticket ingestion;
- retrieval and answer workflow;
- summaries, classification, scoring, routing, or approval states;
- API/admin surface or operator queue;
- tests, smoke checks, deployment notes, and runbook.

Good success condition:

```text
Given a new batch of documents or tickets, the system ingests them, produces searchable records,
routes the high-priority items, and leaves an audit trail a human can review.
```

## 4. Integration Adapter MVP

Use this when business systems need reliable data flow instead of manual exports, fragile scripts,
or undocumented sync.

Targets can include:

- 1C, CRM, ERP, accounting, banking, custom databases, public APIs, webhooks, spreadsheets, and
  operator tools.

Possible output:

- source/target contract;
- mapping and validation rules;
- sync, retry, and error handling path;
- logs, health checks, smoke checks;
- rollout and debugging notes.

Good success condition:

```text
One source object can move through validation, mapping, sync, retry/error handling, and operator
review without losing traceability.
```

## 5. Docker/CI Release Recovery Sprint

Use this when a service exists but deployment, rollback, logs, backups, or recovery are fragile.

Possible output:

- Docker Compose or service cleanup;
- GitHub Actions or release gate;
- health checks, smoke checks, logs, and evidence capture;
- backup/restore and rollback path;
- operator runbook.

Good success condition:

```text
A fresh deploy or recovery path can be run from the documented steps, with logs and smoke checks
showing whether the service is healthy.
```

## 6. Internal Operations Platform Slice

Use this when a business needs an owned system instead of another spreadsheet, chat routine, or
manual admin process.

Possible output:

- FastAPI/PostgreSQL backend;
- records, tasks, roles, permissions, audit trail, notifications, or admin workflows;
- adapter boundaries for future integrations;
- Docker deploy path, tests, docs, health checks, and recovery notes.

Good success condition:

```text
One real operational workflow can be created, updated, audited, and handed off to an operator with
clear recovery notes.
```

## 7. DriveDesk-Style Operating Layer

This is the flagship proof path: a phased operating layer that integrates real business workflows
across CRM/ERP/1C/banking/accounting/admin systems.

The right version is not "connect everything to everything" on day one. The right version is:

- choose the first high-value workflow;
- define explicit contracts and trust boundaries;
- ship one reliable slice;
- add logs, tests, docs, and recovery;
- repeat with the next adapter or role.

Possible phases:

1. Discovery and first workflow slice.
2. Data model, roles, audit trail, and admin workflow.
3. First integration adapter.
4. AI workflow or operator queue.
5. Deployment, observability, backup, and recovery.
6. Next adapters and deeper automation.

Detailed route: [DriveDesk flagship backend workflow](https://alexgerlitz.github.io/AlexGerlitz/flagship-platform.html)
and [GitHub-readable platform notes](./FLAGSHIP_PLATFORM.md).

## Scoping The First Slice

The strongest first step is one real workflow, the current systems or data involved, and one clear
success condition. I use that to identify the smallest responsible working slice, the integration
risks, the verification path, and what should wait until after the first proof slice.

I will respond with the smallest responsible path to a working result, the risky assumptions, the
proof needed, and what should wait until after the first slice.
