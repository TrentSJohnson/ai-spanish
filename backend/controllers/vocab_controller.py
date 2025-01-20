from typing import List

from models.vocab_word import VocabWord
from services.vocab_service import VocabService


class VocabController:
    def __init__(self, vocab_service: VocabService):
        self.vocab_service = vocab_service

    async def create_vocab_word(self, word: str) -> VocabWord:
        vocab_word = VocabWord(word=word)
        return await self.vocab_service.create_vocab_word(vocab_word)

    async def get_vocab_words(self) -> List[VocabWord]:
        return await self.vocab_service.get_vocab_words()
