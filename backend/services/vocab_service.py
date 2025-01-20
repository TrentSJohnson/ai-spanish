from typing import List, Optional
from bson import ObjectId
from models.vocab_word import VocabWord
from services.db_service import BaseDBService

class VocabService(BaseDBService):
    async def create_vocab_word(self, vocab_word: VocabWord) -> VocabWord:
        result = await self.db.vocab_words.insert_one(vocab_word.dict(by_alias=True))
        return await self.get_vocab_word(result.inserted_id)

    async def get_vocab_word(self, word_id: ObjectId) -> Optional[VocabWord]:
        word_dict = await self.db.vocab_words.find_one({"_id": word_id})
        if word_dict:
            return VocabWord(**word_dict)
        return None

    async def get_vocab_words(self) -> List[VocabWord]:
        cursor = self.db.vocab_words.find()
        return [VocabWord(**doc) async for doc in cursor]

    async def update_vocab_word_stats(self, word_id: ObjectId, is_correct: bool) -> None:
        update = {
            "$inc": {
                "guesses": 1,
                "correct": 1 if is_correct else 0
            }
        }
        await self.db.vocab_words.update_one({"_id": word_id}, update)
