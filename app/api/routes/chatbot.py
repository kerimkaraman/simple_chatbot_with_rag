from fastapi import APIRouter
from typing import List
from app.models.chatbot import Chatbot
from app.services.db_services import mongo_service

router = APIRouter()

@router.post("/chatbots", response_model=dict)
async def create_new_chatbot(chatbot: Chatbot):
    bot_id = await mongo_service.create_chatbot(
        model_name=chatbot.model_name,
        name=chatbot.name,
        temperature=chatbot.temperature,
        system_instructions=chatbot.system_instructions
    )
    return {"id": bot_id, "message": "Chatbot başarıyla oluşturuldu"}

@router.get("/chatbots")
async def list_chatbots():
    bots = await mongo_service.get_all_chatbots()
    return bots