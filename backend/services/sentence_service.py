from typing import Optional

from bson import ObjectId

from models.generated_sentence import GeneratedSentence
from services.db_service import BaseDBService


class SentenceService(BaseDBService):
    async def create_generated_sentence(self, sentence: GeneratedSentence) -> GeneratedSentence:
        result = await self.db.generated_sentences.insert_one(sentence.model_dump(by_alias=True, exclude_none=True))
        return await self.get_generated_sentence(result.inserted_id)

    async def get_generated_sentence(self, sentence_id: ObjectId) -> Optional[GeneratedSentence]:
        sentence_dict = await self.db.generated_sentences.find_one({"_id": sentence_id})
        if sentence_dict:
            return GeneratedSentence(**sentence_dict)
        return None
