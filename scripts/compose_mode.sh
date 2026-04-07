#!/bin/bash

compose_mode="default"

parse_compose_mode_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --linux-hostnet)
        compose_mode="linux-hostnet"
        ;;
      -h|--help)
        print_compose_mode_help
        exit 0
        ;;
      *)
        echo "Unknown option: $1" >&2
        print_compose_mode_help >&2
        return 1
        ;;
    esac
    shift
  done
}

print_compose_mode_help() {
  echo "Usage: $(basename "$0") [--linux-hostnet]"
}

require_linux_for_hostnet() {
  if [[ "$compose_mode" == "linux-hostnet" ]] && [[ "$(uname -s)" != "Linux" ]]; then
    echo "--linux-hostnet is intended for Linux or WSL." >&2
    exit 1
  fi
}

run_compose() {
  if [[ "$compose_mode" == "linux-hostnet" ]]; then
    docker compose -f docker-compose.linux-hostnet.yml "$@"
  else
    docker compose "$@"
  fi
}
