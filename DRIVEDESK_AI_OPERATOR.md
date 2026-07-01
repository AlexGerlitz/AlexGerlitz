# DriveDesk AI Operator

Flagship proof route: an AI sales and support backend workflow that turns calls, documents,
transcripts, CRM leads, and knowledge-base records into reviewable operator actions.

This is the proof route I want recruiters, founders, and hiring managers to use when they evaluate
my work. It combines the strongest parts of the current proof stack:

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) for backend automation and integration, tenants,
  audit/outbox, workflow rules, adapters, OpenAPI, Docker, CI, and docs.
- [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) for document intake,
  RAG, OpenAI/Claude/Gemini provider boundary, call-audio transcription, transcript analysis, lead scoring, approval queues,
  Telegram callback handling, dry-run Bitrix CRM contract handoff with live Bitrix24 read-only preflight, idempotent outbox drain, opt-in worker, live PostgreSQL/pgvector persistence, importable n8n
  workflow artifacts, committed demo GIF/walkthrough, and n8n/Telegram boundaries.
- [DeployMate](https://github.com/AlexGerlitz/deploymate) for deployment, health checks, release
  gates, runbooks, and recovery discipline.

## Core Scenario

A company uploads or sends one of these inputs:

- call recording or transcript;
- support/sales chat transcript;
- documents, knowledge-base records, or external file-provider exports;
- CRM lead or deal payload;
- operator notes or follow-up context.

The system:

1. ingests and normalizes the input;
2. runs RAG search over the knowledge base;
3. analyzes the call/transcript;
4. produces structured JSON;
5. scores the lead or support case;
6. extracts tasks and missing information;
7. drafts a follow-up;
8. sends a Telegram approval request;
9. applies approve/reject/edit decisions;
10. creates a task, comment, or follow-up action in CRM through an adapter.

Bitrix/CRM can start as a fake or sandbox adapter, but the adapter contract should be real:
idempotency, retries, error visibility, dead-letter handling, audit log, and clear rollout notes.

## Minimum Technical Shape

| Layer | Minimum proof |
| --- | --- |
| Backend | FastAPI, PostgreSQL/pgvector, documents, transcripts, leads, approvals, audit log. |
| RAG | Ingestion, chunking, embeddings, retrieval, citations, and quality eval on test questions. |
| Call analysis | Structured JSON: summary, objections, next step, lead score, risks, missing info. |
| n8n | Importable workflow artifact: document/text export -> API -> approval -> CRM/Telegram route. |
| Telegram approval | Approve, reject, and edit draft before action is sent to CRM. |
| CRM adapter | Fake/sandbox first; real contract with retries, idempotency, and dead-letter queue. |
| Production proof | Docker Compose, CI, tests, screenshots, 2-minute demo video/GIF, runbook, metrics/cost notes. |

## The Selling Point

I am not just gluing no-code nodes together.

The backend owns the hard parts:

- state;
- RAG data;
- audit trail;
- retries;
- idempotency;
- quality checks;
- integration contracts;
- approval history;
- testable API behavior.

n8n is the orchestration layer. It should connect events and tools, not hide the business state or
make reliability impossible to inspect.

That difference matters in real companies. A workflow that only works inside a visual canvas is hard
to test, recover, audit, or extend. A backend-owned workflow with n8n orchestration can be reviewed
like software and still move fast.

## Demo Flow

The public offer demo takes one command:

```bash
python scripts/run_offer_demo.py
```

It proves:

1. document or sales playbook ingestion;
2. RAG retrieval with source context;
3. call transcript webhook;
4. structured call analysis and lead score;
5. approval item creation;
6. approve transition;
7. Telegram callback approval;
8. dry-run Bitrix CRM contract handoff event queued through the idempotent outbox drain.

Manual demo flow should take two minutes:

1. Upload a transcript or send a CRM lead webhook.
2. Show ingestion and RAG retrieval with citations.
3. Show call analysis JSON:
   - summary;
   - objections;
   - next step;
   - lead score;
   - risks;
   - missing info.
4. Show Telegram approval with generated follow-up.
5. Approve or edit the draft.
6. Show CRM sandbox task/comment created through the adapter.
7. Show audit log, retries/idempotency evidence, and runbook route.

## Why This Is Strong Proof

This single project proves the role surface better than a generic portfolio:

- AI automation: RAG, call-audio transcription, transcript analysis, scoring, draft actions, approval flow.
- Backend engineering: FastAPI, PostgreSQL, pgvector, API contracts, data model, tests.
- Platform thinking: state, audit, retries, idempotency, dead-letter handling, observability.
- Integrations: Telegram, n8n, CRM/Bitrix-style adapter boundaries.
- Docker/CI handoff: Docker Compose, CI, runbook, screenshots, demo video, metrics/cost notes.
- Product judgment: one business workflow, one success condition, one inspectable slice.

## Positioning

Best-fit roles after this demo:

- AI Automation Engineer;
- Python Backend / Internal Tools Engineer;
- LLM Workflow Engineer;
- RAG Workflow Engineer;
- CRM Integration Engineer;
- Internal Tools Engineer;
- AI Workflow Engineer with Docker/CI handoff.

Operating principle: AI tooling accelerates research, decomposition, implementation, debugging, docs,
tests, and review. I still own architecture, verification, logs, deployment, and result quality.

## Build Order

1. Data model and API contracts.
2. document/transcript/lead ingestion.
3. PostgreSQL/pgvector-backed RAG path with citations and restart persistence proof.
4. Call analysis JSON contract and tests.
5. Approval state machine.
6. Telegram approval route.
7. n8n webhook orchestration.
8. Fake CRM/Bitrix adapter with idempotency and retries.
9. Committed demo walkthrough/GIF, screenshots, runbook, and metrics/cost notes.
10. Real CRM adapter after the sandbox contract is proven.

## Review Links

- Visual page: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-ai-operator.html
- AI Ops Workflow Kit: https://github.com/AlexGerlitz/ai-ops-workflow-kit
- AI Ops demo walkthrough: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/DEMO_WALKTHROUGH.md
- AI Ops public proof status: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- AI Ops reviewer acceptance report: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md
- AI Ops live approval proof: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md
- AI Ops role requirements map: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md
- AI Ops CI workflow: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml
- DriveDesk Core review: https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html
- Role fit pack: https://alexgerlitz.github.io/AlexGerlitz/application-pack.html
- PDF resume: https://alexgerlitz.github.io/AlexGerlitz/output/pdf/alex-gerlitz-python-backend-automation-resume.pdf
