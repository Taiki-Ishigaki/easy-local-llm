from openai import APITimeoutError

from app.config import LITELLM_TIMEOUT_SECONDS
from app.llm_client import chat, configured_models


def main() -> None:
    models = configured_models()
    print(f"Configured models: {', '.join(models)}")
    try:
        print(chat("ロボットとはなんですか？"))
    except APITimeoutError as exc:
        raise SystemExit(
            "The request timed out before the selected model responded. "
            f"Current timeout: {LITELLM_TIMEOUT_SECONDS:.0f}s. "
            "If you are using a large local model such as gpt-oss:20b, try increasing "
            "LITELLM_TIMEOUT_SECONDS in .env, switching to a smaller model, or ensuring "
            "`ollama serve` is running."
        ) from exc


if __name__ == "__main__":
    main()
