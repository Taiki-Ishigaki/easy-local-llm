from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "litellm.yaml"


def main() -> None:
    model_name = os.getenv("LITELLM_MODEL_NAME", "local-phi3")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi3")
    ollama_api_base = os.getenv("OLLAMA_API_BASE", "http://host.docker.internal:11434")

    rendered = "\n".join(
        [
            "model_list:",
            f"  - model_name: {model_name}",
            "    litellm_params:",
            f"      model: ollama/{ollama_model}",
            f"      api_base: {ollama_api_base}",
            "",
        ]
    )

    CONFIG_PATH.write_text(rendered, encoding="utf-8")
    print(f"Rendered {CONFIG_PATH} with model {model_name} -> ollama/{ollama_model}")


if __name__ == "__main__":
    main()
