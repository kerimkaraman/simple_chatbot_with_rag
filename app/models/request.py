from pydantic import BaseModel

class LLMRequest(BaseModel):
    id: str
    conversation_id: str
    request_message: str
    