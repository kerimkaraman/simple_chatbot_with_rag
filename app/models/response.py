from pydantic import BaseModel

class LLMResponse(BaseModel):
    success: bool
    id: str
    conversation_id: str
    response_message: str