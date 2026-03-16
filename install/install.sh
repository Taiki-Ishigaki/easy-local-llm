#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v ollama >/dev/null 2>&1; then
  curl -fsSL https://ollama.com/install.sh | sh
fi

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required for this project. Install Docker Desktop (or Docker Engine + Docker Compose) and start it first." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 is required. Install Docker Desktop or enable the Docker Compose plugin." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is installed, but the Docker daemon is not reachable. Start Docker Desktop and run this installer again." >&2
  exit 1
fi

cd "$PROJECT_ROOT"

uv sync
ollama pull phi3
docker compose build

echo "Installation complete"
