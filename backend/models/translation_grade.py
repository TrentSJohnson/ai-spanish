from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

from .vocab_word import PyObjectId


class VocabWordGrade(BaseModel):
    vocab_word: PyObjectId
    is_correct: bool

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class TranslationGrade(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sentence: PyObjectId
    guessed_translation: PyObjectId
    vocab_word_grades: List[VocabWordGrade]
    feedback: str

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True
