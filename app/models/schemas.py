from pydantic import BaseModel
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    # model: Optional[str] = "gpt-3.5-turbo"
    # temperature: Optional[float] = 0.7
    # max_tokens: Optional[int] = 150
    model : str = 'llama-3.3-70b-versatile'

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Message]
    total_messages: int

class ClearResponse(BaseModel):
    session_id: str
    status: str