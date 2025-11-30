from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id") 
    conversation_id: str
    chatbot_id: str
    content: str
    role: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True