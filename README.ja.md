# easy-local-llm

Local LLM を easy に試せる最小構成です。

- `Ollama` はホストで実行
- `LiteLLM` は Docker で実行
- Python から OpenAI 互換 API として利用

## Requirements

- Python 3.12+
- Docker Desktop 推奨、または Docker Engine + Docker Compose
- `uv`
- `Ollama`

## セットアップ前に Docker を確認

Docker を使うのが初めてなら、先にここだけ確認してください。

1. Docker Desktop をインストールして起動します。

   Linux の場合は Docker Engine と Docker Compose を入れて、Docker daemon が起動している状態にします。

2. Docker が使えることを確認します。

```bash
docker --version
```

3. あとで LiteLLM を起動するときに使うコマンドはこれです。

```bash
./scripts/start_server.sh
```

## Setup

インストーラは Docker がインストール済みで、起動中である前提です。

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

このスクリプトは Docker を使って LiteLLM を起動し、`http://localhost:4000/health` が通るまで待機します。

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

現在どのモデルに向いているか確認するとき:

```bash
./scripts/show_model.sh
```

対話しながら使いたいとき:

```bash
./scripts/chat.sh
```

チャット中の主なコマンド:

```text
/help
/models
/model <alias>
/reset
/quit
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

ローカルの大きいモデルは返答に時間がかかることがあります。必要なら `.env` に次を追加してタイムアウトを延ばせます。

```dotenv
LITELLM_TIMEOUT_SECONDS=180
```

## 複数モデルを登録する

LangGraph のようなオーケストレーション層から使う場合は、LiteLLM に複数モデルを同時に公開しておく方が扱いやすいです。

1. ひな形をコピー

```bash
cp config/models.example.json config/models.json
```

2. `.env` で読み込む

```dotenv
LITELLM_MODEL_CONFIG_FILE=config/models.json
LITELLM_DEFAULT_MODEL=local-llama32
```

3. LiteLLM を再起動

```bash
./scripts/restart_server.sh
```

すると [`config/litellm.yaml`](/home/ishigaki/local-llm/config/litellm.yaml) に JSON 内の各モデル alias が並び、外部のオーケストレータから model 名で選べるようになります。

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

ターミナルで対話したい場合:

```bash
./scripts/chat.sh --system "短く答えてください。"
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

## LangGraph と統合する

オプション依存を入れます。

```bash
uv sync --extra orchestration
```

次にサンプルを実行します。

```bash
uv run python scripts/run_langgraph_debate.py
```

サンプルの graph は [`orchestrator/langgraph_workflow.py`](/home/ishigaki/local-llm/orchestrator/langgraph_workflow.py) にあります。LiteLLM をモデル gateway、LangGraph を状態管理と分岐に限定しているので、責務を分けたまま拡張しやすい構成です。

## More

- 詳しいセットアップと構成: [`doc/guide.md`](/home/ishigaki/local-llm/doc/guide.md)
- 設計メモ: [`doc/plan.md`](/home/ishigaki/local-llm/doc/plan.md)
