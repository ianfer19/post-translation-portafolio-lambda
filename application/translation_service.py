from typing import Any
from infrastructure.translate_provider import TranslateProvider

class TranslationService:
    def __init__(self, provider: TranslateProvider):
        self.provider = provider

    def translate_content(self, content: Any, target_lang: str) -> Any:
        """
        Recursively translates the content.
        """
        # print(f"Processing content of type: {type(content)}") # Optional: too noisy for deep recursion?

        if isinstance(content, str):
            return self.provider.translate_text(content, target_lang)
        
        if isinstance(content, list):
            # print(f"Recursing into list of length {len(content)}")
            return [self.translate_content(item, target_lang) for item in content]
        
        if isinstance(content, dict):
            # print(f"Recursing into dict with keys: {list(content.keys())}")
            return {
                key: self.translate_content(value, target_lang)
                for key, value in content.items()
            }
        
        # Return as is for numbers, booleans, None, etc.
        # print(f"Skipping translation for type {type(content)}: {content}")
        return content

