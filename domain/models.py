from dataclasses import dataclass
from typing import Any

@dataclass
class TranslationRequest:
    content: Any
    target_language: str
