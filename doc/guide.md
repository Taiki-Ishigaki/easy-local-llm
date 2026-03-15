# easy-local-llm Guide

`easy-local-llm` は、ホスト上の `Ollama` と Docker 上の `LiteLLM` を組み合わせて、ローカル LLM を OpenAI 互換 API として使うための最小構成です。

日本語のクイックスタートは [`README.ja.md`](/home/ishigaki/local-llm/README.ja.md)、英語の簡易版は [`README.md`](/home/ishigaki/local-llm/README.md) を参照してください。

## Architecture

```text
Host machine
  Ollama
    -> http://localhost:11434

Docker
  LiteLLM router
    -> http://localhost:4000

Application
  Python client
```

デフォルト設定:

- LiteLLM model name: `local-phi3`
- Ollama model: `phi3`
- LiteLLM endpoint: `http://localhost:4000`
- LiteLLM -> Ollama: `http://host.docker.internal:11434`
- `.env` で上書き可能

## Directory structure

```text
easy-local-llm/
├── app/
│   ├── config.py
│   └── llm_client.py
├── config/
│   └── litellm.yaml
├── doc/
│   ├── guide.md
│   └── plan.md
├── Docker/
│   └── Dockerfile
├── install/
│   ├── install.ps1
│   └── install.sh
├── scripts/
│   ├── sitecustomize.py
│   ├── start_server.sh
│   └── test_llm.py
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## Setup details

### macOS / Linux / WSL

```bash
./install/install.sh
```

### Windows

```powershell
install/install.ps1
```

インストールスクリプトで行うこと:

- `Ollama` がなければ導入
- `uv` がなければ導入
- `uv sync`
- `ollama pull phi3`
- `docker compose build`

## Start services

まずホストで Ollama を起動します。

```bash
ollama serve
```

次に LiteLLM を起動します。

```bash
docker compose up
```

または:

```bash
./scripts/start_server.sh
```

## Test

別ターミナルで:

```bash
uv run python scripts/test_llm.py
```

このテストは `app/llm_client.py` から LiteLLM に接続し、最終的にホストの `phi3` モデルへ到達します。

## Python usage

```python
from app.llm_client import chat

print(chat("Explain robotics briefly"))
```

内部では OpenAI 互換クライアントを使っています。

```python
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything",
)
```

## LiteLLM routing

[`config/litellm.yaml`](/home/ishigaki/local-llm/config/litellm.yaml) は起動時に自動生成されます。

```yaml
model_list:
  - model_name: local-phi3
    litellm_params:
      model: ollama/phi3
      api_base: http://host.docker.internal:11434
```

`host.docker.internal` を使うことで、Docker コンテナからホスト上の Ollama に接続できます。[`docker-compose.yml`](/home/ishigaki/local-llm/docker-compose.yml) では Linux 向けに `host-gateway` も指定しています。

### Model switching with `.env`

まず `.env.example` をコピーします。

```bash
cp .env.example .env
```

例:

```dotenv
LITELLM_MODEL_NAME=local-llama32
OLLAMA_MODEL=llama3.2
OLLAMA_API_BASE=http://host.docker.internal:11434
```

このとき:

- `LITELLM_MODEL_NAME` はアプリから指定する論理名
- `OLLAMA_MODEL` はホストの Ollama に入っている実モデル名

モデルを取得したあとに LiteLLM を再起動します。

```bash
ollama pull llama3.2
docker compose up --build
```

## Troubleshooting

### Ollama 側を先に確認

```bash
ollama list
curl http://localhost:11434/api/tags
```

### 次に API 層を確認

```bash
uv run python scripts/test_llm.py
```

Ollama は見えているのにテストが失敗する場合は、Docker ネットワークか LiteLLM 設定が原因のことが多いです。

### uv cache

[`uv.toml`](/home/ishigaki/local-llm/uv.toml) で uv の cache をプロジェクト内に寄せています。通常は `UV_CACHE_DIR` を手動で設定しなくても動きます。
