# Local Gemma 4 setup and physical offline verification

This is the most important prerequisite. **Codex is the coding agent; Gemma 4 E4B is the runtime AI model installed locally on the operator's computer.** They are not the same service.

## 1. Confirm computer capacity

Check RAM and free space. E4B in Ollama is a multi-gigabyte model; local inference may require substantially more memory than disk model size alone, depending on context size and hardware. Start with 16GB+ RAM where possible and prefer 24–32GB for headroom. Run short test cases and record actual results; there is no guaranteed performance on an unknown machine.

On macOS, open **Apple menu → About This Mac** to find chip and memory. On Windows use **Settings → System → About**. Linux users can use `free -h`. You do not need to run the AI model inside Codex; Codex must make the application connect to the local Ollama server.

## 2. Install and pull local model

- Download Ollama for your platform at https://ollama.com/download.
- Open a terminal (macOS Terminal, Windows PowerShell, Linux shell).

```bash
ollama --version
ollama pull gemma4:e4b
ollama list
ollama run gemma4:e4b "Translate this Urdu sentence to English: ہمیں مدد چاہیے"
```

Run `ollama serve` only if the Ollama app/service is not already serving requests. The app should connect to `http://127.0.0.1:11434`.

If E4B fails to load for memory reasons, capture actual error and manually test `gemma4:e2b` as a less resource-intensive option:

```bash
ollama pull gemma4:e2b
ollama run gemma4:e2b "Hello"
```

**Important:** E2B is a disclosed backup, not the silent default or proof of an E4B demo. Do not substitute an external hosted or cloud model and call it local.

## 3. Verify a genuine local API request

```bash
curl http://127.0.0.1:11434/api/tags
curl -sS http://127.0.0.1:11434/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma4:e4b","prompt":"Translate into English: ہمیں مدد چاہیے", "stream":false}'
```

A real response proves the host is running the model **on the local Ollama server**. It does not by itself prove complete offline operation; perform step 4 after app implementation.

## 4. Validate real offline mode after Codex implements the app

1. Download all packages and model and bundle offline map assets while online.
2. Start backend/frontend and Ollama and open the app through localhost.
3. Disable Wi-Fi and unplug/disconnect wired internet. Do not disable network loopback or kill Ollama.
4. Submit an Urdu message and a synthetic JPEG/PNG flood-road illustration. Observe local Gemma output, original text preserved, no invented coordinates, advisory priority and human-review badge.
5. Restart the frontend/backend; confirm incident saved in SQLite and local map still renders.
6. Inspect browser network panel and backend logs: AI requests must go to `127.0.0.1:11434`, not `generativelanguage.googleapis.com` or a third-party LLM endpoint.
7. Record the real result in `docs/OFFLINE_PROOF.md` using the template. Screenshot/log filenames must be real, not placeholders.

## 5. Distinguish other online components

- `Gemini API hosted Gemma` uses external internet, is opt-in, and requires a key; it is for challenge evaluation only.
- `Snowflake CoCo` uses an eligible connected Snowflake account and is not locally runnable as a public data warehouse in this architecture. Local SQLite caches relevant baseline data.
- `Solana Agent Registry` requires network and an explicit transaction. Local incident analysis must not depend on it.

## 6. Troubleshooting

- `ollama: command not found`: install Ollama and restart terminal / verify PATH.
- `model not found`: run `ollama pull gemma4:e4b`; confirm exact tag shown in `ollama list`.
- `connection refused localhost:11434`: launch Ollama service/app and test port; do not change to remote host.
- `out of memory`: close other apps, reduce context length, use smaller test image and, if required, manually select E2B while clearly disclosing fallback.
- `CORS / 404`: React should call the FastAPI backend; browser should not call Ollama directly. Backend service uses loopback Ollama API.
- `offline map blank`: ensure map tiles/basemaps are local and served from Vite/backend; remove third-party tile URLs and CDN assets.
