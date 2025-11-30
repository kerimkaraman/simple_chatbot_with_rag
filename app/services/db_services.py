import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from app.db.mongo import get_db
from app.core.constants import MONGO_MESSAGES_COLLECTION
from app.models.message import Message

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

mongo_service = MongoService()