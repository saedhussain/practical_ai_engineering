"""Interactive multi-turn chat with the workshop assistant.

Run with:

    poetry run python scripts/chat.py

The session persists to chat_history.db so you can quit, come back, and
continue the same conversation. Use a different session ID via --session
to start a fresh thread.
"""

import argparse
import asyncio
import sys

from agents import Runner, SQLiteSession

from agent_workshop import build_assistant, settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat with the workshop assistant.")
    parser.add_argument(
        "--session",
        default="default",
        help="Session ID. Use a different value to start a separate conversation.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"Override the model (default: {settings.openai_model}).",
    )
    return parser.parse_args()


async def chat_loop(session_id: str, model: str | None) -> None:
    agent = build_assistant(model=model)
    session = SQLiteSession(session_id, db_path=str(settings.sessions_db))

    print(f"🤖 Chat started — session {session_id!r}.")
    print("   Conversation is persistent. Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            return

        if not user_input:
            continue

        try:
            result = await Runner.run(agent, user_input, session=session)
        except Exception as exc:  # noqa: BLE001 — surface the error to the user
            print(f"\n⚠️  Agent error: {exc}\n")
            continue

        print(f"\nAgent: {result.final_output}\n")


def main() -> int:
    args = parse_args()
    asyncio.run(chat_loop(args.session, args.model))
    return 0


if __name__ == "__main__":
    sys.exit(main())
