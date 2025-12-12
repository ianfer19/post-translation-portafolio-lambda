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
            return text

        try:
            response = self.client.translate_text(
                Text=text,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang.lower()
            )
            return response.get('TranslatedText', text)
        except ClientError as e:
            print(f"Error translating text: {e}")
            # Fallback to original text in case of failure to avoid breaking the structure
            return text
