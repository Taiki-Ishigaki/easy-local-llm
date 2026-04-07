#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

. "$SCRIPT_DIR/compose_mode.sh"

parse_compose_mode_args "$@"
require_linux_for_hostnet

cd "$PROJECT_ROOT"

run_compose stop litellm

echo "LiteLLM has been stopped."
