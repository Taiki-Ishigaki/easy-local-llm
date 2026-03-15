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

3. In another terminal, run the test

```bash
uv run python scripts/test_llm.py
```

If everything works, the request will go through `http://localhost:4000` and reach `phi3`.

## Change model with `.env`

Copy `.env.example` to `.env`, then change the model values:

```bash
cp .env.example .env
```

```dotenv
LITELLM_MODEL_NAME=local-llama32
OLLAMA_MODEL=llama3.2
```

Pull the model and restart LiteLLM:

```bash
ollama pull llama3.2
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

## More

- Japanese README: [`README.ja.md`](/home/ishigaki/local-llm/README.ja.md)
- Detailed setup and architecture: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- Design notes: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
