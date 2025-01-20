from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from datetime import datetime
from bson import ObjectId
from .vocab_word import PyObjectId, VocabWord
from .generated_sentence import GeneratedSentence
from .guessed_translation import GuessedTranslation

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
