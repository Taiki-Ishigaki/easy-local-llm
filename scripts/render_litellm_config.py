from pathlib import Path
import json
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "litellm.yaml"
MODEL_CONFIG_FILE = os.getenv("LITELLM_MODEL_CONFIG_FILE", "config/models.json")


def _model_config_path() -> Path:
    path = Path(MODEL_CONFIG_FILE)
    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


def _single_model_settings() -> list[dict[str, str]]:
    provider = os.getenv("LITELLM_PROVIDER", "ollama").strip().lower()
    model_name = os.getenv("LITELLM_MODEL_NAME", "local-phi3")

    if provider == "ollama":
        ollama_model = os.getenv("OLLAMA_MODEL", "phi3")
        ollama_api_base = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434")
        return [
            {
                "model_name": model_name,
                "provider": provider,
                "model": ollama_model,
                "api_base": ollama_api_base,
            }
        ]

    if provider in {"openai_oss", "openai-oss"}:
        openai_oss_model = os.getenv("OPENAI_OSS_MODEL", "gpt-oss:20b")
        ollama_api_base = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434")
        return [
            {
                "model_name": model_name,
                "provider": "openai_oss",
                "model": openai_oss_model,
                "api_base": ollama_api_base,
            }
        ]

    if provider == "openai":
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return [
            {
                "model_name": model_name,
                "provider": provider,
                "model": openai_model,
                "api_key_env": "OPENAI_API_KEY",
            }
        ]

    if provider == "gemini":
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        return [
            {
                "model_name": model_name,
                "provider": provider,
                "model": gemini_model,
                "api_key_env": "GEMINI_API_KEY",
            }
        ]

    raise SystemExit(f"Unsupported LITELLM_PROVIDER: {provider}")


def _load_models() -> list[dict[str, str]]:
    config_path = _model_config_path()
    if config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or not raw:
            raise SystemExit(f"Model config must be a non-empty list: {config_path}")
        return raw

    return _single_model_settings()


def _provider_model(provider: str, model: str) -> str:
    normalized = provider.strip().lower().replace("-", "_")
    if normalized == "ollama":
        return f"ollama/{model}"
    if normalized == "openai_oss":
        return f"ollama/{model}"
    if normalized == "openai":
        return f"openai/{model}"
    if normalized == "gemini":
        return f"gemini/{model}"
    raise SystemExit(f"Unsupported provider in model config: {provider}")


def _render_model_block(model: dict[str, str]) -> list[str]:
    provider = str(model["provider"]).strip().lower().replace("-", "_")
    rendered = [
        f"  - model_name: {model['model_name']}",
        "    litellm_params:",
        f"      model: {_provider_model(provider, model['model'])}",
    ]
    api_base = model.get("api_base")
    api_key_env = model.get("api_key_env")
    if api_base:
        rendered.append(f"      api_base: {api_base}")
    if api_key_env:
        rendered.append(f"      api_key: os.environ/{api_key_env}")
    return rendered


def main() -> None:
    rendered_lines = ["model_list:"]
    for model in _load_models():
        rendered_lines.extend(_render_model_block(model))
    rendered = "\n".join([*rendered_lines, ""])

    CONFIG_PATH.write_text(rendered, encoding="utf-8")
    config_path = _model_config_path()
    source = config_path if config_path.exists() else "environment"
    print(f"Rendered {CONFIG_PATH} from {source}")


if __name__ == "__main__":
    main()
