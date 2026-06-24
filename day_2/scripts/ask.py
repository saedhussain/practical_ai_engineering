"""One-shot query to the workshop assistant.

Run with:

    poetry run python scripts/ask.py "what's the price of bitcoin in GBP?"

No session is used — each invocation is independent. For multi-turn
conversations, use scripts/chat.py instead.
"""

import argparse
import asyncio
import sys

from agents import Runner

from agent_workshop import build_assistant, settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ask the workshop assistant a single question."
    )
    parser.add_argument(
        "question",
        help="The question to ask, in quotes.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"Override the model (default: {settings.openai_model}).",
    )
    return parser.parse_args()


async def ask_one(question: str, model: str | None) -> str:
    agent = build_assistant(model=model)
    result = await Runner.run(agent, question)
    return result.final_output


def main() -> int:
    args = parse_args()
    try:
        answer = asyncio.run(ask_one(args.question, args.model))
    except Exception as exc:  # noqa: BLE001 — surface the error to the user
        print(f"⚠️  Agent error: {exc}", file=sys.stderr)
        return 1

    print(answer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
