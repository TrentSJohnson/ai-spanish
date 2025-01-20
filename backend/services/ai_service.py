from typing import Optional, List
import os
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
                messages = [
                    {"role": "system", "content": "You are a language learning assistant. Generate a simple sentence in English."},
                    {"role": "user", "content": "Generate a simple English sentence for language practice."}
                ]
                
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Log the error in production
            print(f"Error generating sentence: {str(e)}")
            return "An error occurred while generating the sentence."

    async def check_translation(self, original: str, translation: str) -> tuple[bool, str]:
        """Check if the translation is correct using OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a language learning assistant. Compare the original sentence with the translation and provide feedback."},
                    {"role": "user", "content": f"Original: {original}\nTranslation: {translation}\nAre these equivalent? Respond with 'True' or 'False' followed by a brief explanation."}
                ]
            )
            result = response.choices[0].message.content.strip()
            is_correct = result.lower().startswith("true")
            feedback = result.split("\n")[0] if "\n" in result else result
            return is_correct, feedback
        except Exception as e:
            # Log the error in production
            print(f"Error checking translation: {str(e)}")
            return False, "An error occurred while checking the translation."
