# Easy Local LLM (Minimal Semi‑Docker Architecture)

## 1. Purpose

Provide a **simple local LLM environment** that can be installed with minimal setup and used consistently across operating systems.

Design goal:

> The user should focus on **using LLMs**, not operating LLM infrastructure.

Target OS

* macOS
* Windows
* Ubuntu / Linux
* WSL

Typical usage

* Research experiments
* LLM application development
* Prompt testing
* Agent prototyping

---

# 2. Design Philosophy

This system intentionally keeps the architecture **minimal**.

Principles:

* OpenAI API compatible
* Minimal infrastructure
* Cross‑platform
* Easy to install
* Easy to understand

The system separates responsibilities:

| Component   | Responsibility          |
| ----------- | ----------------------- |
| Ollama      | Model execution         |
| LiteLLM     | API compatibility layer |
| Application | User code               |

The goal is to **avoid building a complex LLM platform**.

---

# 3. System Architecture

This project uses a **semi‑Docker architecture**.

Ollama runs on the host machine while the API layer runs in Docker.

```
Host Machine

  Ollama
  (local model execution)

        │
        │ http://localhost:11434
        ▼

Docker

  LiteLLM Router

        │
        ▼

Application
```

Roles

| Component   | Description                    |
| ----------- | ------------------------------ |
| Ollama      | Executes local models          |
| LiteLLM     | Provides OpenAI compatible API |
| Application | User research code             |

---

# 4. Directory Structure

```
easy-local-llm/

install/
  install.sh
  install.ps1

config/
  litellm.yaml

app/
  llm_client.py

scripts/
  test_llm.py

Docker/
  Dockerfile

pyproject.toml
uv.lock

docker-compose.yml

README.md
```

---

# 5. Installation Flow

User setup

```
git clone easy-local-llm
cd easy-local-llm
./install/install.sh
```

Windows

```
install/install.ps1
```

Installation steps

1. Install Ollama
2. Install uv
3. Pull default model
4. Build Docker container

---

# 6. install.sh

```
#!/bin/bash

set -e

echo "Installing Ollama"

curl -fsSL https://ollama.com/install.sh | sh


echo "Installing uv"

curl -LsSf https://astral.sh/uv/install.sh | sh


echo "Pulling default model"

ollama pull phi3


echo "Building docker image"

docker compose build


echo "Installation complete"
```

---

# 7. Python Environment (uv)

`pyproject.toml`

```
[project]
name = "easy-local-llm"
version = "0.1.0"

dependencies = [
  "litellm",
  "openai",
  "httpx",
  "numpy"
]
```

uv is used for

* dependency management
* reproducible environments

---

# 8. LiteLLM Configuration

`config/litellm.yaml`

```
model_list:
  - model_name: local-phi3

    litellm_params:

      model: ollama/phi3

      api_base: http://host.docker.internal:11434
```

`host.docker.internal` allows containers to access the host Ollama server.

---

# 9. Docker Compose

`docker-compose.yml`

This container runs LiteLLM and connects to Ollama running on the host machine.

To ensure compatibility across operating systems, the configuration explicitly
allows the container to access the host network.

```
version: "3"

services:

  litellm:

    build: ./Docker

    ports:

      - "4000:4000"

    volumes:

      - ./config:/app/config

    extra_hosts:

      - "host.docker.internal:host-gateway"

    command: >
      uv run litellm --config config/litellm.yaml
```

Explanation

* `host.docker.internal` allows Docker containers to access services running on the host.
* `extra_hosts: host.docker.internal:host-gateway` ensures this works on Linux.

This keeps the same connection configuration across

* macOS
* Windows
* Linux
* WSL

LiteLLM can therefore consistently access Ollama using

```
http://host.docker.internal:11434
```

---

# 10. Dockerfile

```
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install uv

RUN uv pip install --system litellm openai httpx numpy

COPY . .
```

---

# 11. Start Server

Start LiteLLM container

```
docker compose up
```

API endpoint

```
http://localhost:4000
```

---

# 12. Health Check and Connectivity

To avoid debugging complexity, connectivity should be verified in two steps.

Step 1 — Verify Ollama on the host

```
ollama list
```

or

```
curl http://localhost:11434/api/tags
```

Step 2 — Verify LiteLLM through the API layer

```
python scripts/test_llm.py
```

If step 1 works but step 2 fails, the issue is likely related to Docker networking or LiteLLM configuration.

This separation simplifies troubleshooting.

---

# 13. Python Client

```
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./

RUN pip install uv

RUN uv pip install --system litellm openai httpx numpy

COPY . .
```

---

# 11. Start Server

```
docker compose up
```

API endpoint

```
http://localhost:4000
```

---

# 12. Python Client

`app/llm_client.py`

```
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything"
)


def chat(prompt):

    resp = client.chat.completions.create(

        model="local-phi3",

        messages=[{"role":"user","content":prompt}]

    )

    return resp.choices[0].message.content
```

---

# 13. Test Script

`scripts/test_llm.py`

```
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

Run

```
python scripts/test_llm.py
```

---

# 14. Model Management Policy

Model management is intentionally simple.

Rules

* Local models are managed by **Ollama**
* Model files remain on the **host machine**
* Docker containers do **not** store models

Advantages

* simple architecture
* no model duplication
* easy model updates

---

# 15. What This System Does NOT Include

To keep the system simple, the following features are **not included initially**:

* Vector databases
* RAG pipelines
* complex model caching
* multi‑GPU inference
* automatic hardware detection

These can be added later if needed.

---

# 16. Future Extensions (Optional)

If the project grows, the following may be added later.

Possible additions

* RAG systems
* vector databases
* evaluation pipelines
* agent frameworks

However the base design intentionally avoids these.

---

# 17. Minimal Stack

Host

* Ollama

Docker

* LiteLLM

Application

* Python client

This keeps the environment **easy to install and easy to understand**.

---

# 18. Target Users

* Researchers
* Developers
* Students

Anyone who wants a **simple local OpenAI‑compatible LLM environment**.
