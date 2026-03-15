#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

set -a
if [[ -f .env ]]; then
  # Load the user's selected routing values.
  source .env
fi
set +a

provider="${LITELLM_PROVIDER:-ollama}"
route_name="${LITELLM_MODEL_NAME:-local-phi3}"

case "$provider" in
  ollama)
    target="ollama/${OLLAMA_MODEL:-phi3}"
    ;;
  openai_oss|openai-oss)
    target="ollama/${OPENAI_OSS_MODEL:-gpt-oss:20b}"
    ;;
  openai)
    target="openai/${OPENAI_MODEL:-gpt-4o-mini}"
    ;;
  gemini)
    target="gemini/${GEMINI_MODEL:-gemini-2.0-flash}"
    ;;
  *)
    target="unsupported provider: $provider"
    ;;
esac

echo "Route name : $route_name"
echo "Provider   : $provider"
echo "Target     : $target"
