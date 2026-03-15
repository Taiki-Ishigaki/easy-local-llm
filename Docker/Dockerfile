FROM python:3.11-slim

WORKDIR /app

RUN pip install uv
RUN uv pip install --system \
    "litellm[proxy]>=1.76.0" \
    "openai>=2.28.0" \
    "httpx>=0.28.1" \
    "numpy>=2.4.3"

COPY . .
