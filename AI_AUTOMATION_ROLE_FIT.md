# AI Automation Role Fit

Public role-fit page for AI automation, LLM workflow, RAG, integration, and backend-owned
internal automation work.

## Strongest Fit

The best role fit is not pure ML research and not no-code-only automation. The strongest fit is a
business workflow where AI has to be useful, inspectable, and operated by people:

- documents, call audio, transcripts, tickets, leads, or knowledge bases;
- RAG / retrieval / context assembly;
- LLM analysis with structured JSON output and an OpenAI/Claude/Gemini-ready provider boundary;
- scoring, routing, drafts, recommendations, or tasks;
- approval flow and human review;
- Telegram, CRM, Bitrix, webhook, or backend handoff;
- Docker/CI/tests/logs/runbooks so the workflow can survive real usage.

## Workflow Slice I Can Own

| Step | Output |
| --- | --- |
| Intake | Normalize documents, transcripts, tickets, leads, or webhook payloads into a backend-owned record. |
| Retrieval | Store and retrieve relevant context through PostgreSQL/pgvector-backed storage or a compatible vector layer. |
| AI analysis | Produce structured summaries, risk flags, scoring, routing reasons, and draft actions. |
| Approval | Keep human review explicit through approval states, audit notes, Telegram payloads, and operator handoff. |
| Integration | Push the approved result into CRM/API/webhook boundaries with mapping, validation, retries, and logs. |
| Operations | Add deterministic tests, smoke checks, Docker/CI paths, docs, and a short runbook for support. |

## Proof Route

| Signal | Review |
| --- | --- |
| Public proof status | [AI Ops public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md) |
| Live owner proof | [Live Telegram approval evidence](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md) |
| Reviewer acceptance report | [AI Ops reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md) |
| Vacancy requirement map | [AI Ops role requirements map](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md) |
| AI workflow demo | [AI Ops offer demo](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/OFFER_DEMO.md) |
| CI proof | [AI Ops CI workflow](https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml) |
| Backend/platform foundation | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) |
| Technical verification path | [Verification pack](./VERIFICATION_PACK.md) |
| Role fit | [Role Fit](./ROLE_FIT.md) |
| First-month plan | [First 30 days](./FIRST_30_DAYS.md) |

## Stack Mapping

| Need | Fit |
| --- | --- |
| Backend-owned AI workflow | Python, FastAPI, PostgreSQL, service contracts, structured outputs, provider boundaries, tests. |
| RAG / embeddings / context | Vector Databases, PostgreSQL/pgvector-backed storage, retrieval boundaries, citations/context discipline, quality checks. |
| LLM API integration | OpenAI/Claude/Gemini-ready boundary with local fallback, provider runtime, and payload contract tests. |
| Automation orchestration | Importable n8n workflow artifact, n8n-compatible webhook boundaries, document intake, call-audio transcription boundary, Telegram approval payloads and callback handling, queue/outbox worker thinking. |
| CRM / Bitrix / API handoff | Adapter contracts, field mapping, validation, retries, logs, and rollout notes. |
| Production readiness | Docker Compose, GitHub Actions, health/smoke checks, docs, runbooks, recovery thinking. |

## Proof Review Path

A useful review starts from one real workflow, not a generic puzzle:

1. Show the current document/call-audio/transcript/ticket/lead flow.
2. Define the first success condition.
3. Ask for the smallest backend-owned slice.
4. Review how retrieval, LLM output, approval, integration, and verification would be handled.
5. Check the AI Ops offer demo and DriveDesk Core for concrete proof.

## Boundary Discipline

I do not treat AI automation as loose workflow glue. The production boundary matters:

- the backend owns state, audit, validation, and retries;
- n8n is useful for orchestration, not for hiding business logic;
- LLM output should be structured, reviewed, logged, and testable;
- RAG quality depends on source quality, chunking/retrieval strategy, and evaluation;
- risky actions need approval, rollback notes, and clear operator visibility.

## Strong First Slice

Give me one real workflow with enough context to ship a responsible slice:

- one input source;
- one retrieval/context source;
- one useful AI analysis output;
- one approval or review point;
- one CRM/API/webhook handoff;
- one success metric and verification path.

That is enough to produce a working first version with tests, docs, and a clear next iteration path.
