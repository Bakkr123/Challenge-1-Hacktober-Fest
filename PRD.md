# RescueBridge AI — Product Requirements Document

**Version:** 1.0  
**Status:** Build-ready specification for Codex  
**Project:** Challenge 1 — Multi-Lingual Disaster Relief Hub  
**Repository target:** `rescuebridge-ai` (public GitHub repository after review)  
**Positioning:** An offline-first, human-supervised coordination prototype for emergency reports during network disruption. **Not a certified emergency dispatch or structural safety system.**

## 1. Executive summary

RescueBridge AI transforms fragmented multilingual emergency reports (text, images, and optionally voice recordings) into structured, traceable incident records that rescue volunteers can review and prioritize. The default AI engine is **Gemma 4 E4B fully hosted on the user's own computer using Ollama**, with no internet required after the model, software, and local data have been downloaded. A deliberately separate, opt-in **Gemini API demonstration adapter** invokes the hosted Gemma 4 26B A4B model for evaluation requirements; it is never a silent fallback from the local model.

When a network is available, RescueBridge can query a Snowflake infrastructure dataset prepared with **Snowflake CoCo**, and can register/verify its agent identity using the **Solana Agent Registry**. External integration failures must not stop local incident intake, review, search, or local inference. Unsent sync operations remain queued and auditable.

## 2. Challenge traceability and non-negotiable deliverables

| Challenge requirement | Deliverable | Evidence |
|---|---|---|
| Gemma 4 Core | Local text+image analysis and translated/normalized incident reports | Recorded terminal/UI demo with Ollama model name, network disconnected |
| Gemma through Gemini API | A distinct hosted Gemma 4 26B A4B call analyzing a permitted synthetic image or text log | Runnable script, integration tests, sample sanitized output, README commands |
| Snowflake CoCo | Documented CoCo-assisted dataset discovery, ingestion, SQL exploration, and dashboard lookup | SQL scripts, dataset provenance, sample outputs, CoCo conversation/query record |
| Solana Agent Identity | Registered RescueBridge agent, inspectable devnet transaction and agent record | Real transaction signature + explorer URL created by authenticated integration |
| GitHub Copilot | Actual use to resolve a package/data/multimodal integration blocker | Exact Copilot prompts, files affected, before/after or terminal screenshots in README |
| Open-source repo | Public repository with explicit source license | `LICENSE` (MIT), README, architecture, safety notes, secrets excluded |

**Proof standard:** Distinguish `LIVE`, `CACHED`, `SIMULATED`, `UNAVAILABLE`, and `NOT_CONFIGURED` everywhere. Mock results never count as real Snowflake, Gemini, or Solana integration evidence. No wallet signature, API output, citation, or test pass is to be invented.

## 3. Goals and success criteria

**G1 — Local-only core:** With Wi-Fi disconnected and local packages/models already installed, a user can submit an Urdu/Hindi/English text message, attach a JPEG/PNG image, create an incident, and receive a structured Gemma-generated analysis stored in SQLite. The UI retains full basic functionality.

**G2 — Information quality:** Every result preserves the verbatim original report; distinguishes user-reported facts from model interpretations; records confidence as a qualitative limitation rather than a false certainty; displays `needs human review`. Unknown coordinates, shelter capacities, bridge safety status, and emergency availability must remain unknown.

**G3 — Data visualization:** Show live (local) incident list, details, filters, priority, location status, map pins only for confirmed coordinates, and task/update history.

**G4 — Connected capabilities:** Run at least one real Snowflake geospatial/infrastructure lookup with CoCo-generated SQL and at least one authentic Solana devnet agent registration; optionally submit *synthetic/non-sensitive* report material to hosted Gemini API only with explicit operator action.

**G5 — Reproducibility:** A new developer can run the app using documented commands. Automated backend, frontend, and API tests pass. README includes precise offline test steps, all environment variables, known limitations, and actual external integration evidence.

Recommended engineering targets (aspirational, measured and disclosed): p95 local request completion <= 30 seconds on the test machine for short text; media analysis <= 90 seconds on the test machine; offline data loss = 0 in deliberate restart tests; no uncaught error when cloud APIs are unreachable. **Do not claim these targets until benchmarked.**

## 4. Audience / roles

1. **Field volunteer (reporter):** Sends a location, original-language text, and optionally photos or audio. Sees submission status and can edit/correct their own report during a demo.
2. **Coordinator (primary user):** Reviews incidents, confirms classifications and locations, updates statuses, assesses needs, and approves any outbound sync.
3. **Evaluator (hackathon judge):** Can launch demo mode with preloaded synthetic reports and inspect exact source of AI, model execution location, Snowflake/CoCo evidence, Solana verification, and offline readiness.

For the hackathon MVP, implement a simple **single-machine demo** with role labels and a local admin PIN/configured password if available; do not suggest it is suitable for internet-facing deployment with enterprise authentication. Bind backend to `127.0.0.1` by default and disallow remote access unless documented secure deployment options are built.

## 5. User journeys

### Journey A — Emergency photo in Urdu, fully offline (P0)
1. Reporter submits an Urdu text report and an optional image of visible flood/road damage, and optionally selects or drops a location pin.
2. FastAPI validates upload and stores media **locally**, stripping EXIF GPS and metadata from derivative images.
3. The local Ollama Gemma 4 E4B adapter receives user report plus photo bytes; language may be identified and original text is retained.
4. AI returns a strictly validated JSON object with translation, incident category, reported needs, potential hazards, uncertainty, and questions for human follow-up.
5. A rules engine computes a *suggested review priority*, clearly marked advisory, and the coordinator must approve any operational change.
6. Incident appears in dashboard and SQLite even if the user closes the browser and reopens.

### Journey B — Multi-language and voice memo (P1)
- Accept audio WAV/MP3/M4A with size/duration limits. Use a separately verified **local speech-to-text adapter** (e.g. whisper.cpp/faster-whisper) if native Gemma audio handling is not supported by the installed local inference runtime. Feed transcript to local Gemma. Display original transcript, recognized language, manual correction control. Never use remote transcription implicitly. Audio is **not a blocking P0 feature**.

### Journey C — Infrastructure lookup (P0 connected demo)
- Coordinator opens an incident with confirmed coordinates and selects `Check Infrastructure (online)`.
- Backend queries allowlisted Snowflake table/view of infrastructure assets within configured radius (example: 2,000 meters), using SQL created and documented via CoCo. Display source, record timestamp, query status, and last successful cache. If Snowflake unavailable, display `Cached lookup from <timestamp>` or `No offline infrastructure data available`; never assert current route passability.

### Journey D — Agent identity (P0 connected demo)
- Operator selects `Register/Verify RescueBridge Agent` after local configuration of devnet wallet, SDK and required metadata. A separate TypeScript CLI registers the agent using official Solana Agent Registry SDK and captures the resulting asset/public key, signature, network, date, and explorer URL. Backend reads local metadata file/records for the dashboard. Devnet is acceptable for live demonstration if identified as **devnet**. Never auto-issue paid transactions; require explicit operator action.

### Journey E — Gemini API evaluation (P0 connected demo)
- An explicitly marked `Hosted Gemma API demo` pane uses `gemma-4-26b-a4b-it` via `google-genai`, with a **synthetic image or text log only**. Offline analysis continues on local E4B. Cloud response is labeled `HOSTED / GEMINI API`, is never silently mixed into local incident analysis, and secrets never appear in logs/screenshots.

### Journey F — Internet disconnect and resync (P0)
- User preloads model and cached maps, submits and edits two records without internet, then reconnects. Sync outbox lists deferred Snowflake/chain tasks; operator opts in to sending an allowed payload. Duplicate submissions prevented using idempotency keys. Failed sync remains pending with visible retry status.

## 6. Feature scope and priorities

### P0 — Must build and test
- Dashboard: KPIs (total, new, reviewed, high review priority), incident list, search, filters, status chips, relative timestamps, offline/online and provider health badges.
- New report form: required report text or image, optional confirmed coordinates, language hint, field reporter alias, created_at; image upload JPEG/PNG/WebP, <= 8MB, image dimensions guard, MIME sniffing, no public storage.
- Local AI: Ollama `gemma4:e4b` text and image endpoint; prompt template; guarded JSON parsing with Pydantic; original media/text immutable; low-confidence/unknown handling; per-request trace metadata with model, runtime, prompt version, duration (no secrets).
- Incidents: create/list/detail, coordinator-confirmed priority and status; AI summaries may be corrected manually with change history; CRUD soft-delete for local demo.
- Offline: SQLite WAL mode, per-upload local filesystem paths, durable outbox table, no external AI/map CDN calls required for the offline test. Bundle needed frontend assets and basic map geometry/tiles for chosen demo city.
- Maps: offline-capable Leaflet with bundled tiles or an appropriately licensed local static basemap; only confirmed coordinates produce pins; zoom, marker/filter interaction; omit live route ETA or safety assurances.
- Snowflake integration: real documented dataset provenance; allowlisted infrastructure schema, read-only SQL query over nearest locations, query result cache, health/error states, and CoCo transcript plus SQL committed under docs (without secrets).
- Solana: TypeScript registration script (`devnet` default), metadata file, link to transaction explorer, read-only status API and visibility of pending; real signature only if actual transaction succeeds.
- Hosted Gemini API evaluation: opt-in endpoint and script, Google SDK, real documented text/image call, failure state when absent API key, mode isolation.
- Public GitHub readiness: README, license, .gitignore, env example, setup/test/demo instructions, detailed Copilot evidence, reproducible fixture dataset, architecture diagram, self-assessment.
- Tests: unit/integration/frontend E2E plus no-network smoke (human-testable steps + script wherever feasible).

### P1 — Valuable if time allows
- Multilingual voice memo offline transcription; language selector Urdu/Hindi/Punjabi/English with corrections.
- Local queued geodata import/refresh for chosen region; drag/drop location pin and shelter list.
- Duplicate report detection (text + time + location) with human confirmation; batch ingest of synthetic reports.
- Privacy-safe agent uptime diagnostics: collect local service-health heartbeat aggregates and optionally publish a hash/attestation through a **documented SDK-supported** Solana validation mechanism after explicit operator approval and reconnection; label self-reported uptime as self-reported, not independently verified.
- Export PDF/CSV of redacted report summaries.
- Stable prioritized filters and map/list cross-highlighting.

### P2 — Not in initial hackathon demo
- Automated rescue dispatch, autonomous road routing, SMS/WhatsApp integration, real-time emergency alerts, public citizen portal, blockchain storage of private reports, continuous monitoring, production identity management.

## 7. UX specification

**Design direction:** Serious, operational, dark navy or slate surface, restrained red/orange for high review priority, teal for confirmed status, neutral gray for unknown. No sensational danger claims. Responsive desktop-first for coordinator, mobile-width intake. Keyboard accessible, WCAG 2.2 AA as target.

**Screens / routes:**
- `/` **Operations Overview**: system mode banner (`LOCAL / ONLINE SERVICES AVAILABLE` or `LOCAL / OFFLINE`), KPIs, 2-column map + incident feed, filters, warning about advisory AI.
- `/reports/new` **Report Intake**: language hint, multilingual free text, image picker and thumbnail, optional lat/lon pin or manual precise location, submit, local model status.
- `/incidents/:id` **Incident Detail**: source report, image, translated message, extracted fields, suggested priority with reasons and unknowns, human approval controls, activity and sync history, read-only infrastructure panel.
- `/integrations` **Integrations/Evidence**: Ollama model health, Gemini API `NOT_CONFIGURED/READY/DEMO_RUN`, Snowflake health/cache, Solana devnet asset/signature, evidence reference links; operator-only actions and warning labels.
- `/demo` **Guided Demo**: load synthetic fixtures, offline procedure, run-safe scripted demonstrations, not falsely marking mocks as live.

**Status language:** `UNREVIEWED`, `IN_REVIEW`, `VERIFIED_BY_HUMAN`, `NEEDS_MORE_INFO`, `CLOSED`. Review priority `CRITICAL_REVIEW`, `HIGH_REVIEW`, `NORMAL_REVIEW`, `UNKNOWN`; never claim to be a real emergency service triage classification. Show data source tags `REPORTED`, `AI_INTERPRETED`, `HUMAN_CONFIRMED`.

**Operational guardrails:** Always present a banner: 'Prototype decision support. AI output is unverified. Do not use for emergency dispatch or structural safety assessment.'

## 8. System architecture

```text
Browser (React/Vite, bundled local assets)
   | localhost HTTP
FastAPI (127.0.0.1:8000)
   |--- SQLite (incidents, evidence, outbox, sync attempts)
   |--- Local media store (metadata-stripped derivatives; protected paths)
   |--- GemmaProvider interface
   |      |--- OllamaLocalProvider -> http://127.0.0.1:11434 (DEFAULT)
   |      `--- GeminiHostedDemoProvider -> Gemini API (manual, non-sensitive)
   |--- TriageRuleEngine -> advisory classification only
   |--- InfrastructureProvider
   |      |--- Cached/Offline Infrastructure SQLite read
   |      `--- SnowflakeProvider -> restricted remote SQL when online
   `--- Evidence/Sync service
          `--- Solana registrar TypeScript CLI (explicit devnet action)
```

**Offline means no request leaves this machine for core inference or storage.** External services are modular and always opt-in. Cloud integration may be installed/configured but must never be called in the core offline path. A browser's network `navigator.onLine` is not sufficient to prove connectivity; implement explicit service health checks and show last known health.

## 9. Proposed repository layout

```text
rescuebridge-ai/
  AGENTS.md
  LICENSE
  README.md
  .env.example
  .gitignore
  Makefile
  docker-compose.yml            # optional: local services, no cloud LLM
  frontend/
    package.json
    src/{app,pages,components,hooks,lib,types,assets}/
    public/offline-map/          # provenance/attribution documented
  backend/
    pyproject.toml
    app/
      main.py
      api/{reports,incidents,health,integrations}.py
      core/{config,security,logging}.py
      models/{db,schemas}.py
      services/{gemma_local,gemini_hosted,snowflake,triage,media,sync}.py
      prompts/{incident_v1.txt,image_v1.txt}
      data/{db,fixtures}/
    tests/{unit,integration}/
  integrations/
    solana/{package.json,src/register.ts,src/verify.ts}
    snowflake/{schema.sql,seed.sql,queries.sql}
    gemini_demo/{run.py}
  docs/
    PRD.md
    ARCHITECTURE.md
    OFFLINE_PROOF.md
    INTEGRATION_EVIDENCE.md
    COPILOT_EVIDENCE.md
    DEMO_SCRIPT.md
    SECURITY.md
    SOURCE_DATA.md
    screenshots/
  scripts/{dev.sh,seed_demo.sh,check_offline.sh,verify_demo.sh}
  .github/workflows/ci.yml
```

## 10. Backend API contract (v1)

All responses use a consistent envelope `{data, meta, error}` where `error` is structured and non-sensitive. Use opaque UUIDs as incident IDs. JSON is UTF-8; timestamps UTC ISO-8601.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Backend + SQLite + provider status, no secrets |
| GET | `/api/v1/settings/runtime` | Configured local model/tag, execution mode, offline readiness |
| POST | `/api/v1/reports` | Multipart report + optional image and location; creates incident |
| POST | `/api/v1/incidents/{id}/analyze` | Re-run local Gemma analysis; version old results |
| GET | `/api/v1/incidents` | Filter and paginate incidents |
| GET | `/api/v1/incidents/{id}` | Full record, derived fields, history |
| PATCH | `/api/v1/incidents/{id}` | Human status/priority/coordinates corrections |
| GET | `/api/v1/incidents/{id}/media/{media_id}` | Authorized local media (never static public path) |
| GET | `/api/v1/infrastructure/nearby?lat=&lon=&radius_m=` | Cached or remote, provenance and fetched_at |
| POST | `/api/v1/incidents/{id}/infrastructure/refresh` | Explicit remote lookup when configured |
| GET | `/api/v1/integrations/status` | Providers, their modes, last success, last error |
| POST | `/api/v1/evaluation/gemini/analyze` | Explicit opt-in synthetic hosted Gemma evaluation |
| GET | `/api/v1/solana/identity` | Local record of agent + explorer link, no wallet keys |
| GET | `/api/v1/outbox` | Queued remote operations, retries, state |
| POST | `/api/v1/outbox/{id}/retry` | Explicit operator-driven synchronization |

**Error design:** invalid MIME `415`, input too large `413`, validation `422`, missing local model `503` with next action, remote provider unavailable `503` without blocking incidents, explicit cloud demo without key `412`, unexpected failure `500` sanitized.

## 11. Domain schemas and field definitions

### Incident
`id: uuid`, `created_at`, `updated_at`, `reporter_alias?`, `language_hint?`, `original_text`, `display_translation?`, `source_type` (TEXT/IMAGE/TEXT_AND_IMAGE/AUDIO), `category?` (FLOOD, ROAD_DAMAGE, MEDICAL, SHELTER, FOOD_WATER, OTHER), `summary?`, `reported_people_affected? integer`, `reported_needs: string[]`, `hazards_observed: string[]`, `location_text?`, `latitude?`, `longitude?`, `location_provenance` (USER_CONFIRMED/UNKNOWN/HUMAN_CONFIRMED), `review_priority`, `priority_reason`, `review_status`, `human_notes`, `ai_analysis_id?`, `is_synthetic boolean`, `revision integer`.

### AIAnalysis
`id`, `incident_id`, `provider` (`ollama_local`/`gemini_hosted_evaluation`), `model_identifier`, `runtime_location` (`LOCAL`/`HOSTED`), `prompt_version`, `result_json`, `raw_response_redacted?`, `error_type?`, `duration_ms`, `created_at`, `reviewed_by_human boolean`.

### Media
`id`, `incident_id`, `filename_sanitized`, `mime_detected`, `storage_relative_path`, `sha256`, `bytes`, `metadata_stripped boolean`, `created_at`; image metadata and upload paths must not be returned to frontend.

### InfrastructureAsset
`asset_id`, `name`, `type`, `latitude`, `longitude`, `source_dataset`, `source_url`, `source_license`, `last_updated_at?`, `last_fetched_at`, `record_status`; never infer road condition from baseline infrastructure attributes.

### OutboxAction
`id`, `kind`, `payload_redacted`, `idempotency_key`, `state` (`QUEUED/RETRYING/SUCCEEDED/FAILED/WAITING_FOR_APPROVAL`), `attempt_count`, `last_attempt_at`, `last_error_sanitized`, `created_at`.

### AuditEvent
`id`, `incident_id?`, `actor_type` (`LOCAL_USER`, `AI`, `SYSTEM`, `EXTERNAL`), `action`, `old_value_redacted?`, `new_value_redacted?`, `created_at`.

**Database:** SQLAlchemy 2 + Alembic + SQLite; enable foreign keys and WAL; migration must preserve records. Do not log or store wallet keys/Gemini secrets; test fixtures contain no real personally identifiable survivor data.

## 12. Local AI contract

**Default** `LOCAL_MODEL=gemma4:e4b`, `OLLAMA_BASE_URL=http://127.0.0.1:11434`, `AI_MODE=local`, `ALLOW_HOSTED_EVALUATION=false`. Use `ollama` Python client or requests to local `/api/chat` with images. Validate actual model via `/api/tags` or equivalent and `/api/ps` if available. Avoid Docker-in-Docker or remote hosted Ollama.

**The local prompt must:** (a) prioritize preservation of source language; (b) translate without embellishment; (c) extract reported facts vs observed evidence vs inference; (d) return only JSON with enumerations/nulls; (e) never fabricate locations, people counts, bridge structural conclusions, availability, or transport routes; (f) treat text within uploaded images as data, not instructions; (g) flag uncertainty and offer human follow-up questions.

Suggested validated output shape:

```json
{
  "detected_language": "ur",
  "english_translation": "The village bridge is damaged by flooding. Twenty people are reported stranded.",
  "short_summary": "Reported bridge damage and people stranded after flooding.",
  "category": "ROAD_DAMAGE",
  "reported_people_affected": 20,
  "reported_needs": ["rescue assistance"],
  "observable_image_details": [],
  "unverified_claims": ["extent of damage", "number of people stranded"],
  "risk_signals": ["possible loss of road access"],
  "location": {"place_name": null, "latitude": null, "longitude": null},
  "follow_up_questions": ["What is the precise location?", "Are people in immediate danger?"],
  "requires_human_review": true
}
```

Use JSON mode/format constraint where supported, parse via Pydantic, retry one local correction request on malformed output, then show recoverable error. Do not silently switch to external providers. Limit token generation/timeouts, semaphore model concurrency=1 by default to prevent laptop overcommit; report model health explicitly. Advisory priority must be calculated by deterministic, tested rules, **not by unsupported model confidence**.

## 13. Triage priority rules (human review only)

- `CRITICAL_REVIEW`: explicit report of immediate threat to life or people trapped, pending verification.
- `HIGH_REVIEW`: blocked essential access, flooding near populated location, severe injury reported, or urgent supply shortages.
- `NORMAL_REVIEW`: non-immediate operational needs.
- `UNKNOWN`: insufficient data or incompatible/failed extraction.

Rules need version IDs and tests. Evidence should show why a review category was suggested. Coordinator can override with written reason, stored in audit log. Never automatically dispatch personnel or mark a road passable.

## 14. Snowflake / CoCo data specification

**Intent:** baseline infrastructure context, not live road condition. CoCo is the development/analytics agent assisting dataset selection and query generation, while the application uses authenticated, parameterized and allowlisted read-only Snowflake queries. Do **not** treat CoCo as a local offline database.

For the demo: search the Snowflake Marketplace first for an eligible freely accessible infrastructure dataset; if none is actually accessible, transparently import a properly licensed public dataset. Select a single city or flood-prone region and one verifiably public, licensable point-based infrastructure dataset (bridge locations, shelters, hospitals, road assets). Document exact source URL, publisher, date, license, columns, transformation, and timestamp. Do not rely on nonexistent Snowflake Marketplace datasets. If the intended dataset cannot be accessed, use a labeled **synthetic data fixture** for UI development, but reserve live-evidence claims until the Snowflake query actually succeeds.

**Tables/views:** `INFRASTRUCTURE_ASSETS(asset_id, name, kind, latitude, longitude, source, dataset_date)`; optionally `SHELTERS` as public baseline locations. SQL shall use `ST_DWITHIN(TO_GEOGRAPHY(ST_MAKEPOINT(...)), ...)` only with the function signatures verified against current Snowflake docs, or precompute Haversine in read-only SQL if warranted. Use bind parameters and a maximum safe radius. Example docs should contain CoCo prompts, resulting *tested* SQL, and exact schema.

**Sync semantics:** default do not upload emergency report raw text, photos, names or coordinates to Snowflake. Only query public infrastructure. External sharing requires separate deliberate and minimally scoped authorization.

## 15. Solana spec

Use the official Solana-linked `8004-solana` TypeScript SDK in `integrations/solana`. Default `cluster: devnet`. Provide `register.ts`, `verify.ts`, and minimal public metadata (`name`, `description`, public endpoints only if actually available). Use a dedicated funded **demo-only** wallet; never commit private key, seed phrase, or keypair JSON. Devnet registration must be executed by an operator, not during npm install or frontend load. Confirm transaction success, persist only public signature/asset/address/network, and produce a valid Solana explorer URL `https://explorer.solana.com/tx/<signature>?cluster=devnet` (if verified on devnet). Do not emit 'registered' unless chain confirms. Local offline UI remains functional when chain is unavailable. Any public attestation should contain a hash of an **already-redacted synthetic evidence bundle**, never personal report content. Store local agent uptime diagnostics (e.g. local-model health, last successful inference, offline duration) without personal data. An optional explicit onchain validation/feedback demonstration may attest to a sanitized uptime digest only if supported by the installed SDK; distinguish self-attestation from independent verification and never claim unverified uptime as trusted evidence.

## 16. Hosted Gemini API evaluation spec

Use the supported `gemma-4-26b-a4b-it` model with `google-genai` in a standalone script plus a separate evaluation-only API path. Env key `GEMINI_API_KEY`. No key required to run the ordinary app. Hosted requests are disabled by default; operator opts in and receives a clear note that submitted demo content will leave the device. Never send real emergency information or personal images to this endpoint by default. Include command, logs/screenshot and test output as evidence.

## 17. Offline engineering requirements

- No CDN requests for React scripts, fonts, CSS, map tiles, icons or analytics in offline demo. All assets bundled/local.
- Cache geographically bounded map data in `frontend/public/offline-map/` with documented attribution and compatible license; acceptable alternative is a locally rendered static city grid underlay, clearly marked `Demo map`, combined with vector feature layers. Never promise an offline Google/OSM web tiles service without cached tiles.
- Ollama runs on device; frontend cannot call cloud LLM directly; no remote `Ollama Cloud` model tags.
- SQLite persists across restarts. Browser UI may use service worker/PWA caching only if verified; backend offline itself does not require PWA.
- Network status is a per-provider health read, not a boolean claim based solely on connectivity. When internet disconnects, queued operations remain local.
- `check_offline.sh` should verify local health and provide tested manual Wi-Fi-off steps; do not pretend to simulate full offline conditions by simply setting a frontend flag.

## 18. Security, privacy, ethical constraints

- No claim this is a live, authoritative emergency operations tool. Do not deploy to real emergency teams without security, reliability, legal, accessibility and domain expert review.
- Treat every upload, transcript and image as untrusted. Prompt injection protection through instruction/data boundaries and strict schema; no untrusted content passed as executable code/SQL.
- Limit file size and allowed formats; validate MIME and magic bytes; random file naming; strip EXIF; forbid SVG/HTML uploads; path traversal defense.
- Clear local-only data controls including demo wipe/reset after confirmation; avoid keeping real sensitive materials.
- CORS allowlist localhost origins; never put secrets in JavaScript client; redact logs, mask traceback details; basic local auth for state changes if practical.
- Configurable retention; default demo fixture data may persist, unneeded media removable; explain backup of SQLite and source media.
- Minimize information sent to connected services and Solana; send no images/name/location of real victims onchain.
- Document Gemma 4 model license separately: **MIT license only applies to our source code**, not automatically to model weights.

## 19. Test and quality gate

### Backend
- Pytest: schema validation, translations preserved, wrong JSON handled, upload restrictions, image preprocessing, SQLite restart persistence, deterministic triage, sync queue retry and idempotency, mocked errors from each provider, unknown coordinates not created.

### Frontend
- Vitest/React Testing Library and Playwright: intake submission, incident list, detail correction, filter, online indicators, initial empty state, local health errors, responsive mobile form and accessible labels.

### Integration
- Real local Ollama test (explicitly marked environment-dependent); one PNG and one Urdu text fixture, store outputs with timestamp/model metadata, no external calls.
- Google Gemini API script tested online with synthetic fixtures and API key; evidence required but CI must not require secrets.
- Snowflake query tested with permitted account; output includes evidence, not secrets.
- Solana devnet register + verify script returns real signature; manual key/wallet step required.

### Offline E2E
- Pre-pull model, install dependencies, and cache map data; disconnect WAN physically or disable Wi-Fi. Start local services, submit report, attach image, run AI, review, modify, restart services, confirm persistent record and queued external tasks. Capture video/log and ensure no external network request; distinguish localhost requests from outbound network traffic.

### CI
- Formatting/lint checks; typecheck; backend unit tests; frontend unit tests and build; secret scanning; no live credentials required. Separate optional integration job with manual approval.

## 20. Dependencies and constraints

- Local hardware: verify the actual machine's RAM/GPU/OS. Start with E4B on a reasonably capable computer (16 GB system RAM or more is desirable, 24–32 GB preferable for margin, but performance must be measured). Model download/storage consumes several GB. Offer E2B as a **visible manual fallback** if E4B cannot run; never silently downgrade the required demo.
- Ollama tag **`gemma4:e4b`** (not unreliable unofficial short tags). Keep tag configurable.
- Snowflake CoCo CLI requires a paid account or dedicated CoCo trial; ordinary standard Snowflake trial alone is insufficient, per Snowflake guide dated Oct 19, 2026.
- Solana devnet access and funded devnet wallet required for real registration; RPC/key/metadata dependencies may fail and must have transparent failure states.
- GitHub Copilot requirement is separate from Codex: Codex writing code does **not** prove Copilot use. A human must actually use GitHub Copilot, retain the exact prompt and relevant before/after output, and commit evidence documentation.

## 21. Milestones (sequential gates, not promises)

- **M0 Setup:** Establish repo scaffold, tools, Ollama local E4B available, SQLite migrations, .env examples; document machine specs.
- **M1 Offline MVP:** Report intake, media, local Gemma extraction, incident dashboard, human review, durable data.
- **M2 Offline proof:** Map assets, test suite, full physical disconnect demonstration and report.
- **M3 Evaluation integrations:** Gemini hosted separate live proof, Snowflake/CoCo query, Solana devnet registration; all with explicit real evidence.
- **M4 Release:** README, AGENTS.md, source licensing, security review, genuine GitHub Copilot evidence, CI, public repository publish after secret scan.

Complete M0→M1→M2 before spending time polishing remote integrations. Never mark M3 as complete based solely on mocks.

## 22. Definition of done

The deliverable is ready for submission only when: local E4B can actually process an image and multilingual text while WAN is disconnected; a coordinator can inspect and edit resulting incidents in a persistent dashboard; the README provides a genuine runnable Gemma-via-Gemini-API example and at least one executed example; the Snowflake/CoCo integration has referenced and queried data with provenance; an agent is visibly registered on Solana with a verifiable transaction link; real GitHub Copilot assistance is documented; all applicable tests pass; source is published with MIT license and **no leaked credentials**. If a remote credential or account blocks a requirement, report that requirement as `BLOCKED`, not done.

## 23. Reference documentation (verify against current version before implementation)

- Local Gemma via Ollama: https://ai.google.dev/gemma/docs/integrations/ollama
- Ollama Gemma tags: https://ollama.com/library/gemma4
- Gemma via Gemini API: https://gemma.ai/deployment/gemini-api/
- Snowflake CoCo CLI quickstart: https://www.snowflake.com/en/developers/guides/getting-started-with-coco-cli/
- Solana Agent Registry: https://solana.com/agent-registry
- Solana TypeScript SDK: https://github.com/QuantuLabs/8004-solana-ts/blob/main/docs/QUICKSTART.md

*This specification intentionally distinguishes product work from proof of third-party account execution. Model download, API keys, Snowflake account, and funded Solana wallet are operator prerequisites; they cannot be truthfully simulated as completed integrations.*
