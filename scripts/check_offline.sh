#!/usr/bin/env bash
set -euo pipefail

echo "Checking loopback services only. This does not simulate a disconnected WAN."
curl --fail --silent http://127.0.0.1:11434/api/tags >/dev/null && echo "Ollama: reachable" || echo "Ollama: unavailable"
curl --fail --silent http://127.0.0.1:8000/api/v1/health >/dev/null && echo "Backend: reachable" || echo "Backend: unavailable"
echo "For proof, disable Wi-Fi after dependencies, model, and map assets are cached."
