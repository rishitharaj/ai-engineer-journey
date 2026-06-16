from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.rag_chain import rag_query
from app.embedder import initialise_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Job Market Intelligence API",
    description="RAG-powered job market intelligence for India's tech industry",
    version="2.0.0"
)

# initialise vector store on startup
@app.on_event("startup")
async def startup_event():
    print("Initialising vector store...")
    initialise_vector_store()
    print("Vector store ready!")

class QueryRequest(BaseModel):
    question: str
    n_results: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list
    tokens_used: int

@app.post("/api/v2/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = rag_query(request.question, request.n_results)
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            tokens_used=result["tokens_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "component": "RAG pipeline"}