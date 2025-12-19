from pydantic import BaseModel
from typing import List, Any

class LLMResponse(BaseModel):
    success: bool
    id: str
    conversation_id: str
    response_message: str

class KBResponse(BaseModel):
    success: bool
    message: str
    inserted_ids: List[Any] | None = None
    error: str | None = None