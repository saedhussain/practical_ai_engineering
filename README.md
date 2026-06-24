# Practical AI Engineering

**A five-day intensive course on building real AI agent systems.**

This repo contains the notebooks, source code, scripts, and tests for a one-week course in practical AI engineering — aimed at people familiar with Python (intermediate level) who want to learn how working AI systems are actually built.

It's not a survey of every framework, model, or technique. It's a focused walk through a small set of production-quality patterns: how to design tools, how to give agents memory, how to orchestrate multiple agents, how to ground answers in your own data, and how to make all of it reliable enough to ship.

By the end of the week, you'll have built a multi-tool agent, a multi-agent system, a RAG pipeline, and a capstone project of your own design.

---

## What you'll learn

| Day | Topic | What you build |
|---|---|---|
| **Day 1** | Foundations — chat loops and the OpenAI Agents SDK | A chat loop from scratch, then re-built with the SDK |
| **Day 2** | Tools and memory | An agent with several tools and persistent sessions, refactored into a production-shaped Python package |
| **Day 3** | Multi-agent orchestration | Three orchestration patterns (Manager, Handoff, Code Driven) applied to real examples |
| **Day 4** | Retrieval-augmented generation | A complete RAG pipeline — ingestion, retrieval, grounded answers, citation validation, evaluation |
| **Day 5** | Capstone | Your own AI system, demoed to the class |

Each day has its own `README.md` with full detail. This top-level README is just the map.

---

## Repository layout

```
practical_ai_engineering/
├── day_1/                       # Foundations
│   ├── notebooks/
│   └── README.md
├── day_2/                       # Tools and memory
│   ├── notebooks/
│   ├── src/agent_workshop/     # production-quality refactor
│   ├── scripts/                # chat.py, ask.py CLIs
│   ├── tests/
│   └── README.md
├── day_3/                       # Multi-agent orchestration
│   ├── notebooks/
│   └── README.md
├── day_4/                       # RAG
│   ├── notebooks/
│   ├── src/rag_workshop/       # production-quality refactor
│   ├── scripts/                # ingest.py, ask.py CLIs
│   ├── tests/
│   ├── data/                   # sample knowledge base
│   └── README.md
├── day_5/                       # Capstone
│   ├── capstone_brief.md
│   └── README.md
├── outputs/                     # generated artefacts (markdown, etc.)
├── .env.example
├── pyproject.toml
└── README.md                    # you are here
```

Two notes on the layout:

- **`day_2/src/` and `day_4/src/`** are real Python packages (`agent_workshop` and `rag_workshop`) installed editably by Poetry. They're refactored, tested versions of the notebook code — useful as reference for what production-shaped agent code looks like.
- **Day 1, 3, and 5** are notebook-only. Day 3 teaches *patterns* rather than infrastructure; Day 5 is open project work. Neither needs its own package.

---

## Setup

You need:

- **Python 3.13** (this course is pinned to 3.13)
- **Poetry** for dependency management
- API keys for OpenAI, Tavily, and Hugging Face (free tiers work for all three)

### 1. Clone the repo

```bash
git clone <repo-url>
cd practical_ai_engineering
```

### 2. Install Python 3.13

Check what you have:

```bash
python3 --version
```

If you don't have 3.13:

**macOS:**

```bash
brew install python@3.13
```

Or with pyenv:

```bash
brew install pyenv
pyenv install 3.13.0
pyenv local 3.13.0
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3.13 python3.13-venv
```

Or with pyenv:

```bash
curl https://pyenv.run | bash
pyenv install 3.13.0
pyenv local 3.13.0
```

**Windows:**

Download the Python 3.13 installer from [python.org/downloads](https://www.python.org/downloads/) and run it. 
Tick **"Add Python to PATH"** during installation.

Verify with:

```powershell
python --version
```

### 3. Install Poetry

**macOS / Linux:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then add Poetry to your PATH (the installer prints the line to add, usually):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Windows (PowerShell):**

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Then add Poetry to your PATH — the installer prints the location, typically `%APPDATA%\Python\Scripts`.

Verify with:

```bash
poetry --version
```

### 4. Install the project

From the repo root:

```bash
poetry install
```

This creates a virtual environment, installs all dependencies, and installs the course packages (`agent_workshop`, `rag_workshop`) in editable mode.

### 5. Set up your environment file

Copy the example:

**macOS / Linux:**

```bash
cp .env.example .env
```

**Windows (PowerShell):**

```powershell
Copy-Item .env.example .env
```

Then open `.env` in your editor and fill in your keys:

- **`OPENAI_API_KEY`** — get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **`TAVILY_API_KEY`** — free tier at [tavily.com](https://tavily.com)
- **`HF_TOKEN`** — free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 6. Verify the setup

```bash
poetry run python -c "from agent_workshop import settings; print('OK')"
poetry run python -c "from rag_workshop import settings; print('OK')"
```

Both should print `OK`. If you see import errors, run `poetry install` again.

---

## Running things

All commands run from the repo root.

**Open a notebook:**

```bash
poetry run jupyter lab
```

Then navigate to `day_2/notebooks/`, `day_3/notebooks/`, etc.

**Try Day 2's CLI scripts:**

```bash
# One-shot question
poetry run python day_2/scripts/ask.py "What's the price of bitcoin?"

# Interactive chat
poetry run python day_2/scripts/chat.py
```

**Try Day 4's RAG scripts:**

```bash
# Build the knowledge base (only needed once)
poetry run python day_4/scripts/ingest.py

# Ask a question
poetry run python day_4/scripts/ask.py "What should a courier do when the customer cannot be reached?"
```

**Run the tests:**

```bash
poetry run pytest day_2/tests/ -v
poetry run pytest day_4/tests/ -v
```

---

## Course philosophy

This course is deliberately narrow. It doesn't try to cover every framework, model, or technique in AI engineering. Instead, it picks a small set of production-quality patterns and teaches them carefully.

Three principles shape the materials:

**Production-quality craft on a focused surface.** Each day teaches a small number of concepts deeply, with real engineering practices (testing, error handling, structured outputs, tracing) applied throughout. The goal is not breadth — it's depth on patterns you'll actually use.

**Notebooks for learning, modules for reference.** Each day's notebook is where you learn and experiment. The `src/` packages show what the same code looks like cleaned up into a real Python project. Read them when you want to see what good production code looks like.

**Build something every day.** Each day ends with a lab where you build a working system. By Friday, you've produced four working artefacts and a capstone — a real portfolio of practical work.

---

## Who this is for

Anyone comfortable with Python who wants to move beyond LLM API tutorials and learn how real AI systems are engineered

You should be comfortable with:

- Python 3 (functions, classes, type hints, async/await — at least the basics)
- The terminal and basic git
- Reading API documentation

You don't need prior experience with LLMs, agents, or AI frameworks. The course starts from first principles on Day 1.

---

## What's not covered

In the interest of focus, some adjacent topics are explicitly out of scope:

- **Deployment** — containers, Kubernetes, hosting, CI/CD. Day 4's appendix gives a brief map of what comes next; full deployment is a separate course.
- **Fine-tuning** — when to fine-tune vs prompt vs RAG is mentioned, but we don't train models.
- **Voice, vision, or multimodal** — text-only throughout.
- **Specific cloud platforms** — AWS, Azure, GCP. We use OpenAI's hosted API and a few free public APIs.
- **Heavy framework comparisons** — we use the OpenAI Agents SDK consistently; LangChain, LlamaIndex, AutoGen are mentioned but not taught.

The course teaches transferable patterns. If you learn it well, switching frameworks later is easy.

---

## License

[MIT](LICENSE) — feel free to fork, adapt, and reuse for your own teaching.

If you build something significant on this material, a note in the README is appreciated but not required.

---

## Acknowledgements

This course draws on excellent published material from several teams. Particular thanks to:

- The **OpenAI Agents SDK team** for the SDK and *A Practical Guide to Building Agents*
- The **Anthropic team** for *Building Effective Agents*
- **Mem0**, **Zep**, and **Letta** for clear writing on agent memory
- **CoALA paper** (Princeton, 2023) for the foundational vocabulary

Full citations live inside each day's notebooks.

---

## Getting unstuck

If something doesn't work:

1. Read the day's `README.md` — most setup issues are covered there
2. Check that `.env` has all three keys filled in
3. Try `poetry install` again from the repo root
4. Open an issue on this repo with: the day you're on, the command you ran, and the error you got

Good luck — and have fun building.
