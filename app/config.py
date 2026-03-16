from dataclasses import dataclass
from pathlib import Path
import json
import os
from typing import Any


def _load_dotenv() -> None:
    dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


_load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_OPENAI_BASE_URL = LITELLM_BASE_URL
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "anything")
DEFAULT_ROUTED_MODEL = os.getenv("LITELLM_MODEL_NAME", "local-phi3")
PREFERRED_DEFAULT_MODEL = os.getenv("LITELLM_DEFAULT_MODEL", DEFAULT_ROUTED_MODEL)
MODEL_CONFIG_FILE = os.getenv("LITELLM_MODEL_CONFIG_FILE", "config/models.json")


@dataclass(frozen=True)
class ModelDefinition:
    model_name: str
    provider: str
    model: str
    api_base: str | None = None
    api_key_env: str | None = None


def _model_config_path() -> Path:
    path = Path(MODEL_CONFIG_FILE)
    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


def _single_model_definition() -> ModelDefinition:
    provider = os.getenv("LITELLM_PROVIDER", "ollama").strip().lower()

    if provider == "ollama":
        return ModelDefinition(
            model_name=DEFAULT_MODEL,
            provider=provider,
            model=os.getenv("OLLAMA_MODEL", "phi3"),
            api_base=os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434"),
        )

    if provider in {"openai_oss", "openai-oss"}:
        return ModelDefinition(
            model_name=DEFAULT_MODEL,
            provider="openai_oss",
            model=os.getenv("OPENAI_OSS_MODEL", "gpt-oss:20b"),
            api_base=os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434"),
        )

    if provider == "openai":
        return ModelDefinition(
            model_name=DEFAULT_MODEL,
            provider=provider,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key_env="OPENAI_API_KEY",
        )

    if provider == "gemini":
        return ModelDefinition(
            model_name=DEFAULT_MODEL,
            provider=provider,
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            api_key_env="GEMINI_API_KEY",
        )

    raise ValueError(f"Unsupported LITELLM_PROVIDER: {provider}")


def _normalize_definition(raw: dict[str, Any]) -> ModelDefinition:
    provider = str(raw["provider"]).strip().lower().replace("-", "_")
    if provider not in {"ollama", "openai_oss", "openai", "gemini"}:
        raise ValueError(f"Unsupported provider in model config: {provider}")

    api_base = raw.get("api_base")
    api_key_env = raw.get("api_key_env")
    return ModelDefinition(
        model_name=str(raw["model_name"]).strip(),
        provider=provider,
        model=str(raw["model"]).strip(),
        api_base=str(api_base).strip() if api_base else None,
        api_key_env=str(api_key_env).strip() if api_key_env else None,
    )


def load_model_definitions() -> list[ModelDefinition]:
    config_path = _model_config_path()
    if not config_path.exists():
        return [_single_model_definition()]

    raw_models = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw_models, list) or not raw_models:
        raise ValueError(f"Model config must be a non-empty list: {config_path}")

    return [_normalize_definition(item) for item in raw_models]


def model_aliases() -> list[str]:
    return [model.model_name for model in load_model_definitions()]


def default_model_name() -> str:
    aliases = model_aliases()
    if not aliases:
        return PREFERRED_DEFAULT_MODEL
    if PREFERRED_DEFAULT_MODEL in aliases:
        return PREFERRED_DEFAULT_MODEL
    return aliases[0]


DEFAULT_MODEL = default_model_name()
