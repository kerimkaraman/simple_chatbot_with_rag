from pydantic import BaseModel
from typing import List

class KnowledgeBaseItem(BaseModel):
    chatbot_id: str
    text: str
    source: str
    vector: List[float]        