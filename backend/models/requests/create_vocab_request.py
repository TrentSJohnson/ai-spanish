from pydantic import BaseModel, ConfigDict


class CreateVocabRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    word: str
