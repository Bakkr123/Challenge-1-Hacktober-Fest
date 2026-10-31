# RescueBridge AI

RescueBridge AI is an offline-first, human-supervised prototype for collecting
multilingual disaster reports and turning them into reviewable incident records.
The current development path uses the explicit hosted Gemma API evaluation
adapter. Snowflake/CoCo is intentionally out of scope for this submission
build.

This project is a decision-support prototype. AI output is unverified and must
not be used for emergency dispatch or structural safety decisions.

## Current status

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md). The repository is
being built in gates, starting with the local offline path.

## Local prerequisites

- Ollama with `gemma4:e4b` pulled locally
- Python 3.12 or 3.13 recommended
- Node.js and npm

Copy `.env.example` to `.env` and never commit `.env`. The current development
configuration selects the explicit hosted API mode; use `AI_MODE=local` when
you are ready to run the challenge-compliant offline path.

## Hosted Gemma API mode

For the current API-based development path, copy `.env.example` to `.env`, set
`GEMINI_API_KEY` to a newly generated Google AI Studio key, and keep:

```env
AI_MODE=hosted_gemma
ALLOW_HOSTED_EVALUATION=true
HOSTED_MODEL=gemma-4-26b-a4b-it
```

Install the backend dependencies, then run the API with:

```bash
python3 -m pip install -e './backend[dev]'
cd backend && python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The hosted evaluation endpoint is `POST /api/v1/evaluation/gemini/analyze`.
It requires `is_synthetic: true` and never silently falls back to a cloud
provider from the local path. The Google Gemma API model and image input flow
are documented by Google at
https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api.

Do not send real survivor reports, personal data, or real emergency images to
the hosted endpoint.

## Deliberately skipped challenge item

Snowflake/CoCo integration is not included by operator decision. The project
must not claim Snowflake evidence or mark that challenge item as complete.

## License

Application source is MIT licensed. Gemma model weights and external datasets
retain their own licenses and terms.
