from pydantic import BaseModel

class LLMRequest(BaseModel):
    id: str
    conversation_id: str
    request_message: str
    chatbot_id: str | None = None