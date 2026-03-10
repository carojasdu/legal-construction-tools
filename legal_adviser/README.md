# Legal Case Q&A System

A proof-of-concept (PoC) RAG pipeline for answering natural-language questions over a corpus of legal rulings related to social media. Built with LangChain, ChromaDB, and OpenAI.

## Problem

The goal is to accelerate legal case research by enabling plain-language queries over a database of prior rulings, rather than relying on manual document review.

## Architecture

**RAG pipeline:**

1. Each legal case (one Excel row = one case) is embedded as a single chunk using `text-embedding-3-small` (OpenAI).
2. Embeddings are stored and persisted in a local ChromaDB vector database.
3. At query time, the top k=3 semantically similar chunks are retrieved and passed as context to `gpt-4o-mini`, which generates a response in plain Spanish.

Keeping each case as a single chunk preserves the integrity of individual rulings and avoids fragmented context during retrieval.

LangChain is used to wire the retrieval chain. Total implementation cost: under $0.01 USD via personal API key.

## Setup

Requires an OpenAI API key.

1. Create a `.env` file:

   ```
   OPENAI_API_KEY=your-key-here
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Build the vector database (only needed once):

   ```bash
   python scripts/create_vector_database.py
   ```

4. Run the Q&A notebook or use the module directly:

   ```bash
   python scripts/instanciate_model.py
   ```

   Or open `scripts/01_question_answering.ipynb` for an interactive walkthrough with example queries.

## Results summary

The system performed well on thematic queries (e.g., "school bullying cases") — correctly identifying multiple relevant rulings and summarizing them in accessible language.

A known limitation: exact-term queries (e.g., acronyms like "PIAR") fail to retrieve relevant cases because semantic embeddings don't guarantee lexical matching. Hybrid retrieval (semantic + keyword search) is the recommended fix.

Conversational memory is not implemented — multi-turn queries that reference earlier answers need to be rephrased as self-contained questions.

See [Informe.md](Informe.md) for the full analysis including example Q&A outputs.

## Potential improvements

- **Hybrid retrieval:** Combine semantic search with BM25/keyword search to handle exact-term and acronym queries.
- **Conversational memory:** Add a conversation buffer so follow-up questions can reference earlier answers.
- **Chunking strategy:** For long rulings, split into sub-chunks with shared metadata, then retrieve all chunks belonging to a matched case. Balances retrieval granularity with case-level context integrity.
- **Larger embedding model:** `text-embedding-3-large` or a legal-domain-specific model for richer semantic representations.
- **Evaluation dataset:** Curate a benchmark with reference answers and expected source documents to systematically compare retrieval strategies using precision, recall, and answer quality metrics.
- **Production path:** Streamlit UI, managed cloud vector DB, logging and monitoring, guardrails for input/output validation.
