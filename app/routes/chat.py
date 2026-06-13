from fastapi import APIRouter, HTTPException
from groq import Groq
from app.models.schemas import ChatRequest, ChatResponse
from collections import defaultdict
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
conversation_store = defaultdict(list)

@router.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest):
    try:
        history = conversation_store[session_id]
        history.extend([{"role": m.role, "content": m.content} for m in request.messages])
        
        response = client.chat.completions.create(
            model=request.model,
            messages=history
        )
        
        assistant_reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_reply})
        
        return ChatResponse(
            reply=assistant_reply,
            tokens_used=response.usage.total_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))