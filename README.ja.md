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
./scripts/start_server.sh
```

このスクリプトは Docker をバックグラウンドで起動し、`http://localhost:4000/health` が通るまで待機します。

3. 別ターミナルで動作確認

```bash
uv run python scripts/test_llm.py
```

うまくいけば `http://localhost:4000` 経由で、`.env` で選んだプロバイダに接続します。

停止するとき:

```bash
./scripts/stop_server.sh
```

再起動するとき:

```bash
./scripts/restart_server.sh
```

## `.env` でプロバイダとモデルを切り替える

`.env.example` を `.env` にコピーして、使いたいプロバイダに合わせて値を変えます。

```bash
cp .env.example .env
```

Ollama の例:

```dotenv
LITELLM_MODEL_NAME=local-llama32
LITELLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

OpenAI OSS の例:

```dotenv
LITELLM_MODEL_NAME=local-gpt-oss
LITELLM_PROVIDER=openai_oss
OPENAI_OSS_MODEL=gpt-oss:20b
```

OpenAI の例:

```dotenv
LITELLM_MODEL_NAME=cloud-openai
LITELLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

Gemini の例:

```dotenv
LITELLM_MODEL_NAME=cloud-gemini
LITELLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=...
```

その後、必要に応じてモデルを取得して LiteLLM を再起動します。OpenAI OSS をローカルで使うときは、先に `Ollama` にモデルを取得しておきます。

```bash
ollama pull llama3.2
./scripts/start_server.sh
```

OpenAI OSS の例:

```bash
ollama pull gpt-oss:20b
./scripts/start_server.sh
```

これでアプリ側のコードを変えずに、`.env` だけで切り替えられます。

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

ログを追いたい場合:

```bash
docker compose logs -f litellm
```

## More

- 詳しいセットアップと構成: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- 設計メモ: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
