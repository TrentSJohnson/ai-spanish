from typing import Optional
from bson import ObjectId
from models.guessed_translation import GuessedTranslation
from models.translation_grade import TranslationGrade
from services.db_service import BaseDBService

class TranslationService(BaseDBService):
    async def create_guessed_translation(self, translation: GuessedTranslation) -> GuessedTranslation:
        result = await self.db.guessed_translations.insert_one(translation.model_dump(by_alias=True))
        return await self.get_guessed_translation(result.inserted_id)

    async def get_guessed_translation(self, translation_id: ObjectId) -> Optional[GuessedTranslation]:
        translation_dict = await self.db.guessed_translations.find_one({"_id": translation_id})
        if translation_dict:
            return GuessedTranslation(**translation_dict)
        return None

    async def create_translation_grade(self, grade: TranslationGrade) -> TranslationGrade:
        result = await self.db.translation_grades.insert_one(grade.model_dump(by_alias=True))
        return await self.get_translation_grade(result.inserted_id)

    async def get_translation_grade(self, grade_id: ObjectId) -> Optional[TranslationGrade]:
        grade_dict = await self.db.translation_grades.find_one({"_id": grade_id})
        if grade_dict:
            return TranslationGrade(**grade_dict)
        return None
