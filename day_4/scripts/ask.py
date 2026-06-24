from __future__ import annotations

import argparse
import asyncio

from rag_workshop.rag import answer_question


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ask the AsterLane RAG system.")
    parser.add_argument("question")
    parser.add_argument("--top-k", type=int, default=4)
    parser.add_argument("--show-context", action="store_true")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    result = await answer_question(args.question, top_k=args.top_k)

    print("\nANSWER")
    print(result.answer.answer)
    print(f"\nAnswerable: {result.answer.answerable}")

    print("\nCITATIONS")
    if result.answer.citations:
        for citation in result.answer.citations:
            print(
                f"- {citation.source}, page {citation.page}, "
                f"chunk {citation.chunk_id}\n  \"{citation.quote}\""
            )
    else:
        print("- none")

    print(f"\nCitation validation: {result.citation_check.valid}")
    for error in result.citation_check.errors:
        print(f"- {error}")

    if args.show_context:
        print("\nRETRIEVED CONTEXT")
        for rank, chunk in enumerate(result.retrieved_chunks, start=1):
            print(
                f"\n[{rank}] {chunk.source}, page {chunk.page}, "
                f"distance={chunk.distance:.4f}\n{chunk.text}"
            )


if __name__ == "__main__":
    asyncio.run(main())
