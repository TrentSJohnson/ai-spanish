from typing import Dict, Tuple
import uuid
from services.ai_service import AIService
from models.responses.sentence_response import SentenceResponse
from models.requests.check_request import CheckRequest

# Store generated sentences with their IDs
sentences_store: Dict[str, str] = {}

class GenerateController:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def generate_sentence(self) -> SentenceResponse:
        generated_sentence = await self.ai_service.generate_sentence()
        sentence_id = str(uuid.uuid4())
        sentences_store[sentence_id] = generated_sentence
        
        return SentenceResponse(
            id=sentence_id,
            sentence=generated_sentence
        )

    async def check_sentence(self, request: CheckRequest) -> Tuple[bool, str]:
        if request.id not in sentences_store:
            return False, "Sentence ID not found"
        
        original_sentence = sentences_store[request.id]
        is_correct, feedback = await self.ai_service.check_translation(
            original_sentence,
            request.sentence
        )
        
        return True, feedback
