# Verification Pack

Fast technical verification path for the public profile. This page is for reviewers who want to
check claims directly instead of relying on summaries.

Last checked: 2026-06-26.

## 15-Minute Review Path

1. Open the DriveDesk Core review route and public demo.
2. Open the latest DriveDesk Core CI and Pages runs.
3. Scan the Skill Evidence Matrix for the role keywords that matter.
4. For AI automation roles, open the AI Ops public proof status, reviewer acceptance report, role requirements map,
   live approval proof, and CI workflow first.
5. Open one proof repo that matches the role: DriveDesk Core, AI Ops Workflow Kit, DeployMate, or
   MPlusForm.
6. Check whether the project has tests, CI, docs, runbooks, demo paths, or explicit reviewer
   snapshots.

## Pinned Repository Order

The GitHub profile pins are intentionally ordered as a review funnel:

| Order | Repository | Review signal |
| --- | --- | --- |
| 1 | [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) | Flagship backend/platform and integration foundation. Start here for the strongest proof. |
| 2 | [AI Ops Workflow Kit](https://github.com/AlexGerlitz/ai-ops-workflow-kit) | AI workflow/RAG backend proof with document/CRM/call intake, importable n8n workflow artifact, one-command offer demo, reviewer acceptance report, LLM/transcription provider boundaries, transcript analysis, approvals, Telegram callback approval, dry-run Bitrix CRM handoff, idempotent outbox drain, opt-in worker, Docker, and integration boundaries. |
| 3 | [DeployMate](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot) | DevOps/release discipline proof. Includes release gates, evidence bundle, and a public recovery trail. |
| 4 | [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) | Validation, trust-boundary, client/server sync, and Windows automation proof. |
| 5 | [AlexGerlitz profile](https://github.com/AlexGerlitz/AlexGerlitz) | Index for resume, services, role targets, and verification links. |

## Claim To Evidence Map

| Claim | Evidence | How to verify |
| --- | --- | --- |
| Backend/platform engineering | DriveDesk Core: tenant model, RBAC, audit/outbox, workflow rules, adapter boundaries, OpenAPI, tests, docs, public demo. | Open the [DriveDesk Core review route](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html), the [public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/), and the latest checked [CI run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062). |
| Public demo and release discipline | DriveDesk Core GitHub Pages demo is published from the repo and checked by Actions. | Open the [Pages deployment run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544), the [public demo health run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28198174892), and the demo URL. |
| AI workflow / RAG backend | AI Ops Workflow Kit: document/CRM/call intake, importable n8n workflow artifact, offer demo, LLM/transcription provider boundaries, reviewer acceptance report, ingestion/retrieval, transcript analysis, lead scoring, approvals, Telegram callback approval, dry-run Bitrix CRM handoff, idempotent outbox drain, opt-in worker, pgvector-ready storage, deterministic tests, Docker, and n8n/Telegram boundaries. | Open the [AI Ops public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), the [reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md), the [live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md), the [role requirements map](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md), the [repo](https://github.com/AlexGerlitz/ai-ops-workflow-kit), and the [CI workflow](https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml). |
| DevOps and release ownership | DeployMate: self-hosted deployment control panel direction, release gates, production contract checks, strict SSH host-key posture, runbooks, incident automation, and evidence bundle. | Open [DeployMate](https://github.com/AlexGerlitz/deploymate#engineering-proof-snapshot), the [CI run](https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684), the [public evidence bundle](https://github.com/AlexGerlitz/deploymate/actions/runs/28203961395), and the [release-secrets audit](https://github.com/AlexGerlitz/deploymate/actions/runs/28151327814). |
| Validation and trust boundaries | MPlusForm: client-side data is treated as untrusted until server-side validation creates an approved public snapshot. | Open [MPlusForm](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot). |
| Remote business infrastructure support | Autoschool54 / DriveDesk private work since March 2024, represented publicly through sanitized architecture, docs, proof repos, and operational case studies. | Read [Case Studies](./CASE_STUDIES.md), [Proof of Work](./PROOF_OF_WORK.md), and [Resume](./RESUME.md). |

## Current External Verification

Checked on 2026-06-26:

- DriveDesk Core public demo returned HTTP 200.
- DriveDesk Core `main` is green on `633e92a`.
- DriveDesk Core latest checked CI run succeeded on `633e92a`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203636062
- DriveDesk Core Pages deployment succeeded on `633e92a`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28203635544
- DriveDesk Core latest scheduled public demo health succeeded on `e67e478`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28198174892
- AI Ops public proof status is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- AI Ops Workflow Kit CI workflow is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml
- AI Ops reviewer acceptance report is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md
- AI Ops latest checked CI run succeeded on `99667b9`: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28203298763
- AI Ops live approval proof is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md
- AI Ops deeper review docs are available from the public proof status when a technical reviewer wants full drill-down.
- AI Ops public proof status tracks the live-runtime boundary, local public gate, committed runtime evidence, LLM provider fallback state, and transcription provider state: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- DeployMate default branch `develop` is green on `237b2c9`.
- DeployMate CI succeeded on `237b2c9`, including the production-contract job: https://github.com/AlexGerlitz/deploymate/actions/runs/28203923684
- DeployMate public evidence bundle succeeded on `237b2c9`: https://github.com/AlexGerlitz/deploymate/actions/runs/28203961395
- DeployMate release-secrets audit is green for staging and production: https://github.com/AlexGerlitz/deploymate/actions/runs/28151327814
- MPlusForm `main` is current on `9c55283`; repository and reviewer snapshot were reachable.

## Recovery Trail

DeployMate keeps the public release-audit incident trail visible as recovery evidence:

- Production issue, now closed: https://github.com/AlexGerlitz/deploymate/issues/18
- Staging issue, now closed: https://github.com/AlexGerlitz/deploymate/issues/19

Observed root cause: strict SSH host-key verification detected pinned host-key drift for the target
host. That was treated as a trust-anchor incident, not a test flake.

What was improved publicly:

- Commit `4b493b9` updates the release-audit action so failed audits are reported as failures in
  summaries and notifications instead of being mislabeled as success.
- The DeployMate runbook documents the safe recovery path: confirm host-key rotation out of band,
  regenerate known_hosts with `scripts/prepare_known_hosts.sh`, update the environment
  `DEPLOY_SSH_KNOWN_HOSTS` secret, re-run the audit manually, then close the incident only after a
  successful run.
- The latest checked `Release Secrets Audit` run passed staging and production audit jobs:
  https://github.com/AlexGerlitz/deploymate/actions/runs/28151327814

What is intentionally not claimed:

- Release automation is presented as inspectable CI/recovery evidence, not as a claim that every
  private environment can be deployed by a public reviewer.

## What To Take Away

The point is not to hide every system behind a polished screenshot. The useful proof is inspectable:
code, docs, CI, release gates, runbooks, incidents, and recovery steps are visible enough for a
technical reviewer to evaluate the engineering behavior.
