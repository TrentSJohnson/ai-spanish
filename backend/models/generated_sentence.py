from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

from .vocab_word import PyObjectId


class GeneratedSentence(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    vocab_words: List[PyObjectId]
    sentence: str

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True
