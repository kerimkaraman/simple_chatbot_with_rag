from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Chatbot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    model_name: str = "gemini-flash-latest"
    temperature: float = 0.7
    system_instructions: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True