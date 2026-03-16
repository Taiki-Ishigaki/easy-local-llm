from collections.abc import Sequence
from typing import Any

from openai import OpenAI

from app.config import DEFAULT_MODEL, LITELLM_API_KEY, LITELLM_OPENAI_BASE_URL, model_aliases


client = OpenAI(
    base_url=LITELLM_OPENAI_BASE_URL,
    api_key=LITELLM_API_KEY,
    timeout=60.0,
)


Message = dict[str, Any]


def completion(
    messages: Sequence[Message],
    model: str = DEFAULT_MODEL,
    **kwargs: Any,
):
    return client.chat.completions.create(
        model=model,
        messages=list(messages),
        **kwargs,
    )


def chat_messages(
    messages: Sequence[Message],
    model: str = DEFAULT_MODEL,
    **kwargs: Any,
) -> str:
    resp = completion(messages=messages, model=model, **kwargs)
    return resp.choices[0].message.content or ""


def chat(prompt: str, model: str = DEFAULT_MODEL, **kwargs: Any) -> str:
    return chat_messages(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        **kwargs,
    )


def configured_models() -> list[str]:
    return model_aliases()


def build_langchain_chat_model(model: str = DEFAULT_MODEL, **kwargs: Any) -> Any:
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "langchain-openai is not installed. Install with `uv sync --extra orchestration`."
        ) from exc

    return ChatOpenAI(
        model=model,
        base_url=LITELLM_OPENAI_BASE_URL,
        api_key=LITELLM_API_KEY,
        timeout=60.0,
        **kwargs,
    )
