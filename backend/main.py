from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict

app = FastAPI()

# Store generated sentences with their IDs
sentences_store: Dict[str, str] = {}

class SentenceResponse(BaseModel):
    id: str
    sentence: str

class CheckRequest(BaseModel):
    id: str
    sentence: str

@app.post("/api/v1/generate/sentence")
async def generate_sentence() -> SentenceResponse:
    # TODO: Replace with actual sentence generation logic
    generated_sentence = "This is a sample generated sentence."
    sentence_id = str(uuid.uuid4())
    sentences_store[sentence_id] = generated_sentence
    
    return SentenceResponse(
        id=sentence_id,
        sentence=generated_sentence
    )

@app.post("/api/v1/generate/check")
async def check_sentence(request: CheckRequest) -> dict:
    if request.id not in sentences_store:
        raise HTTPException(status_code=404, detail="Sentence ID not found")
    
    original_sentence = sentences_store[request.id]
    # TODO: Replace with actual checking logic
    is_correct = request.sentence.lower() == original_sentence.lower()
    
    return {
        "result": "Correct!" if is_correct else "Incorrect, try again!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
