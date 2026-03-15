from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "litellm.yaml"


def _provider_settings() -> tuple[str, list[str]]:
    provider = os.getenv("LITELLM_PROVIDER", "ollama").strip().lower()
    model_name = os.getenv("LITELLM_MODEL_NAME", "local-phi3")

    if provider == "ollama":
        ollama_model = os.getenv("OLLAMA_MODEL", "phi3")
        ollama_api_base = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434")
        return model_name, [
            "    litellm_params:",
            f"      model: ollama/{ollama_model}",
            f"      api_base: {ollama_api_base}",
        ]

    if provider in {"openai_oss", "openai-oss"}:
        openai_oss_model = os.getenv("OPENAI_OSS_MODEL", "gpt-oss:20b")
        ollama_api_base = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434")
        return model_name, [
            "    litellm_params:",
            f"      model: ollama/{openai_oss_model}",
            f"      api_base: {ollama_api_base}",
        ]

    if provider == "openai":
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return model_name, [
            "    litellm_params:",
            f"      model: openai/{openai_model}",
            "      api_key: os.environ/OPENAI_API_KEY",
        ]

    if provider == "gemini":
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        return model_name, [
            "    litellm_params:",
            f"      model: gemini/{gemini_model}",
            "      api_key: os.environ/GEMINI_API_KEY",
        ]

    raise SystemExit(f"Unsupported LITELLM_PROVIDER: {provider}")


def main() -> None:
    model_name, provider_lines = _provider_settings()

    rendered = "\n".join(
        [
            "model_list:",
            f"  - model_name: {model_name}",
            *provider_lines,
            "",
        ]
    )

    CONFIG_PATH.write_text(rendered, encoding="utf-8")
    print(f"Rendered {CONFIG_PATH} for routed model {model_name}")


if __name__ == "__main__":
    main()
