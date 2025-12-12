from typing import Any
from infrastructure.translate_provider import TranslateProvider

class TranslationService:
    def __init__(self, provider: TranslateProvider):
        self.provider = provider

    def translate_content(self, content: Any, target_lang: str) -> Any:
        """
        Recursively translates the content.
        """
        if isinstance(content, str):
            return self.provider.translate_text(content, target_lang)
        
        if isinstance(content, list):
            return [self.translate_content(item, target_lang) for item in content]
        
        if isinstance(content, dict):
            return {
                key: self.translate_content(value, target_lang)
                for key, value in content.items()
            }
        
        # Return as is for numbers, booleans, None, etc.
        return content
