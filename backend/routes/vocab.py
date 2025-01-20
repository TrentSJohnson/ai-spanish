from fastapi import APIRouter, Depends
from controllers.vocab_controller import VocabController
from services.vocab_service import VocabService
from models.vocab_word import VocabWord
from models.requests.create_vocab_request import CreateVocabRequest
from models.requests.get_vocab_request import GetVocabRequest
from typing import List

router = APIRouter(prefix="/vocab")

# Dependency injection
async def get_controller():
    vocab_service = VocabService()
    return VocabController(vocab_service)

@router.post("/words", response_model=VocabWord)
async def create_vocab_word(
    request: CreateVocabRequest,
    controller: VocabController = Depends(get_controller)
) -> VocabWord:
    return await controller.create_vocab_word(request.word)

@router.get("/words", response_model=List[VocabWord])
async def get_vocab_words(
    request: GetVocabRequest = None,
    controller: VocabController = Depends(get_controller)
) -> List[VocabWord]:
    return await controller.get_vocab_words()
