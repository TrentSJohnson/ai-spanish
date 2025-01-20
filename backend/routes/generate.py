from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import uuid
from typing import Dict
from services.ai_service import AIService

router = APIRouter(prefix="/api/v1/generate")

# Dependency injection
async def get_ai_service():
    return AIService()

# Store generated sentences with their IDs
sentences_store: Dict[str, str] = {}

class SentenceResponse(BaseModel):
    id: str
    sentence: str

class CheckRequest(BaseModel):
    id: str
    sentence: str

@router.post("/sentence")
async def generate_sentence(ai_service: AIService = Depends(get_ai_service)) -> SentenceResponse:
    generated_sentence = await ai_service.generate_sentence()
    sentence_id = str(uuid.uuid4())
    sentences_store[sentence_id] = generated_sentence
    
    return SentenceResponse(
        id=sentence_id,
        sentence=generated_sentence
    )

@router.post("/check")
async def check_sentence(
    request: CheckRequest,
    ai_service: AIService = Depends(get_ai_service)
) -> dict:
    if request.id not in sentences_store:
        raise HTTPException(status_code=404, detail="Sentence ID not found")
    
    original_sentence = sentences_store[request.id]
    is_correct, feedback = await ai_service.check_translation(
        original_sentence,
        request.sentence
    )
    
    return {
        "result": feedback
    }
