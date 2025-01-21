from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from models.vocab_word import PyObjectId


class GuessedTranslation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sentence: PyObjectId
    translation: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }
        populate_by_name = True
        arbitrary_types_allowed = True
