# Practical Retrieval-Augmented Generation Workshop

A three-hour workshop for third- and fourth-year engineering students.

The project teaches three connected areas:

```text
PART 1 — INGESTION
PDFs -> pages -> chunks -> embeddings -> ChromaDB

PART 2 — RAG
question -> retrieval -> grounded prompt
         -> structured answer -> citation validation

PART 3 — TESTING & EVALUATION
retrieval checks -> generation checks -> citation checks
                 -> end-to-end evaluation
```

## Teaching design

The notebook is the primary teaching implementation. It defines and explains each
function directly rather than importing the implementation from `src/`.

After the complete system has been built in the notebook, the final section shows
how the same functions have been refactored into clean source modules.

## Technology

- Python 3.13
- Poetry
- LangChain document loading and recursive text splitting
- Sentence Transformers for local embeddings
- ChromaDB for vector storage and retrieval
- OpenAI Agents SDK with `gpt-4o-mini`
- Pydantic structured output

## Project structure

```text
practical-rag-workshop-v3/
├── data/knowledge_base/
├── notebooks/practical_rag_workshop.ipynb
├── src/rag_workshop/
│   ├── config.py
│   ├── schemas.py
│   ├── ingestion.py
│   ├── rag.py
│   ├── validation.py
│   └── evaluation.py
├── scripts/
│   ├── ingest.py
│   └── ask.py
├── tests/
├── pyproject.toml
└── .env.example
```

## Setup

```bash
poetry install
cp .env.example .env
```

Add an OpenAI API key to `.env`.

Register a notebook kernel:

```bash
poetry run python -m ipykernel install --user   --name practical-rag-workshop   --display-name "Practical RAG Workshop"
```

Start Jupyter:

```bash
poetry run jupyter lab
```

## Reference implementation

After completing the notebook, the same pipeline can be run from the terminal.

Build the knowledge base:

```bash
poetry run python scripts/ingest.py
```

Ask a question:

```bash
poetry run python scripts/ask.py   "Can a frontline support agent approve an £80 refund?"
```

Show retrieved context:

```bash
poetry run python scripts/ask.py   "How long should a courier wait for an unavailable customer?"   --show-context
```

Database updating, incremental indexing and deployment are deliberately outside scope.
