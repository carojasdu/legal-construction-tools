# Tools for legal construction firm

Two independent data science projects: time series forecasting for cost estimation, and a RAG-based system for querying a legal case database in natural language.

## Projects

### [cost-estimation/](cost-estimation/)

Forecasting construction equipment acquisition costs over a 3-year horizon using Facebook Prophet on historical material price time series data.

**Stack:** Python, Prophet, pandas, Jupyter

### [legal_adviser/](legal_adviser/)

A proof-of-concept RAG pipeline for natural-language question answering over a corpus of legal rulings. Uses semantic embeddings, ChromaDB, and GPT-4o-mini via LangChain.

**Stack:** Python, LangChain, ChromaDB, OpenAI API

## Setup

Both projects use [uv](https://docs.astral.sh/uv/) for dependency management. Navigate to the relevant directory and run:

```bash
uv sync
```

Alternatively, use your preferred virtual environment tool with the `pyproject.toml`. Code style is enforced with [ruff](https://docs.astral.sh/ruff/).
