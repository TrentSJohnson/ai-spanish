from pydantic import BaseModel


class GradeRequest(BaseModel):
    sentence_id: str
    translation: str
