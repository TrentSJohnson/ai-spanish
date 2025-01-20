import json
import os
import re
from pathlib import Path
from typing import Optional, List

from anthropic import AsyncAnthropic
from jinja2 import Environment, FileSystemLoader


class AIService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Can be configured as needed

        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "prompts"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

    async def generate_sentence(self, vocab_words: Optional[List[str]] = None) -> str:
        """Generate a sentence using OpenAI API, optionally using specific vocabulary words"""
        if vocab_words:
            template = self.jinja_env.get_template("sentence_with_vocab.j2")
            prompt = template.render(vocab_words=vocab_words)
            messages = [{"role": "user", "content": prompt}]
        else:
            template = self.jinja_env.get_template("sentence_with_vocab.j2")
            prompt = template.render(vocab_words=[])
            messages = [{"role": "user", "content": prompt}]

        response = await self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": messages[0]["content"]}],
            max_tokens=1024
        )
        content = response.content[0].text.strip()
        result = json.loads(re.search(r'{.*}', content, re.DOTALL).group(0))
        return result["sentence"]

    async def check_vocab_usage(self, word: str, sentence: str) -> tuple[bool, str]:
        """Check if a vocabulary word is properly used in the sentence"""
        template = self.jinja_env.get_template("check_vocab_usage.j2")
        prompt = template.render(word=word, sentence=sentence)
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        result = json.loads(re.search(r'{.*}', content, re.DOTALL).group(0))
        return result["is_correct"], result["feedback"]

    async def rewrite_spanish(self, sentence: str) -> str:
        """Rewrite a Spanish sentence to be grammatically correct"""
        template = self.jinja_env.get_template("rewrite_spanish.j2")
        prompt = template.render(sentence=sentence)
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        result = json.loads(re.search(r'{.*}', content, re.DOTALL).group(0))
        return result["corrected_sentence"]

    async def get_translation_feedback(self, original: str, translation: str) -> str:
        """Get general feedback about a translation attempt"""
        template = self.jinja_env.get_template("translation_feedback.j2")
        prompt = template.render(original=original, translation=translation)
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        result = json.loads(re.search(r'{.*}', content, re.DOTALL).group(0))
        return result["feedback"]
