from pathlib import Path
import os


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


LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_OPENAI_BASE_URL = LITELLM_BASE_URL
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "anything")
DEFAULT_ROUTED_MODEL = os.getenv("LITELLM_MODEL_NAME", "local-phi3")
