#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

. "$SCRIPT_DIR/compose_mode.sh"

parse_compose_mode_args "$@"
require_linux_for_hostnet

cd "$PROJECT_ROOT"

echo "[1/5] Routed model"
"$SCRIPT_DIR/show_model.sh"
echo

echo "[2/5] LiteLLM health"
curl -fsS http://localhost:4000/health
echo
echo

echo "[3/5] LiteLLM models"
curl -fsS http://localhost:4000/v1/models
echo
echo

echo "[4/5] Ollama models on host"
ollama list
echo

echo "[5/5] Ollama reachability from LiteLLM container"
run_compose exec -T litellm python -c "import os, urllib.request; base=os.getenv('OLLAMA_API_BASE', 'http://host.docker.internal:11434'); print(urllib.request.urlopen(f'{base}/api/tags', timeout=5).read().decode())"
echo
echo "Checks completed."
