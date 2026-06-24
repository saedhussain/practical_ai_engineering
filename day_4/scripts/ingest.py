from rag_workshop.ingestion import run_ingestion


def main() -> None:
    summary = run_ingestion(reset=True)
    print("Ingestion complete")
    for name, value in summary.items():
        print(f"- {name}: {value}")


if __name__ == "__main__":
    main()
