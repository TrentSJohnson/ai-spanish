from typing import Tuple

from models.generated_sentence import GeneratedSentence
from models.guessed_translation import GuessedTranslation
from models.requests.check_request import CheckRequest
from models.responses.sentence_response import SentenceResponse
from services.ai_service import AIService
from services.sentence_service import SentenceService
from services.translation_service import TranslationService
from services.vocab_service import VocabService


class GenerateController:
    def __init__(
            self,
            ai_service: AIService,
            sentence_service: SentenceService,
            translation_service: TranslationService,
            vocab_service: VocabService
    ):
        self.ai_service = ai_service
        self.sentence_service = sentence_service
        self.translation_service = translation_service
        self.vocab_service = vocab_service

    async def generate_sentence(self) -> SentenceResponse:
        random_words = await self.vocab_service.get_random_vocab_words(2)
        vocab_word_ids = [str(word.id) for word in random_words]
        vocab_words = [word.word for word in random_words]

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
