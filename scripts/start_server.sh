#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

. "$SCRIPT_DIR/compose_mode.sh"

parse_compose_mode_args "$@"
require_linux_for_hostnet

cd "$PROJECT_ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required to run LiteLLM. Install Docker Desktop (or Docker Engine + Docker Compose) first." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required. Install Docker Desktop or enable the Docker Compose plugin." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is installed, but the Docker daemon is not reachable. Start Docker Desktop and try again." >&2
  exit 1
fi

if [[ "$compose_mode" == "linux-hostnet" ]]; then
  echo "Starting LiteLLM with docker-compose.linux-hostnet.yml"
fi

run_compose up --build -d

echo "Waiting for LiteLLM on http://localhost:4000/health ..."

for _ in $(seq 1 60); do
  if health_response="$(curl -fsS http://localhost:4000/health 2>/dev/null)" && [[ -n "$health_response" ]]; then
    echo "LiteLLM is ready at http://localhost:4000"
    exit 0
  fi

  sleep 1
done

echo "Timed out waiting for LiteLLM to become healthy." >&2
run_compose logs --tail=50 litellm >&2 || true
exit 1
