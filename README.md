# easy-local-llm

`easy-local-llm` is a small local LLM starter kit built around `Ollama`, `LiteLLM`, and the OpenAI-compatible Python client.

The goal is to provide a simple local environment with an OpenAI API style interface, so application code can stay clean while model routing is handled by LiteLLM.

## What this project does

- Runs local models with `Ollama`
- Exposes them through `LiteLLM`
- Calls them from Python with the standard `openai` client
- Keeps the structure simple enough to extend later to OpenAI, Claude, or Gemini

## Architecture

```text
Application
    ->
OpenAI-compatible client
    ->
LiteLLM router
    ->
Ollama local model
```

Current default route:

- LiteLLM model name: `local-phi3`
- Ollama model: `phi3`
- LiteLLM endpoint: `http://localhost:4000`

## Directory structure

```text
easy-local-llm/
├── app/
│   └── llm_client.py
├── config/
│   └── litellm.yaml
├── doc/
│   └── plan.md
├── install/
│   ├── install.ps1
│   └── install.sh
├── scripts/
│   ├── start_server.sh
│   └── test_llm.py
├── config.py
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.12+
- `uv`
- `Ollama`
- A local model installed in Ollama, such as `phi3`

## Setup

### macOS / Linux / WSL

```bash
./install/install.sh
```

This script:

- installs `Ollama` if needed
- installs `uv` if needed
- runs `uv sync`
- pulls the default model `phi3`

### Windows

Run:

```powershell
install/install.ps1
```

## Start Ollama

Make sure the Ollama server is running.

Example:

```bash
ollama serve
```

If Ollama is already running in the background on your system, you can skip this step.

## Start LiteLLM

Start the LiteLLM proxy server with:

```bash
env DEBUG= .venv/bin/litellm -c config/litellm.yaml --telemetry False
```

After startup, the local OpenAI-compatible endpoint will be available at:

```text
http://localhost:4000
```

Notes:

- `DEBUG=release` in the shell environment can break LiteLLM startup
- `env DEBUG=` clears that value only for this command

## Run the test script

In another terminal:

```bash
env UV_CACHE_DIR=/tmp/uv-cache uv run python scripts/test_llm.py
```

This sends a prompt through:

- `scripts/test_llm.py`
- `app/llm_client.py`
- LiteLLM on port `4000`
- Ollama model `phi3`

## Python usage

Example client code:

```python
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

The client uses the OpenAI-compatible API:

```python
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything",
)
```

## Key files

- `app/llm_client.py`: Python chat client for LiteLLM
- `config/litellm.yaml`: LiteLLM routing config
- `config.py`: shared constants for endpoints and model names
- `scripts/start_server.sh`: helper script to start LiteLLM
- `scripts/test_llm.py`: minimal end-to-end test
- `install/install.sh`: setup script for macOS / Linux / WSL
- `install/install.ps1`: setup script for Windows
- `doc/plan.md`: design notes and target architecture

## Current configuration

The current LiteLLM config maps:

```yaml
model_list:
  - model_name: local-phi3
    litellm_params:
      model: ollama/phi3
      api_base: http://localhost:11434
```

This means application code calls `local-phi3`, while LiteLLM forwards requests to the local Ollama model `phi3`.

## Troubleshooting

### LiteLLM fails with `Invalid value for '--debug'`

Your shell may have:

```bash
DEBUG=release
```

Start LiteLLM like this:

```bash
env DEBUG= .venv/bin/litellm -c config/litellm.yaml --telemetry False
```

### `ModuleNotFoundError` for LiteLLM proxy dependencies

Run:

```bash
uv sync
```

This project needs `litellm[proxy]`, not only the base `litellm` package.

### Cannot connect to `localhost:11434`

Check that Ollama is running:

```bash
ollama list
ollama serve
```

### Cannot connect to `localhost:4000`

Check that LiteLLM is running and that `config/litellm.yaml` is loaded correctly.

## Future extension ideas

- Add OpenAI as an optional routed backend
- Add Claude or Gemini routes
- Add RAG components such as Chroma or FAISS
- Add agent workflows on top of the same client interface
