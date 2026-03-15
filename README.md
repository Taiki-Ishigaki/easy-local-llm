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
docker compose up
```

or:

```bash
./scripts/start_server.sh
```

3. In another terminal, run the test

```bash
uv run python scripts/test_llm.py
```

If everything works, the request will go through `http://localhost:4000` and reach `phi3`.

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
