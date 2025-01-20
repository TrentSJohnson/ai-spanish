from typing import Optional, List
import os
import json
import openai
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Can be configured as needed
        
        # Setup Jinja2 environment
        template_dir = Path(__file__).parent / "prompts"
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

    async def generate_sentence(self, vocab_words: Optional[List[str]] = None) -> str:
        """Generate a sentence using OpenAI API, optionally using specific vocabulary words"""
        try:
            if vocab_words:
                template = self.jinja_env.get_template("sentence_with_vocab.j2")
                prompt = template.render(vocab_words=vocab_words)
                messages = [{"role": "user", "content": prompt}]
            else:
                template = self.jinja_env.get_template("sentence_with_vocab.j2")
                prompt = template.render(vocab_words=[])
                messages = [{"role": "user", "content": prompt}]
                
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            return result["sentence"]
        except Exception as e:
            # Log the error in production
            print(f"Error generating sentence: {str(e)}")
            return "An error occurred while generating the sentence."

    async def check_translation(self, original: str, translation: str) -> tuple[bool, str]:
        """Check if the translation is correct using OpenAI API"""
        try:
            template = self.jinja_env.get_template("check_translation.j2")
            prompt = template.render(original=original, translation=translation)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            return result["is_correct"], result["feedback"]
        except Exception as e:
            # Log the error in production
            print(f"Error checking translation: {str(e)}")
            return False, "An error occurred while checking the translation."

    async def check_vocab_usage(self, word: str, sentence: str) -> tuple[bool, str]:
        """Check if a vocabulary word is properly used in the sentence"""
        try:
            template = self.jinja_env.get_template("check_vocab_usage.j2")
            prompt = template.render(word=word, sentence=sentence)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            return result["is_correct"], result["feedback"]
        except Exception as e:
            # Log the error in production
            print(f"Error checking vocab usage: {str(e)}")
            return False, "An error occurred while checking the vocabulary usage."

    async def rewrite_spanish(self, sentence: str) -> str:
        """Rewrite a Spanish sentence to be grammatically correct"""
        try:
            template = self.jinja_env.get_template("rewrite_spanish.j2")
            prompt = template.render(sentence=sentence)
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            result = json.loads(content)
            return result["corrected_sentence"]
        except Exception as e:
            # Log the error in production
            print(f"Error rewriting sentence: {str(e)}")
            return "An error occurred while rewriting the sentence."
