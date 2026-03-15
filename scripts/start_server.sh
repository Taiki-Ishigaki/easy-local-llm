#!/bin/bash

set -e

env DEBUG= PORT= .venv/bin/litellm -c config/litellm.yaml --port 4000
