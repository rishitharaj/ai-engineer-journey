from fastapi import FastAPI
from app.routes.chat import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Chatbot API",
    description="Production chatbot built with FastAPI and Groq",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is running"}