# Local LLM (uv oriented design)

## 1. Purpose

Provide a **one‑command installable local LLM environment** that works across multiple operating systems.

Target OS:

* macOS
* Windows
* Ubuntu / Linux
* WSL

Main use cases:

* Research and experimentation
* LLM application development
* RAG experiments
* Agent development

---

## 2. Design Principles

Key design principles:

* OpenAI API compatible
* Runs on CPU-only systems
* Easy installation
* Minimal OS dependency
* Extensible architecture

---

## 3. System Architecture

```
Application
    │
    ▼
OpenAI API Client
    │
    ▼
LiteLLM Router
    │
    ├── Ollama (local models)
    ├── OpenAI (optional)
    ├── Claude (optional)
    └── Gemini (optional)
```

Roles:

| Component   | Role                  |
| ----------- | --------------------- |
| Application | User applications     |
| OpenAI API  | Unified API interface |
| LiteLLM     | Model routing         |
| Ollama      | Local inference       |

---

## 4. Directory Structure

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
    start_server.sh
    test_llm.py

pyproject.toml
uv.lock
README.md
```

---

## 5. Installation Flow

User commands:

```
git clone easy-local-llm
cd easy-local-llm
./install/install.sh
```

Windows:

```
install/install.ps1
```

Installation tasks:

* Install Ollama
* Create uv environment
* Install dependencies
* Download model
* Start API server

---

## 6. install.sh

```
#!/bin/bash

set -e

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Install uv if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup python environment
uv sync

# Pull default model
ollama pull phi3

echo "Installation complete"
```

---

## 7. pyproject.toml

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

---

## 8. LiteLLM Configuration

`config/litellm.yaml`

```
model_list:
  - model_name: local-phi3
    litellm_params:
      model: ollama/phi3
      api_base: http://localhost:11434
```

---

## 9. Start LiteLLM Server

`scripts/start_server.sh`

```
uv run litellm --config config/litellm.yaml
```

API endpoint:

```
http://localhost:4000
```

---

## 10. Python Client

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
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content
```

---

## 11. Test Script

`scripts/test_llm.py`

```
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

Run:

```
uv run python scripts/test_llm.py
```

---

## 12. Default CPU Model

Default model:

```
phi3
```

Reasons:

* small model
* fast CPU inference
* stable quality

---

## 13. Future Extensions

Possible extensions:

### RAG

* Chroma
* FAISS
* Weaviate

### Agents

* LangGraph
* CrewAI
* AutoGen

### Tool Calling

* function calling
* external APIs
* robot control

---

## 14. Research Benefits

Advantages of this architecture:

| Feature         | Benefit               |
| --------------- | --------------------- |
| Cross‑platform  | Mac / Windows / Linux |
| Unified API     | OpenAI compatible     |
| Local inference | No cloud required     |
| Cloud switching | Easy comparison       |

Example:

```
model="local-phi3"
```

can be changed to

```
model="gpt-4o"
```

without modifying application code.

---

## 15. Future GPU Architecture

Add GPU inference server:

```
LiteLLM
  ├─ Ollama
  └─ vLLM
```

This allows large models on GPU servers.

---

## 16. Minimal Stack

Minimum required components:

* Ollama
* LiteLLM
* Python (uv environment)

---

## 17. Target Users

* Researchers
* Developers
* Students
* AI application builders

---

## 18. Future Improvements

Possible improvements:

* Automatic hardware detection
* Automatic model selection
* GUI installer
* One‑click RAG setup
