from fastapi import APIRouter, HTTPException
from groq import Groq
from app.models.schemas import ChatRequest, ChatResponse, HistoryResponse, ClearResponse, Message
from app.config import SYSTEM_PROMPT
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

        if not history:
            history.append({
                "role": "system",
                "content": SYSTEM_PROMPT
            })

        for m in request.messages:
            history.append({"role": m.role, "content": m.content})

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


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    try:
        history = conversation_store.get(session_id, [])
        # filter out system prompt — users don't need to see it
        visible = [
            Message(role=m["role"], content=m["content"])
            for m in history
            if m["role"] != "system"
        ]
        return HistoryResponse(
            session_id=session_id,
            messages=visible,
            total_messages=len(visible)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear/{session_id}", response_model=ClearResponse)
async def clear_session(session_id: str):
    try:
        if session_id in conversation_store:
            del conversation_store[session_id]
        return ClearResponse(
            session_id=session_id,
            status="cleared"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))