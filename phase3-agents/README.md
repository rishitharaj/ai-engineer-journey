cat > README.md << 'EOF'
# Phase 3 — Multi-Agent Recruiting System with Observability

A LangGraph-based multi-agent pipeline that evaluates job descriptions
against real market data and generates structured candidate evaluation
rubrics — with full observability (latency, token usage, cost) on every
step, both locally and via Langfuse.

---

## What it does

Given a job description, the agent:

1. **Searches** Phase 2's vector database for similar real job postings
2. **Analyses** common skill requirements across those postings using an LLM
3. **Drafts** a weighted candidate evaluation rubric + targeted interview questions

Every step is traced — latency, tokens, model, and estimated cost — logged
to console, a local JSON file, and Langfuse's cloud dashboard.

---

## Architecture

Job Description

↓

┌─────────────────────┐

│ search_similar_jobs   │  ← semantic search over Phase 2's ChromaDB

└──────────┬────────────┘

↓

┌─────────────────────┐

│ analyse_skill_        │  ← LLM identifies common requirements

│ requirements           │

└──────────┬────────────┘

↓

┌─────────────────────┐

│ generate_evaluation_   │  ← LLM drafts weighted rubric + interview Qs

│ rubric                 │

└─────────────────────┘

↓

Final Output + Trace Log


Each node is wrapped in a custom tracer decorator that:
- Times execution (latency)
- Reads token usage from the LLM response
- Estimates cost from Groq's pricing
- Logs to `logs/traces.jsonl` and to Langfuse

---

## Tech Stack

- **LangGraph** — orchestrates the multi-step agent graph
- **Groq** (LLaMA 3.3 70B) — LLM for analysis and generation
- **ChromaDB** (shared with Phase 2) — vector search over job postings
- **Langfuse** (v4 SDK) — production tracing dashboard
- **FastAPI** — API layer

---

## API

### `POST /api/v3/evaluate`

**Request:**
```json
{
  "job_description": "Founding AI Engineer building RAG pipelines..."
}
```

**Response:**
```json
{
  "final_output": "Candidate Evaluation Rubric...",
  "trace_log": [
    {"node": "search_similar_jobs", "latency_ms": 352, "tokens_used": 0, "cost_usd": 0},
    {"node": "analyse_skill_requirements", "latency_ms": 2671, "tokens_used": 1054, "cost_usd": 0.000715},
    {"node": "generate_evaluation_rubric", "latency_ms": 1865, "tokens_used": 1278, "cost_usd": 0.000889}
  ]
}
```

---

## Run Locally

```bash
cd phase3-agents
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to test interactively.

---

## Why this matters

This phase directly mirrors core requirements from production AI engineering
roles: multi-agent orchestration, grounding in real data via RAG, and
observability — tracking latency, cost, and token usage per step so system
performance and spend are measurable, not guessed at.

---

## What's Next — Phase 4

Production hardening: containerization (Docker), latency optimization,
async pipelines, and proper data pipelines (Kafka/Airflow) for continuous
ingestion of new job postings.
EOF