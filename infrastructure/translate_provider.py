import boto3
from botocore.exceptions import ClientError

class TranslateProvider:
    def __init__(self):
        self.client = boto3.client('translate')

    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """
        Translates a single string using AWS Translate.
        Returns the translated text.
        """
        if not text or not text.strip():
            print("Text is empty or whitespace, skipping.")
            return text

        try:
            print(f"Translating text: '{text[:50]}...' to '{target_lang}' (Source: {source_lang})")
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang.lower()
            )
            translated_text = response.get('TranslatedText', text)
            print(f"Success. Result: '{translated_text[:50]}...'")
            return translated_text
        except ClientError as e:
            print(f"ERROR: AWS Translate failed for text '{text[:20]}...': {e}")
            # Fallback to original text in case of failure to avoid breaking the structure
            return text

