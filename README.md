# easy-local-llm

A minimal setup for trying local LLMs the easy way.

- Run `Ollama` on the host
- Run `LiteLLM` in Docker
- Use it from Python through an OpenAI-compatible API

## Requirements

- Python 3.12+
- Docker Desktop (recommended) or Docker Engine + Docker Compose
- `uv`
- `Ollama`

## Before Setup

If Docker is new to you, do this first:

1. Install and launch Docker Desktop.

   On Linux, install Docker Engine + Docker Compose and make sure the Docker daemon is running.

2. Verify that Docker is available:

```bash
docker --version
```

3. When you reach the LiteLLM startup step later, this is the command you will run:

```bash
./scripts/start_server.sh
```

## Setup

The installer assumes Docker is already installed and running.

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

This script uses Docker to start LiteLLM and waits until `http://localhost:4000/health` responds.

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

To see which model is currently selected:

```bash
./scripts/show_model.sh
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

Large local models can take a while to answer. If needed, increase the client timeout in `.env`:

```dotenv
LITELLM_TIMEOUT_SECONDS=180
```

## Register multiple models

For orchestration tools such as LangGraph, it is often better to expose several routed models at once.

1. Copy the example model catalog:

```bash
cp config/models.example.json config/models.json
```

2. Point `.env` at the file:

```dotenv
LITELLM_MODEL_CONFIG_FILE=config/models.json
LITELLM_DEFAULT_MODEL=local-llama32
```

3. Restart LiteLLM:

```bash
./scripts/restart_server.sh
```

The generated [`config/litellm.yaml`](/home/ishigaki/local-llm/config/litellm.yaml) will then publish every model alias in the JSON file.

## Python usage

```python
from app.llm_client import chat, chat_messages, configured_models

print(chat("Explain robotics briefly"))
print(configured_models())
print(
    chat_messages(
        [
            {"role": "system", "content": "Answer briefly."},
            {"role": "user", "content": "Explain robotics briefly"},
        ],
        model="local-llama32",
    )
)
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

## LangGraph integration

Install the optional orchestration dependencies:

```bash
uv sync --extra orchestration
```

Then run the sample workflow:

```bash
uv run python scripts/run_langgraph_debate.py
```

The sample graph lives in [`orchestrator/langgraph_workflow.py`](/home/ishigaki/local-llm/orchestrator/langgraph_workflow.py). It uses LiteLLM as the model gateway and LangGraph only for state orchestration, which keeps the responsibilities clean.

## More

- Japanese README: [`README.ja.md`](/home/ishigaki/local-llm/README.ja.md)
- Detailed setup and architecture: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- Design notes: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
