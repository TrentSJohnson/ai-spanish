from pydantic import BaseModel


class SentenceResponse(BaseModel):
    id: str
    sentence: str
