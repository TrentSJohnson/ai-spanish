from fastapi import APIRouter, Depends
from controllers.vocab_controller import VocabController
from services.vocab_service import VocabService
from models.vocab_word import VocabWord
from typing import List

router = APIRouter(prefix="/vocab")

# Dependency injection
async def get_controller():
    vocab_service = VocabService()
    return VocabController(vocab_service)

@router.post("/words", response_model=VocabWord)
async def create_vocab_word(
    word: str,
    controller: VocabController = Depends(get_controller)
) -> VocabWord:
    return await controller.create_vocab_word(word)

@router.get("/words", response_model=List[VocabWord])
async def get_vocab_words(
    controller: VocabController = Depends(get_controller)
) -> List[VocabWord]:
    return await controller.get_vocab_words()
