from openai import OpenAI

from app.config import DEFAULT_ROUTED_MODEL, LITELLM_API_KEY, LITELLM_OPENAI_BASE_URL


client = OpenAI(
    base_url=LITELLM_OPENAI_BASE_URL,
    api_key=LITELLM_API_KEY,
    timeout=60.0,
)


def chat(prompt: str, model: str = DEFAULT_ROUTED_MODEL) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return resp.choices[0].message.content or ""
