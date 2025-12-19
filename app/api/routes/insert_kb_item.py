from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.response import KBResponse
from app.services.milvus_service import insert_knowledge_item

router = APIRouter()

class KBRequest(BaseModel):
    chatbot_id: str
    text: str
    source: str = "manual"

@router.post("/kb/insert", response_model=KBResponse)
async def add_knowledge_base_item(request: KBRequest):
    """
    Bir Chatbot'un bilgi bankasına (Milvus) yeni veri ekler.
    Otomatik olarak Embedding alır ve vektörleştirir.
    """
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Metin içeriği boş olamaz.")
    
    result = await insert_knowledge_item(
        chatbot_id=request.chatbot_id,
        text=request.text,
        source=request.source
    )

    return result