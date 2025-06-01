# My AI Agent

A LangChain‑powered conversational agent built in Python. The project is scaffolded to grow from a single‑purpose bot to a fully‑featured service with memory, tools, and tests.

---

## 📑 Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Running the Agent](#running-the-agent)
5. [Testing](#testing)
6. [Linting & Formatting](#linting--formatting)
7. [Configuration](#configuration)
8. [Docker](#docker)
9. [Project Structure](#project-structure)
10. [Makefile Shortcuts](#makefile-shortcuts)
11. [Continuous Integration](#continuous-integration)

---

## ✨ Features

* **LangChain orchestration** — easily swap models or add tools.
* **Typed settings** using *Pydantic* and a single `settings.yaml`.
* **Pre‑commit hygiene** (Black + isort + Flake8 + MyPy) enforced automatically.
* **Pytest** with coverage from day one.
* **Docker‑ready** for reproducible production deployments.

---

## 🛠 Prerequisites

| Tool              | Version          | Notes                    |
| ----------------- | ---------------- | ------------------------ |
| Python            | 3.12 recommended | Any 3.11+ will do        |
| Poetry            | ≥ 1.8            | Handles venv & packaging |
| (Optional) Docker | ≥ 24.x           | For containerised runs   |

> **Heads‑up:** Make sure your `OPENAI_API_KEY` (or equivalent) is available—either in your shell or a `.env` file.

---

## 🚀 Quick Start

```bash
# 1 – clone and enter the repo
$ git clone https://github.com/<you>/my_ai_agent.git
$ cd my_ai_agent

# 2 – install deps (dev + prod)
$ poetry install --with dev

# 3 – set environment variables (copy the template)
$ cp config/.env.example .env  # then edit with your keys

# 4 – run the agent on a simple query
$ poetry run python src/scripts/run_agent.py "Hello, agent!"
```

---

## 🏃‍♂️ Running the Agent

```bash
# Direct script invocation
$ poetry run python src/scripts/run_agent.py "What's the weather in Tokyo?"

# Or install the package locally for `agent` CLI imports
$ poetry install
$ python - <<'PY'
from agent.core import run
print(run("Summarise LangChain in one sentence"))
PY
```

### Interactive REPL (optional)

Add a Typer `@app.command()` called `repl` that loops on `input()` and prints `run(query)`—handy for fast local hacking.

---

## ✅ Testing

```bash
# run all unit tests with coverage
$ poetry run pytest -q --cov=agent --cov-report=term-missing

# view an HTML coverage report
$ poetry run coverage html
$ open htmlcov/index.html
```

---

## 🧹 Linting & Formatting

```bash
# one‑off run on the whole repo
$ poetry run pre-commit run --all-files

# or rely on the git hook installed by
$ pre-commit install
```

Hot tip: add `make lint` in your *Makefile* to bundle this.

---

## ⚙️ Configuration

| File                   | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| `config/.env.example`  | Template for API keys and secrets              |
| `config/settings.yaml` | Default model, embeddings, vector store config |

Settings are loaded by a `Settings` class (`pydantic.BaseSettings`) so they can be overridden via env vars at runtime.

---

## 🐳 Docker

```bash
# build the image
$ docker build -t my_ai_agent:latest .

# run (mount .env or pass vars)
$ docker run --env-file .env my_ai_agent:latest "Rate the joke: Why did the python cross the road?"
```

The Dockerfile pins the same Poetry‑locked dependencies for deterministic builds.

---

## 🗂 Project Structure

```
my_ai_agent/
├── src/
│   ├── agent/              # Reusable library code
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── chains/
│   │   ├── prompts/
│   │   └── memory/
│   ├── scripts/
│   │   └── run_agent.py
│   └── tests/
├── config/
│   ├── settings.yaml
│   └── .env.example
├── docs/
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── Makefile
├── LICENSE
└── README.md
```

---

## 🛎 Makefile Shortcuts (optional)

Add these to `Makefile` if you like:

```makefile
install:
	poetry install --with dev

run:
	poetry run python src/scripts/run_agent.py $(q)

test:
	poetry run pytest -q

lint:
	poetry run pre-commit run --all-files
```

Use like `make run q="Hello there"`.

---

## 🤖 Continuous Integration

A minimal **GitHub Actions** workflow (`.github/workflows/ci.yml`):

```yaml
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snok/install-poetry@v1
      - name: Install deps
        run: poetry install --with dev
      - name: Lint & Test
        run: |
          poetry run pre-commit run --all-files
          poetry run pytest -q
```

---

Happy hacking! Feel free to tweak structure, swap vector stores, or add new LangChain tools as your agent’s skills expand.
