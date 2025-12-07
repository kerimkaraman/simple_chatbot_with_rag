from google import genai
import uuid
from dotenv import load_dotenv
from app.models.request import LLMRequest
from app.models.response import LLMResponse
from app.core.prompts import create_rag_prompt
from app.services.db_services import mongo_service
from app.models.chatbot import Chatbot

import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI-API-KEY"))

def prepare_prompt_for_llm_request(question: str, context: str, history: str):
    context = create_rag_prompt(question=question, context=context, history=history)
    return context


async def process_llm_request(request: LLMRequest) -> LLMResponse:
    try:

        chatbot_id = request.chatbot_id if request.chatbot_id else "default_bot"
        model_name = "gemini-flash_latest"
        system_instructions = None


        await mongo_service.create_message(
            conversation_id=request.conversation_id,
            chatbot_id=chatbot_id,
            role="user",
            content=request.request_message
        )


        if chatbot_id != "default_bot":
            chatbot_settings = await mongo_service.get_single_chatbot(chatbot_id)
            if chatbot_settings:
                model_name = chatbot_settings.model_name
                system_instructions = chatbot_settings.system_instructions


        ai_response = client.models.generate_content(
            model = model_name,
            contents=prepare_prompt_for_llm_request(question=request.request_message, context="", history=""),
        )

        await mongo_service.create_message(
            conversation_id=request.conversation_id,
            chatbot_id=chatbot_id,
            role="model",
            content=ai_response.text
        )

        return LLMResponse(
                success=True,
                id=str(uuid.uuid4()),
                conversation_id=request.conversation_id, 
                response_message=ai_response.text
            )
    
    except Exception as e:
        print("Error: ", e)
        return LLMResponse(
            success=False,
            id=str(uuid.uuid4()),
            conversation_id=request.conversation_id, 
            response_message=f"Hata oluştu: {str(e)}"
        )