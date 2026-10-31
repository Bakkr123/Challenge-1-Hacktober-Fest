# AGENTS.md — Mandatory Codex / coding-agent instructions

These rules apply to every coding agent modifying this repository. The canonical specification is `PRD.md`; refer to it continuously. If documentation conflicts, prefer these agent safety rules and the explicit challenge requirements in the PRD.

## Mission
Implement **RescueBridge AI**, an offline-first, human-supervised multilingual disaster report intake/analysis dashboard. The **default and primary AI inference MUST run locally** with Gemma 4 E4B via Ollama (`gemma4:e4b`, `http://127.0.0.1:11434`). Cloud-hosted Gemma via Gemini API is **only** a separate, explicit evaluation adapter. Do not redesign the project into a cloud LLM app. Local report flow must work with WAN physically disconnected after setup.

## Working discipline
1. Inspect existing files and environment before editing. Read `PRD.md` and `docs/ACCEPTANCE_TESTS.md` fully. Create/maintain `IMPLEMENTATION_STATUS.md` with each milestone, actual command output, tests, known blockers, and next steps.
2. Implement in small end-to-end vertical slices and run tests after each milestone. Prefer working end-to-end minimal functionality over nonfunctional mock dashboards.
3. Do not ask optional questions or pause for aesthetic choices. Use specified defaults and reasonable local development conventions. If credentials, proprietary access, GitHub authentication, model downloads, or actual chain transactions are missing, implement the integration with a graceful `NOT_CONFIGURED` state, finish independent parts, and log the blocker precisely.
4. Never fake success: no fictional transaction hashes, screenshots, API outputs, SQL results, timing figures, Copilot evidence, or offline test. Always distinguish `LIVE`, `CACHED`, `SIMULATED`, `NOT_CONFIGURED`, `FAILED`.
5. Any dangerous real-world assertion (passable road, structural safety, verified casualty number, evacuation instruction, dispatch decision) must be excluded or explicitly unverified and require a human. App is a demo, not field-ready emergency software.
6. Never make automatic remote requests containing survivor reports, imagery, personal data, or coordinates. No silent cloud fallback. No CDNs or remote assets in the offline UI.
7. Keep source, tests, docstrings and UI text in English; support multilingual user input. Include no private PII in fixtures. Commit only synthetic data and redacted logs.
8. Credentials only in environment / local secret manager, never repository, screenshots, browser, or debug logs. Use `.env.example` and `.gitignore` properly. Do not install unverified arbitrary scripts without auditing the source; prefer official docs.
9. Format/lint/typecheck/test your code. Keep a real, useful README. Complete code, avoid fake placeholders and no-op handlers. If a feature is incomplete, visibly label it and report why.
10. Do not `git push`, publish the repository, fund a wallet, register an agent, invoke cloud APIs with sensitive data, or create paid resources without explicit user approval. Public repo creation is a final user-authorized step.

## Locked stack
- React + TypeScript + Vite + Tailwind, Leaflet (local assets, offline bounded map), React Router, React Query optional.
- Python 3.11+ FastAPI + Pydantic 2 + SQLAlchemy 2 + Alembic + SQLite + httpx or official Ollama client.
- Ollama default tag `gemma4:e4b`. Local model chosen in `.env`. Optionally `gemma4:e2b` after explicit manual selection, reported in UI and logs.
- Google `google-genai` only in explicit evaluation path, model `gemma-4-26b-a4b-it`.
- Snowflake connector and prepared SQL with CoCo usage documented; read-only restricted dataset access.
- TypeScript `8004-solana` SDK and `@solana/web3.js` in `integrations/solana` with devnet default.
- pytest, Ruff, mypy or pyright where practical, Vitest, Playwright, GitHub Actions CI.
- MIT license for **app source code**. Preserve separate licenses and usage terms for model weights and external datasets.

## Required implementation order

### Gate 0: Repo scaffold and environment diagnostics
- Scaffold backend, frontend, scripts, docs, make/test commands, .env, LICENSE, and CI.
- Record OS/architecture, RAM (if available), `ollama --version`, `ollama list`, Python/Node versions.
- Verify exact local Gemma 4 model is installed or print `ollama pull gemma4:e4b` with guidance. Do not assume model is downloaded. On environment without Ollama or hardware, continue coding with mocks in tests but keep `LIVE_LOCAL_MODEL_NOT_VERIFIED` in status.
- Set safe defaults: app binds loopback only, `AI_MODE=local`, `ALLOW_HOSTED_EVALUATION=false`.

### Gate 1: Persistent report intake + data model
- Implement Alembic migrations, SQLAlchemy models, Pydantic input/output schemas, configured local media directory.
- Media MIME and size validation (sniff header), EXIF removal for image derivative, SHA-256, safe storage; reject SVG/HTML; preserve original report body and user location provenance.
- API POST reports / GET incidents / PATCH incidents / basic health and integration states.
- Tests for permissions boundary, path traversal, invalid files, empty text+file, persistence, duplicate UUID.

### Gate 2: Local Gemma inference vertical slice
- Implement `GemmaProvider` protocol with `OllamaLocalProvider` as the only production incident analyzer.
- Use Ollama local API `http://127.0.0.1:11434`, `gemma4:e4b`, valid text + base64 image input. Validate model presence through Ollama. Model must actually analyze a file when installed, not only mock.
- Prompt must enforce reported/observed/inferred distinctions and structured Pydantic output. When invalid JSON, one repair attempt, then visible recoverable failure.
- Add tests of adapter request shape with mocked HTTP and optional real local integration test gated by `RUN_REAL_OLLAMA_TESTS=1`.
- Rules-based advisory priority; no autonomous emergency dispatch.

### Gate 3: Responsive operations UI
- Dashboard, intake, detail/edit, activity timeline, integrations/health, explicit demo-mode banners.
- Build and test local/offline map. No remote tile servers or Google fonts. Unknown location gets no invented coordinates.
- Show: configured model, `LOCAL` mode, `OFFLINE`, provider health and human review requirement.
- Browser tests for intake, image upload, local model failure and recoverable retry, review status edits.

### Gate 4: Offline resilience and evidence
- SQLite WAL + persistent media; outbox with `QUEUED`, `SUCCEEDED`, `FAILED`, `WAITING_FOR_APPROVAL`; explicit remote calls only.
- Keep local UI, model and map functioning with internet disabled. Create scripts and human walkthrough for disconnected test. Measure and record actual results where available; do not claim test performed unless actually performed.
- Add reproducible synthetic fixtures with explicit `is_synthetic=true`.

### Gate 5: Connected challenge integrations
- Separate hosted Gemini API adapter and synthetic-only script, OFF by default; run and record only if operator has configured key and approved test.
- Snowflake: real table + ingest scripts + parameterized read-only query. Document actual CoCo prompts/SQL output and data provenance. If no account, make runnable connector and mark live test `BLOCKED_ACCOUNT`.
- Solana: devnet registrar/verifier using `8004-solana` SDK, save public receipt only; user must expressly approve onchain call and supply demo wallet via environment. If no wallet, do not invent receipt.
- GitHub Copilot: `docs/COPILOT_EVIDENCE.md` scaffold with instructions; actual human Copilot interaction and proof is necessary. Codex must not impersonate Copilot usage.

### Gate 6: Submission QA and repo
- Tests, CI, secret scanning, README, architecture, license, safety docs, exact setup commands, all challenge evidence mapping, demo script.
- Run `git status`, show uncommitted changes, ensure `.env`, DB, media, wallet keys and outputs containing secrets are ignored.
- Create initial local Git commit only if permitted by execution context; do not push/publicize without user instruction. Document exact commands for creating a public GitHub repo.

## Required runtime modes
- `LOCAL`: actual local Ollama model; supported for main incident workflow.
- `LOCAL_DEMO_DATA`: local model + synthetic fixtures. Label fixtures, not model result, as synthetic.
- `HOSTED_GEMMA_EVALUATION`: explicit standalone synthetic request over network; never used for normal reports.
- `SNOWFLAKE_CONNECTED`/`SNOWFLAKE_CACHED`/`SNOWFLAKE_NOT_CONFIGURED`.
- `SOLANA_DEVNET_REGISTERED` only with verified onchain evidence; otherwise pending/not configured.

## Guardrails for UI and logs
- Header includes `OFFLINE-FIRST / LOCAL GEMMA 4` where actually configured. If not installed show `Local model unavailable — follow setup`, not false green success.
- Always show visible 'AI output must be verified by a human.'
- Show original message, English translation, extracted JSON facts, unverified claims, follow-up questions and model provenance.
- Any geolocation used is user-confirmed, human-entered or from a trusted provided asset; never geocode guesses as confirmed positions.
- Every failure state has actionable steps. Local failures never cause automatic Gemini fallback.

## Review criteria per gate
You may call a gate complete only if the user-facing feature exists, has at least an automated test or manual verified script, and status doc records what actually ran. Track `PASS`, `PARTIAL`, `BLOCKED`, `NOT_STARTED`. Use these statuses in final execution summary.

## Definition of stopping point
Complete as much independent work as possible in the current run. Never end with only a mock UI if the local backend could have been implemented. If hardware/credentials block an external proof, include exact commands, code, and explanation for user completion. Never promise future background work.
