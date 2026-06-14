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
        # Step 1: get existing history for this session
        history = conversation_store[session_id]
        
        # Step 2: add the new user message to history
        for m in request.messages:
            history.append({"role": m.role, "content": m.content})
        
        # Step 3: send full history to Groq
        response = client.chat.completions.create(
            model=request.model,
            messages=history
        )
        
        # Step 4: get reply
        assistant_reply = response.choices[0].message.content
        
        # Step 5: save assistant reply to history
        history.append({"role": "assistant", "content": assistant_reply})
        
        return ChatResponse(
            reply=assistant_reply,
            tokens_used=response.usage.total_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))