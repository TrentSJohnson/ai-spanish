from typing import Tuple, List
import asyncio
from models.translation_grade import TranslationGrade, VocabWordGrade

from models.generated_sentence import GeneratedSentence
from models.guessed_translation import GuessedTranslation
from models.requests.grade_request import GradeRequest
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

        # Update last_seen for all words concurrently
        max_last_seen = await self.vocab_service.get_max_last_seen()
        new_last_seen = max_last_seen + 1
        await asyncio.gather(
            *[self.vocab_service.update_last_seen(word.id, new_last_seen) 
              for word in random_words]
        )

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

    async def grade_translation(self, check_request: GradeRequest) -> TranslationGrade:
        # Get the original sentence and guessed translation
        sentence = await self.sentence_service.get_generated_sentence(check_request.sentence_id)
        if not sentence:
            raise ValueError("Sentence not found")
        print(sentence.id,check_request.translation)
        translation = await self.translation_service.create_guessed_translation(
            GuessedTranslation(
                sentence=sentence.id,
                translation=check_request.translation
            )
        )

        # Get general feedback on the translation
        feedback = await self.ai_service.get_translation_feedback(
            sentence.sentence, 
            check_request.translation
        )

        # Get all vocab words concurrently
        words = await asyncio.gather(
            *[self.vocab_service.get_vocab_word(word_id) 
              for word_id in sentence.vocab_words]
        )
        
        # Check usage of all words concurrently
        word_results = await asyncio.gather(
            *[self.ai_service.check_vocab_usage(
                word.word,
                check_request.translation
            ) for word in words if word]
        )
        
        # Create grades from results
        vocab_word_grades = [
            VocabWordGrade(
                vocab_word=word_id,
                is_correct=is_correct,
                feedback=word_feedback
            )
            for (word_id, (is_correct, word_feedback)) 
            in zip(sentence.vocab_words, word_results)
        ]

        # Create and return the grade using the service
        grade = TranslationGrade(
            sentence=sentence.id,
            guessed_translation=translation.id,
            vocab_word_grades=vocab_word_grades,
            feedback=feedback
        )
        return await self.translation_service.create_translation_grade(grade)
