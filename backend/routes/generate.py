from fastapi import APIRouter, HTTPException, Depends

from controllers.generate_controller import GenerateController
from models.requests.grade_request import GradeRequest
from models.responses.sentence_response import SentenceResponse
from models.translation_grade import TranslationGrade
from services.ai_service import AIService
from services.sentence_service import SentenceService
from services.translation_service import TranslationService
from services.vocab_service import VocabService

router = APIRouter(prefix="/generate")


# Dependency injection
async def get_controller():
    ai_service = AIService()
    sentence_service = SentenceService()
    translation_service = TranslationService()
    vocab_service = VocabService()
    return GenerateController(
        ai_service,
        sentence_service,
        translation_service,
        vocab_service
    )


@router.post("/sentence")
async def generate_sentence(
        controller: GenerateController = Depends(get_controller)
) -> SentenceResponse:
    return await controller.generate_sentence()

@router.post("/check", response_model=TranslationGrade)
async def check_translation(
        request: GradeRequest,
        controller: GenerateController = Depends(get_controller)
) -> TranslationGrade:
    return await controller.grade_translation(request)


