from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
from models.vocab_word import VocabWord
from models.generated_sentence import GeneratedSentence
from models.guessed_translation import GuessedTranslation
from models.translation_grade import TranslationGrade
import os

class DatabaseService:
    def __init__(self):
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "aispanish")
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[database_name]

    # VocabWord operations
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

    # GeneratedSentence operations
    async def create_generated_sentence(self, sentence: GeneratedSentence) -> GeneratedSentence:
        result = await self.db.generated_sentences.insert_one(sentence.dict(by_alias=True))
        return await self.get_generated_sentence(result.inserted_id)

    async def get_generated_sentence(self, sentence_id: ObjectId) -> Optional[GeneratedSentence]:
        sentence_dict = await self.db.generated_sentences.find_one({"_id": sentence_id})
        if sentence_dict:
            return GeneratedSentence(**sentence_dict)
        return None

    # GuessedTranslation operations
    async def create_guessed_translation(self, translation: GuessedTranslation) -> GuessedTranslation:
        result = await self.db.guessed_translations.insert_one(translation.dict(by_alias=True))
        return await self.get_guessed_translation(result.inserted_id)

    async def get_guessed_translation(self, translation_id: ObjectId) -> Optional[GuessedTranslation]:
        translation_dict = await self.db.guessed_translations.find_one({"_id": translation_id})
        if translation_dict:
            return GuessedTranslation(**translation_dict)
        return None

    # TranslationGrade operations
    async def create_translation_grade(self, grade: TranslationGrade) -> TranslationGrade:
        result = await self.db.translation_grades.insert_one(grade.dict(by_alias=True))
        return await self.get_translation_grade(result.inserted_id)

    async def get_translation_grade(self, grade_id: ObjectId) -> Optional[TranslationGrade]:
        grade_dict = await self.db.translation_grades.find_one({"_id": grade_id})
        if grade_dict:
            return TranslationGrade(**grade_dict)
        return None

    async def update_vocab_word_stats(self, word_id: ObjectId, is_correct: bool) -> None:
        update = {
            "$inc": {
                "guesses": 1,
                "correct": 1 if is_correct else 0
            }
        }
        await self.db.vocab_words.update_one({"_id": word_id}, update)
