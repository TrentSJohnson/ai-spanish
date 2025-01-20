from typing import Optional, Annotated
from typing_extensions import Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from pydantic.json_schema import JsonSchemaValue


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class VocabWord(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    word: str
    guesses: int = 0
    correct: int = 0
