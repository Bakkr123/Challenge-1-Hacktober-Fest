#!/usr/bin/env bash
set -u
printf '%s\n' 'RescueBridge AI environment diagnostics'
uname -a
printf 'Python: '; python3 --version 2>&1 || true
printf 'Node: '; node --version 2>&1 || true
printf 'npm: '; npm --version 2>&1 || true
printf 'Git: '; git --version 2>&1 || true
printf 'Ollama CLI: '; ollama --version 2>&1 || printf '%s\n' 'NOT_VERIFIED (install Ollama or add CLI to PATH)'
printf 'Ollama models: '; ollama list 2>&1 || printf '%s\n' 'NOT_VERIFIED (Ollama service unavailable)'
printf 'Ollama API: '; curl -fsS --max-time 3 http://127.0.0.1:11434/api/tags >/dev/null 2>&1 && echo READY || echo NOT_READY
