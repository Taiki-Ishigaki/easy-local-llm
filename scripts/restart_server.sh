#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/stop_server.sh" "$@"
"$SCRIPT_DIR/start_server.sh" "$@"
