# Codex — paste this as your first instruction

You are the implementation engineer for **RescueBridge AI**, a hackathon submission for Challenge 1: Multi-Lingual Disaster Relief Hub. The project folder contains `PRD.md`, `AGENTS.md`, `docs/ACCEPTANCE_TESTS.md`, `docs/INTEGRATION_PLAYBOOK.md`, and `docs/DEMO_SCRIPT.md`.

**Read `AGENTS.md` and `PRD.md` before writing any code. Follow them as binding specifications.** Implement the working full-stack application end-to-end, not just a dashboard mockup.

## Non-negotiable architecture

**Primary AI is entirely local:** Google's Gemma 4 E4B model installed in Ollama as `gemma4:e4b`, queried on `http://127.0.0.1:11434`. After installation, the core system must process multilingual emergency text and road/flood images without public internet connectivity. Never route these requests to Google or any hosted AI. Do not silently substitute a remote model if Ollama fails.

The **Gemini API hosted Gemma 4 26B A4B** adapter is a second, opt-in module used only for judges' API evaluation requirement. Snowflake CoCo + Snowflake live data access and Solana Agent Registry devnet registration are connected enhancements; they must not break offline core functions.

Build React/TypeScript/Vite/Tailwind/Leaflet frontend and FastAPI/Pydantic/SQLAlchemy/SQLite backend. Document a real, source-licensed, bounded offline map approach. Use clear `LIVE/CACHED/SIMULATED/NOT_CONFIGURED` labels, synthetic demo reports, high-quality operational UI, local health indicators, and human approval for all safety-relevant judgments.

## Execution instructions

1. Inspect machine/repo, dependencies and versions; preserve preexisting work. Print an architecture summary and phased plan in `IMPLEMENTATION_STATUS.md` and proceed immediately without optional clarifying questions.
2. Bootstrap complete repo, Python/Node packages, environment example, license, ignore rules, tests and CLI scripts. Configure Ollama `gemma4:e4b` as default. If model absent, provide the exact download command and continue implementing. Do not claim local test passes unless it truly executes.
3. Build backend first: validated report intake with multilingual original text, optional images, SQLite persistence, corrected/human-confirmed fields, media storage and audit trail; add local Gemma image/text adapter with strict JSON extraction; deterministic priority review rules.
4. Build frontend: dashboard, incidents, new report form, details, offline map, status provenance, integrations/evidence page, demo flow. No CDNs or online tiles in core offline flow.
5. Build real offline behaviors: disconnected backend and UI remain usable, model only on localhost, queue remote work, recover cleanly when network returns. Include verified instructions for a Wi-Fi-off demonstration.
6. Add separate hosted Gemma API evaluation script/endpoint with Google SDK; authentic Snowflake SQL and CoCo-evidence workflow; Solana registration and verification TypeScript scripts through 8004-solana. No fabricated success. Never execute paid/chain operations without explicit approval.
7. Make tests thorough: pytest, Vitest, Playwright, API integration, offline/manual test and CI. Run available tests, fix failures, accurately record skipped real external tests.
8. Write a complete public-facing README with installation, local model setup, offline instructions, challenge traceability, screenshots instructions, data provenance, security, actual proofs and exact GitHub Copilot prompt evidence placeholder that the human will fill **only after real Copilot use**.
9. After implementation, report completed files, commands to run, test outputs, unresolved environmental blockers, and ready-to-publish GitHub steps. **Do not publish the repository yourself unless the user explicitly asks.**

## Definition of successful output

A real local Gemma image-analysis flow (not a fake response), multilingual incident extraction, human-review dashboard, persistent offline SQLite, truthful integration modes, separately runnable Gemini/Snowflake/Solana challenge adapters, tests, docs, and source ready for a public GitHub repo. Show proof, not assertions.

**Start now by reading the documents, listing environment requirements, and implementing Gate 0 then Gate 1. Continue through the gates without seeking confirmation unless you reach an irreversible, credential-requiring, paid, or public action.**
