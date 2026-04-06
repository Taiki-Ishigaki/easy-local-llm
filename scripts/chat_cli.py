from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Any

from openai import APIConnectionError, APITimeoutError, OpenAIError

from app.config import DEFAULT_MODEL, LITELLM_BASE_URL, LITELLM_TIMEOUT_SECONDS
from app.llm_client import completion, configured_models


COMMANDS = (
    "/help",
    "/models",
    "/model <alias>",
    "/reset",
    "/quit",
)


@dataclass
class ChatSession:
    model: str
    system_prompt: str | None = None
    messages: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": self.system_prompt})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interactive chat client for the routed LiteLLM endpoint.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="LiteLLM routed model alias to use.",
    )
    parser.add_argument(
        "--system",
        default=None,
        help="Optional system prompt to prepend to the conversation.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Optional sampling temperature passed to the chat completion API.",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="Print configured model aliases and exit.",
    )
    return parser.parse_args()


def print_help() -> None:
    print("Commands:")
    print("  /help           Show this help")
    print("  /models         Show locally configured model aliases")
    print("  /model <alias>  Switch model and reset the conversation")
    print("  /reset          Clear the conversation history")
    print("  /quit           Exit the chat")


def print_models(current_model: str, models: list[str]) -> None:
    if not models:
        print("No local model aliases are configured.")
        return

    print("Configured models:")
    for model in models:
        marker = "*" if model == current_model else " "
        print(f" {marker} {model}")


def run_completion(session: ChatSession, temperature: float | None) -> str:
    kwargs: dict[str, Any] = {}
    if temperature is not None:
        kwargs["temperature"] = temperature

    response = completion(
        messages=session.messages,
        model=session.model,
        **kwargs,
    )
    return response.choices[0].message.content or ""


def handle_command(raw: str, session: ChatSession) -> bool:
    command, _, value = raw.partition(" ")
    command = command.lower()
    value = value.strip()

    if command in {"/quit", "/exit"}:
        return False

    if command in {"/reset", "/clear"}:
        session.reset()
        print("Conversation reset.")
        return True

    if command == "/help":
        print_help()
        return True

    if command == "/models":
        print_models(session.model, configured_models())
        return True

    if command == "/model":
        if not value:
            print("Usage: /model <alias>")
            return True
        session.model = value
        session.reset()
        print(f"Switched to model: {session.model}")
        print("Conversation reset.")
        return True

    print(f"Unknown command: {raw}")
    print(f"Available commands: {', '.join(COMMANDS)}")
    return True


def main() -> None:
    try:
        import readline  # noqa: F401
    except ImportError:
        pass

    args = parse_args()
    models = configured_models()

    if args.list_models:
        print_models(args.model, models)
        return

    session = ChatSession(model=args.model, system_prompt=args.system)

    print("Interactive LiteLLM chat")
    print(f"Base URL: {LITELLM_BASE_URL}")
    print(f"Model: {session.model}")
    if models:
        print(f"Configured aliases: {', '.join(models)}")
    if session.system_prompt:
        print("System prompt: enabled")
    print("Type /help for commands.")

    while True:
        try:
            user_input = input("you> ").strip()
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nUse /quit to exit.")
            continue

        if not user_input:
            continue

        if user_input.startswith("/"):
            if not handle_command(user_input, session):
                break
            continue

        session.messages.append({"role": "user", "content": user_input})
        try:
            assistant_text = run_completion(session, args.temperature)
        except APITimeoutError:
            session.messages.pop()
            print(
                "Request timed out. "
                f"Current timeout: {LITELLM_TIMEOUT_SECONDS:.0f}s."
            )
            continue
        except APIConnectionError:
            session.messages.pop()
            print(
                "Could not reach LiteLLM. "
                f"Start the server and verify {LITELLM_BASE_URL}/health."
            )
            continue
        except OpenAIError as exc:
            session.messages.pop()
            print(f"Request failed: {exc}")
            continue

        session.messages.append({"role": "assistant", "content": assistant_text})
        print(f"assistant> {assistant_text}\n")


if __name__ == "__main__":
    main()
