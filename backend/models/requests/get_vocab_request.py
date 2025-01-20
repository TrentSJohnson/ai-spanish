from pydantic import BaseModel, ConfigDict


class GetVocabRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    pass  # No parameters needed for now, but can be extended later
