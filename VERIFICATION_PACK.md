# Verification Pack

Fast technical verification path for the public profile. This page is for reviewers who want to
check claims directly instead of relying on summaries.

Last checked: 2026-06-25.

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
| 3 | [DeployMate](https://github.com/AlexGerlitz/deploymate) | DevOps/release discipline proof. Includes current public incident handling for known_hosts drift. |
| 4 | [MPlusForm](https://github.com/AlexGerlitz/MPlusForm) | Validation, trust-boundary, client/server sync, and Windows automation proof. |
| 5 | [AlexGerlitz profile](https://github.com/AlexGerlitz/AlexGerlitz) | Index for resume, services, role targets, and verification links. |

## Claim To Evidence Map

| Claim | Evidence | How to verify |
| --- | --- | --- |
| Backend/platform engineering | DriveDesk Core: tenant model, RBAC, audit/outbox, workflow rules, adapter boundaries, OpenAPI, tests, docs, public demo. | Open the [DriveDesk Core review route](https://alexgerlitz.github.io/AlexGerlitz/drivedesk-core-review.html), the [public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/), and the latest [CI run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553622). |
| Public demo and release discipline | DriveDesk Core GitHub Pages demo is published from the repo and checked by Actions. | Open the [Pages deployment run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553066), the [public demo health run](https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28161509901), and the demo URL. |
| AI workflow / RAG backend | AI Ops Workflow Kit: document/CRM/call intake, importable n8n workflow artifact, offer demo, LLM/transcription provider boundaries, reviewer acceptance report, ingestion/retrieval, transcript analysis, lead scoring, approvals, Telegram callback approval, dry-run Bitrix CRM handoff, idempotent outbox drain, opt-in worker, pgvector-ready storage, deterministic tests, Docker, and n8n/Telegram boundaries. | Open the [AI Ops public proof status](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md), the [reviewer acceptance report](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md), the [live approval proof](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md), the [role requirements map](https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/ROLE_REQUIREMENTS_MAP.md), the [repo](https://github.com/AlexGerlitz/ai-ops-workflow-kit), and the [CI workflow](https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml). |
| DevOps and release ownership | DeployMate: self-hosted deployment control panel direction, release gates, production contract checks, strict SSH host-key posture, runbooks, incident automation. | Open [DeployMate](https://github.com/AlexGerlitz/deploymate), the [CI workflow](https://github.com/AlexGerlitz/deploymate/actions/workflows/ci.yml), and the release-audit incidents linked below. |
| Validation and trust boundaries | MPlusForm: client-side data is treated as untrusted until server-side validation creates an approved public snapshot. | Open [MPlusForm](https://github.com/AlexGerlitz/MPlusForm#60-second-reviewer-snapshot). |
| Remote business infrastructure support | Autoschool54 / DriveDesk private work since March 2024, represented publicly through sanitized architecture, docs, proof repos, and operational case studies. | Read [Case Studies](./CASE_STUDIES.md), [Proof of Work](./PROOF_OF_WORK.md), and [Resume](./RESUME.md). |

## Current External Verification

Checked on 2026-06-25:

- DriveDesk Core public demo returned HTTP 200.
- DriveDesk Core latest checked CI run succeeded on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553622
- DriveDesk Core Pages deployment succeeded on `1c04111`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/27925553066
- DriveDesk Core public demo health succeeded on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28161509901
- DriveDesk Core public scheduled validation succeeded on `3f597cf`: https://github.com/AlexGerlitz/drivedesk-core/actions/runs/28155499567
- AI Ops public proof status is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- AI Ops Workflow Kit CI workflow is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/workflows/ci.yml
- AI Ops reviewer acceptance report is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/REVIEWER_ACCEPTANCE_REPORT.md
- AI Ops latest checked CI run succeeded on `9099b52`: https://github.com/AlexGerlitz/ai-ops-workflow-kit/actions/runs/28172015560
- AI Ops live approval proof is published: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/LIVE_OWNER_PROOF.md
- AI Ops deeper review docs are available from the public proof status when a technical reviewer wants full drill-down.
- AI Ops public proof status tracks the live-runtime boundary, local public gate, committed runtime evidence, LLM provider fallback state, and transcription provider state: https://github.com/AlexGerlitz/ai-ops-workflow-kit/blob/main/docs/PUBLIC_PROOF_STATUS.md
- DeployMate `release-gate` and `production-contract` jobs passed on repair run `27737145074`;
  the full workflow failed at `staging-release` because the same strict known_hosts drift blocks
  environment deploy.
- MPlusForm repository and reviewer snapshot were reachable.

## Known Live Incident Surface

DeployMate currently has public scheduled `Release Secrets Audit` incident issues:

- Production: https://github.com/AlexGerlitz/deploymate/issues/18
- Staging: https://github.com/AlexGerlitz/deploymate/issues/19

Observed root cause: strict SSH host-key verification detected pinned `known_hosts` drift for the
target host. That is a trust-anchor incident, not a test flake.

What was improved publicly:

- Commit `4b493b9` updates the release-audit action so failed audits are reported as failures in
  summaries and notifications instead of being mislabeled as success.
- Push run `27737145074` proved the code-side `release-gate` and `production-contract` jobs after
  the repair, then failed at `staging-release` on the same strict host-key mismatch.
- The DeployMate runbook now documents the safe recovery path: confirm the host-key rotation out of
  band, regenerate known_hosts with `scripts/prepare_known_hosts.sh`, update the environment
  `DEPLOY_SSH_KNOWN_HOSTS` secret, re-run the audit manually, then close the incident only after a
  successful run.

What is intentionally not claimed:

- The scheduled release-secrets audit should not be called recovered until the new host fingerprint
  is owner-confirmed and the GitHub environment secret is updated.

## What To Take Away

The point is not to hide every system behind a polished screenshot. The useful proof is inspectable:
code, docs, CI, release gates, runbooks, incidents, and recovery steps are visible enough for a
technical reviewer to evaluate the engineering behavior.
