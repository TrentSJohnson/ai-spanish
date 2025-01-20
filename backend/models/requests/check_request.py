from pydantic import BaseModel


class CheckRequest(BaseModel):
    id: str
    sentence: str
