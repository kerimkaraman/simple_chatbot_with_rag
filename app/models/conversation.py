from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    chatbot_id: str
    title: str = "Yeni Sohbet"
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True