import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from app.db.mongo import get_db
from app.core.constants import MONGO_MESSAGES_COLLECTION
from app.core.constants import MONGO_CHATBOTS_COLLECTION
from app.core.constants import MONGO_CONVERSATIONS_COLLECTION
from app.models.message import Message
from app.models.chatbot import Chatbot
from app.models.conversation import Conversation


class MongoService:

    async def create_message(self, conversation_id: str, chatbot_id: str, content: str, role: str):
        db = get_db()

        new_message = Message(
            conversation_id = conversation_id,
            chatbot_id = chatbot_id,
            content = content,
            role=role
        )

        message_dict = new_message.model_dump(by_alias=True)

        await db[MONGO_MESSAGES_COLLECTION].insert_one(message_dict)

    async def create_chatbot(self, model_name: str, name: str, temperature: float, system_instructions: str ):
        db = get_db()

        new_chatbot = Chatbot(
            model_name = model_name,
            name = name, 
            temperature = temperature,
            system_instructions = system_instructions,
        )

        chatbot_dict = new_chatbot.model_dump(by_alias=True)

        await db[MONGO_CHATBOTS_COLLECTION].insert_one(chatbot_dict)

        return new_chatbot.id


    async def create_conversation(self, chatbot_id: str, title: str):
        db = get_db()

        new_conversation = Conversation(
            chatbot_id = chatbot_id,
            title = title,
        )

        conversation_dict = new_conversation.model_dump(by_alias=True)

        await db[MONGO_CONVERSATIONS_COLLECTION].insert_one(conversation_dict)

        return new_conversation.id
    
    async def get_all_chatbots(self):
        db = get_db()

        cursor = db[MONGO_CHATBOTS_COLLECTION].find({}).sort("created_at", -1)

        chatbots = []
        async for doc in cursor:
            doc["id"] = doc["_id"]
            chatbots.append(doc)
        return chatbots
    
    async def get_single_chatbot(self, chatbot_id: str) -> Chatbot:
        db = get_db()

        cursor = await db[MONGO_CHATBOTS_COLLECTION].find_one({"_id": chatbot_id})
        if cursor:
            return Chatbot(**cursor)
        return None
    

    async def get_chat_history(self, conversation_id: str, limit: int = 6): # limiti son 6 mesaj olarak tuttuk şimdilik
        db = get_db()

        cursor = db[MONGO_MESSAGES_COLLECTION].find(
            {"conversation_id": conversation_id}
        ).sort("created_at", -1).limit(limit)

        history_list = []
        async for doc in cursor:
            role = doc.get("role", "unknown")
            content = doc.get("content", "")
            history_list.append(f"{role}: {content}")

        history_list.reverse()
        return "\n".join(history_list)

mongo_service = MongoService()