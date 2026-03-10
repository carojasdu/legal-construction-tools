# Legal Case Q&A — Full Analysis

## Problem description

This project addresses the development of a system to accelerate legal case lookups over a database of prior rulings. The PoC responds to natural-language queries based on a collection of lawsuits related to social media, and validates the approach through a set of predefined test questions.

## Assumptions

To scope the PoC appropriately:

- Local, low-cost infrastructure is preferred over cloud-managed services, to validate technical feasibility quickly.
- No UI is required at this stage — the focus is on validating the RAG architecture and response quality.
- The provided dataset is assumed representative of real-world query characteristics.

These choices allow effort to concentrate on the core retrieval and generation pipeline, leaving UI and production infrastructure for a future iteration once the approach is proven viable.

## Approach and alternatives considered

Efficient retrieval over a knowledge base is a classical Information Retrieval problem, relevant here because the system must find legally relevant cases in response to natural-language queries.

Given the requirement for generative, natural-language answers, classical IR alone (keyword matching, BM25) is insufficient. The problem maps well to a **Retrieval-Augmented Generation (RAG)** pattern, where an LLM generates answers after its context is enriched with dynamically retrieved relevant documents.

### Alternatives evaluated

**1. Full-context window approach**

Models with context windows exceeding two million tokens could theoretically include the entire case database per query. However:
- Performance degrades in very long contexts (the "lost in the middle" problem)
- Per-call cost scales with full database size
- Scalability is limited as the knowledge base grows

**2. Fine-tuning a specialized model**

Training a model on domain-specific legal data is technically viable but was ruled out because:
- Higher implementation complexity and compute cost
- Poor flexibility for incorporating new cases without retraining
- Knowledge is "frozen" at training time

**3. RAG (selected)**

RAG was selected for combining:
- Focused contextual retrieval per query
- Natural scalability by adding documents to the vector store without touching the model
- Favorable cost-benefit ratio (no training required)
- Source traceability — critical for legal applications

## Technical implementation

### Data ingestion

Each row in the Excel file represents one complete legal case. Cases are embedded as single, atomic chunks to preserve case-level integrity — splitting cases across multiple chunks would risk fragmenting the context needed to answer questions coherently.

### Vector database

ChromaDB was selected for:
- Zero-configuration local persistence
- Open-source and free
- Straightforward LangChain integration

Embeddings: `text-embedding-3-small` (OpenAI). Retrieval strategy: top k=3 by cosine similarity.

### RAG chain

Implemented with LangChain's retrieval chain abstraction. The LLM (`gpt-4o-mini`, temperature=0.3) receives retrieved chunks as context and is prompted to respond in plain, accessible Spanish — avoiding legal jargon or explaining it when necessary.

Total implementation cost: < $0.01 USD via personal API key.

## Results

### Example Q&A outputs

**Q1 & Q2: What are the rulings of 3 cases? What were they about?**

> Claro, aquí te resumo las sentencias de tres demandas:
>
> 1. **Sentencia T-242/22** — Solicitud de nulidad presentada por Marcel Dousse y Daniel Mendoza Leal. La Corte rechazó las solicitudes por falta de argumentos que demostraran errores significativos en la decisión original.
>
> 2. **Sentencia T-452/22** — Director de cine Ciro Alfonso Guerra Picón alegó vulneración de sus derechos al buen nombre por un reportaje de acoso sexual. La Corte no protegió sus derechos, considerando que las periodistas actuaron dentro de la libertad de expresión y que el caso era de interés público.
>
> 3. **Sentencia C-487/23** — Análisis de constitucionalidad de penas de prisión por injuria y calumnia. La Corte declaró las normas válidas y no violatorias de la Constitución.

*(Questions 1 and 2 were combined into a single query because the system lacks conversational memory — it cannot reference cases mentioned in a prior turn.)*

**Q3: What was the ruling in the school bullying case?**

> Hay varios casos que tratan sobre acoso escolar:
>
> 1. **T-249/24 (Paola):** Acoso escolar causó depresión y ansiedad. La corte ordenó disculpas públicas e implementación de estrategias anti-acoso.
>
> 2. **T-449/23 (Sara):** Ciberacoso no investigado adecuadamente. La corte ordenó investigación y disculpas públicas.

**Q4: Detail the school bullying lawsuit.**

> 1. **T-249/24 (Camila y Paola):** La madre demandó por matoneo que causó problemas de salud mental. La escuela no actuó; la corte ordenó disculpas y revisión del manual de convivencia.
>
> 2. **T-449/23 (Sara):** Ciberacoso sin investigación. La corte ordenó investigación y garantizó continuidad educativa.
>
> 3. **T-252/23 (TBQ):** Acoso resultó en retiro del colegio. La corte ordenó medidas preventivas y un plan de reparación.

**Q5: Are there cases about the Plan Individual de Ajustes Razonables (PIAR)?**

> Lo siento, pero no tengo información específica sobre casos que hablen sobre el Plan Individual de Ajustes Razonables (PIAR). Los casos que tengo son sobre conflictos de jurisdicción en temas de recobros de prestaciones de salud, pero no mencionan el PIAR.

*(This is a retrieval failure — at least two PIAR-related cases exist in the dataset. See analysis below.)*

### Performance analysis

**Strength: Thematic queries**

The system handled thematic queries well — correctly identifying multiple relevant rulings and presenting them in clear, accessible language. Retrieval precision was high for queries with rich semantic content.

**Limitation: Conversational memory**

The system has no conversation buffer. Each query is treated independently, with no access to prior turns. This forced combining Q1 and Q2 into a single prompt to reference the same set of cases.

**Weakness: Exact-term retrieval (acronyms)**

The PIAR query failed despite confirmed matching cases in the dataset. Semantic embeddings capture conceptual similarity but do not guarantee lexical overlap with technical acronyms or specialized terminology. The recommended fix is hybrid retrieval — combining semantic search with keyword-based search (e.g., BM25) to capture both types of similarity.

## Conclusions

The PoC successfully validates the RAG approach for this use case. The system demonstrates:

- Accurate comprehension of natural-language queries
- Relevant case retrieval and coherent summarization
- Accessible, non-technical response generation

The identified limitations (conversational memory, exact-term retrieval) are not architectural dead-ends — they are well-understood problems with documented solutions, which strengthens the case for continuing development in this direction.
