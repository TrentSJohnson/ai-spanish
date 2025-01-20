from fastapi import APIRouter, HTTPException, Depends
from controllers.generate_controller import GenerateController, SentenceResponse, CheckRequest
from services.ai_service import AIService

router = APIRouter(prefix="/api/v1/generate")

# Dependency injection
async def get_controller():
    ai_service = AIService()
    return GenerateController(ai_service)

@router.post("/sentence")
async def generate_sentence(
    controller: GenerateController = Depends(get_controller)
) -> SentenceResponse:
    return await controller.generate_sentence()

@router.post("/check")
async def check_sentence(
    request: CheckRequest,
    controller: GenerateController = Depends(get_controller)
) -> dict:
    success, feedback = await controller.check_sentence(request)
    if not success:
        raise HTTPException(status_code=404, detail=feedback)
    
    return {
        "result": feedback
    }
