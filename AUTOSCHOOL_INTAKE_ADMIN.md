# Autoschool Intake Admin Proof

Public HTML route: https://alexgerlitz.github.io/AlexGerlitz/autoschool-intake-admin.html

This is a public-safe representation of the private Autoschool54 intake/admin workflow. It explains
the engineering proof without exposing learner data, live admin screenshots, private repository code,
tokens, logs, internal URLs, or real operator records.

## 30-Second Proof

The workflow proves a first-job-ready backend/integration skill:

1. A person sends a request through a Telegram bot.
2. The backend normalizes and validates the request.
3. The request is persisted as an admin-visible record.
4. An operator sees the record in the admin panel and moves it through a status workflow.
5. The system keeps enough structure for handoff, debugging, deployment, backups, and recovery.

This is not positioned as "just a bot". The signal is business intake to admin handoff: user input,
backend validation, database state, operator workflow, and public-safe documentation.

## Public-Safe Demo Contract

Only synthetic examples belong in public proof:

| Surface | Public-safe example |
| --- | --- |
| Telegram request | Demo learner asks for a driving lesson callback. |
| Normalized record | `name=Demo Learner`, `contact=demo@example.invalid`, `category=lesson_request`, `status=new`. |
| Admin panel | Synthetic queue row with status, source, timestamp, and operator action. |
| Status workflow | `new -> reviewed -> contacted -> closed`. |
| Evidence | Architecture diagram, schema shape, synthetic screenshots or GIF, tests, and runbook notes. |

Not public: real learner names, phone numbers, Telegram IDs, chat IDs, message bodies, admin URLs,
database dumps, tokens, logs, private repository code, live admin screenshots, or internal joke/test
names from the real admin panel.

## Engineering Surface

| Layer | What it proves |
| --- | --- |
| Telegram intake | I can collect structured input from a real user-facing channel. |
| Backend validation | I can normalize messy input before it becomes business state. |
| Database record | I understand persistence, status fields, timestamps, and review state. |
| Admin handoff | I can make user input visible and actionable for an operator. |
| Privacy boundary | I can separate real business data from public proof. |
| Operations | I can think about deployment, backups, logs, recovery, and handoff docs. |

## First-Job Signal

This proof is useful for Junior Python Backend, Python Developer, Integration Developer, CRM/Admin
Tools Developer, or L2/L3 automation roles because it maps directly to common business tasks:

- capture a request from a user-facing channel;
- validate and store it;
- show it in an internal admin surface;
- keep statuses and operator actions clear;
- document what should happen when the workflow fails.

## How To Review

Start with the public routes:

- [DriveDesk Core](https://github.com/AlexGerlitz/drivedesk-core) for FastAPI/PostgreSQL platform foundations.
- [DriveDesk Core public demo](https://alexgerlitz.github.io/drivedesk-core/apps/admin/public-demo/) for public-safe admin surface proof.
- [Engineering Case Studies](https://alexgerlitz.github.io/AlexGerlitz/case-studies.html) for the Autoschool54 operational context.
- [Verification Pack](https://alexgerlitz.github.io/AlexGerlitz/verification-pack.html) for CI, smoke, demo, and proof freshness.

## Next Public Artifact

The next strongest public artifact is a sanitized demo seed:

`Telegram-style request -> API payload -> PostgreSQL record -> admin queue row -> operator status update`

All values should be synthetic and boring. No real names, no funny live-admin names, no phone numbers,
no chat IDs, and no screenshots from the private production admin.
