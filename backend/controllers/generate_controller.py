from typing import Tuple
from services.ai_service import AIService
from services.sentence_service import SentenceService
from services.translation_service import TranslationService
from models.responses.sentence_response import SentenceResponse
from models.requests.check_request import CheckRequest
from models.generated_sentence import GeneratedSentence
from models.guessed_translation import GuessedTranslation

class GenerateController:
    def __init__(
        self,
        ai_service: AIService,
        sentence_service: SentenceService,
        translation_service: TranslationService
    ):
        self.ai_service = ai_service
        self.sentence_service = sentence_service
        self.translation_service = translation_service

    async def generate_sentence(self, vocab_word_ids: list[str] = None) -> SentenceResponse:
        vocab_words = []
        if vocab_word_ids:
            # Fetch actual vocab words from IDs
            for word_id in vocab_word_ids:
                word = await self.vocab_service.get_vocab_word(ObjectId(word_id))
                if word:
                    vocab_words.append(word.word)
        
        sentence_text = await self.ai_service.generate_sentence(vocab_words)
        generated_sentence = await self.sentence_service.create_generated_sentence(
            GeneratedSentence(
                vocab_words=vocab_word_ids or [],
                sentence=sentence_text
            )
        )
        
        return SentenceResponse(
            id=str(generated_sentence.id),
            sentence=generated_sentence.sentence
        )

    async def check_sentence(self, request: CheckRequest) -> Tuple[bool, str]:
        generated_sentence = await self.sentence_service.get_generated_sentence(request.id)
        if not generated_sentence:
            return False, "Sentence ID not found"
        
        # Store the guessed translation
        guessed_translation = await self.translation_service.create_guessed_translation(
            GuessedTranslation(
                generated_sentence=generated_sentence.id,
                guess=request.sentence
            )
        )
        
        is_correct, feedback = await self.ai_service.check_translation(
            generated_sentence.sentence,
            request.sentence
        )
        
        return True, feedback
