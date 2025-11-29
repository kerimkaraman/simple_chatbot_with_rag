from fastapi import APIRouter
from app.models.request import LLMRequest
from app.models.response import LLMResponse
from app.services.llm_request_service import process_llm_request

router = APIRouter()

@router.post("/LLM/LLMRequest")
async def create_llm_request(request: LLMRequest) -> LLMResponse:
    result = await process_llm_request(request)
    return result