#!/usr/bin/env bash
set -euo pipefail
(cd backend && python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000) &
backend_pid=$!
trap 'kill "$backend_pid"' EXIT
(cd frontend && npm run dev -- --host 127.0.0.1)
