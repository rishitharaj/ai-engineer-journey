# AI Engineer Journey 🚀

Documenting my hands-on path to becoming a production AI engineer.

## Phase 1 — FastAPI Chatbot (LIVE ✅)

A production-ready AI career coaching API with a real chat UI.
**Live Demo:** https://ai-engineer-journey-5lu6.onrender.com

### Architecture
User (Browser)

↓

HTML/CSS/JS Frontend

↓

FastAPI Backend (Python)

↓

Groq LLM (LLaMA 3.3 70B)

### Tech Stack
- FastAPI
- Groq LLM (llama-3.3-70b-versatile)
- Pydantic
- Deployed on Render

### Features
- JD analysis — extracts technical and soft skills
- Skill gap assessment with 1-5 rating system
- Personalised learning roadmap generation
- Multi-turn conversation with session memory
- Clear chat / reset session
- Conversation history endpoint
- Token usage tracking
- Auto-generated API docs at /docs
- Deployed on Render

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/chat/{session_id} | Send a message |
| GET | /api/v1/history/{session_id} | Get conversation history |
| DELETE | /api/v1/clear/{session_id} | Clear a session |
| GET | /health | Health check |

### Tech Stack
- FastAPI
- Groq LLM (LLaMA 3.3 70B)
- Pydantic
- Python 3.13
- Deployed on Render

---

## Roadmap
- **Phase 1** — FastAPI + Groq Chatbot ✅
- **Phase 2** — RAG Pipelines + Vector DBs ✅
- **Phase 3** — Multi-Agent Systems 🔜
- **Phase 4** — Production & Infrastructure
- **Phase 5** — Evaluation & Feedback Loops

---

## Built by
Rishitha Raj — transitioning from 12+ years in Program Management to AI Engineering.
[LinkedIn](https://www.linkedin.com/in/rishitharaj) | [GitHub](https://github.com/rishitharaj)