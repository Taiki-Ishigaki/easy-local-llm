#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

if [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
  "$PROJECT_ROOT/.venv/bin/python" scripts/chat_cli.py "$@"
  exit 0
fi

if command -v uv >/dev/null 2>&1; then
  uv run python scripts/chat_cli.py "$@"
  exit 0
fi

if command -v python3 >/dev/null 2>&1; then
  python3 scripts/chat_cli.py "$@"
  exit 0
fi

echo "Python runtime not found. Run \`uv sync\` first." >&2
exit 1
