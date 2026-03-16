from app.llm_client import chat, configured_models


def main() -> None:
    models = configured_models()
    print(f"Configured models: {', '.join(models)}")
    print(chat("ロボットとはなんですか？"))


if __name__ == "__main__":
    main()
