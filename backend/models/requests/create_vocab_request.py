from pydantic import BaseModel

class CreateVocabRequest(BaseModel):
    word: str
