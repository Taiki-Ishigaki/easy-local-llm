# easy-local-llm

A minimal setup for trying local LLMs the easy way.

- Run `Ollama` on the host
- Run `LiteLLM` in Docker
- Use it from Python through an OpenAI-compatible API

## Requirements

- Python 3.12+
- Docker
- `uv`
- `Ollama`

## Setup

### macOS / Linux / WSL

```bash
./install/install.sh
```

### Windows

```powershell
install/install.ps1
```

## Quick Start

1. Start Ollama

```bash
ollama serve
```

2. Start LiteLLM

```bash
./scripts/start_server.sh
```

This script starts Docker in the background and waits until `http://localhost:4000/health` responds.

3. In another terminal, run the test

```bash
uv run python scripts/test_llm.py
```

If everything works, the request will go through `http://localhost:4000` and reach the provider selected in `.env`.

To stop LiteLLM:

```bash
./scripts/stop_server.sh
```

To restart LiteLLM:

```bash
./scripts/restart_server.sh
```

## Change provider and model with `.env`

Copy `.env.example` to `.env`, then update the values for the provider you want:

```bash
cp .env.example .env
```

Ollama example:

```dotenv
LITELLM_MODEL_NAME=local-llama32
LITELLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

OpenAI OSS example:

```dotenv
LITELLM_MODEL_NAME=local-gpt-oss
LITELLM_PROVIDER=openai_oss
OPENAI_OSS_MODEL=gpt-oss:20b
```

OpenAI example:

```dotenv
LITELLM_MODEL_NAME=cloud-openai
LITELLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

Gemini example:

```dotenv
LITELLM_MODEL_NAME=cloud-gemini
LITELLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=...
```

Then pull the model if needed and restart LiteLLM. For local OpenAI OSS, pull the model into `Ollama` first.

```bash
ollama pull llama3.2
./scripts/start_server.sh
```

OpenAI OSS example:

```bash
ollama pull gpt-oss:20b
./scripts/start_server.sh
```

This keeps your app code unchanged and switches the routed model through `.env`.

## Python usage

```python
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

The client uses the LiteLLM endpoint:

```python
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything",
)
```

To follow the LiteLLM logs:

```bash
docker compose logs -f litellm
```

## More

- Japanese README: [`README.ja.md`](/home/ishigaki/local-llm/README.ja.md)
- Detailed setup and architecture: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- Design notes: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
