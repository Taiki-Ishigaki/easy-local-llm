# easy-local-llm

Local LLM を easy に試せる最小構成です。

- `Ollama` はホストで実行
- `LiteLLM` は Docker で実行
- Python から OpenAI 互換 API として利用

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

1. Ollama を起動

```bash
ollama serve
```

2. LiteLLM を起動

```bash
docker compose up
```

または:

```bash
./scripts/start_server.sh
```

3. 別ターミナルで動作確認

```bash
uv run python scripts/test_llm.py
```

うまくいけば `http://localhost:4000` 経由で `phi3` に接続します。

## Python usage

```python
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

クライアントは LiteLLM の endpoint を使います:

```python
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything",
)
```

## More

- 詳しいセットアップと構成: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- 設計メモ: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
