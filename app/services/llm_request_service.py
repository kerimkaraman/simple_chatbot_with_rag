from google import genai
import uuid
from dotenv import load_dotenv
from app.models.request import LLMRequest
from app.models.response import LLMResponse
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI-API-KEY"))

async def process_llm_request(request: LLMRequest) -> LLMResponse:
    try:
        ai_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=request.request_message, 
        )
        
        return LLMResponse(
                success=True,
                id=str(uuid.uuid4()),
                conversation_id=request.conversation_id, 
                response_message=ai_response.text
            )
    
    except Exception as e:
        return LLMResponse(
            success=False,
            id=str(uuid.uuid4()),
            conversation_id=request.conversation_id, 
            response_message=f"Hata oluştu: {str(e)}"
        )