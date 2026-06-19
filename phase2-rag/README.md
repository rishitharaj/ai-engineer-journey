cat > phase2-rag/README.md << 'EOF'
# Phase 2 — Job Market Intelligence RAG Pipeline

A Retrieval-Augmented Generation (RAG) system that answers questions about
tech job postings using real, grounded data instead of generic LLM knowledge.

---

## What it does

Ask a question like *"What skills do I need for a founding AI engineer role?"*
and the system:

1. Converts your question into a vector (embedding)
2. Searches a vector database of real job postings for semantically similar content
3. Retrieves the most relevant postings
4. Feeds them as context to an LLM
5. Returns an answer grounded in actual job market data — with sources cited

---

## Architecture

User Question

↓

Sentence Transformer (embed query)

↓

ChromaDB (semantic search over job postings)

↓

Top-K relevant job postings retrieved

↓

Groq LLM (LLaMA 3.3 70B) generates answer using retrieved context

↓

Answer + Sources + Token usage

---

## Pipeline Components

| File | Responsibility |
|---|---|
| `app/ingestor.py` | Loads job posting text files, splits into overlapping chunks |
| `app/embedder.py` | Converts chunks to vectors using Sentence Transformers, stores in ChromaDB |
| `app/retriever.py` | Performs semantic search — finds most relevant chunks for a query |
| `app/rag_chain.py` | Combines retrieval + LLM generation into one pipeline |
| `main.py` | FastAPI app exposing the RAG pipeline as an API |

---

## Tech Stack

- **FastAPI** — API framework
- **ChromaDB** — local vector database (persistent storage)
- **Sentence Transformers** (`all-MiniLM-L6-v2`) — text embeddings, runs locally
- **Groq** (LLaMA 3.3 70B) — LLM for answer generation
- **Cosine similarity** — semantic search scoring

---

## API

### `POST /api/v2/query`

**Request:**
```json
{
  "question": "What Python skills do AI engineering roles need?",
  "n_results": 3
}
```

**Response:**
```json
{
  "answer": "Based on the job postings...",
  "sources": ["job2.txt", "job4.txt", "job5.txt"],
  "tokens_used": 826
}
```

### `GET /health`
Returns API and pipeline status.

---

## Run Locally

```bash
cd phase2-rag
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to test interactively.

---

## Why RAG matters

Without RAG, an LLM only knows what it was trained on — generic, possibly
outdated information. With RAG, answers are grounded in real, current,
verifiable data, with sources cited for trust and auditability. This is the
core pattern behind production AI systems that work with private or
fast-changing data (legal documents, medical records, job postings,
internal company knowledge).

---

## What's Next — Phase 3

Phase 2 retrieves static job postings. Phase 3 builds on this foundation
with **multi-agent systems** (LangGraph) that can autonomously search,
reason, and act — for example, an agent that reads a JD, searches for
matching candidates, and drafts outreach messages.
EOF