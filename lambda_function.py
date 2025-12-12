import json
from utils import response
from application.translation_service import TranslationService
from infrastructure.translate_provider import TranslateProvider

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    try:
        # 1. Parse Input
        body = event.get('body')
        if not body:
             return response.error("Missing request body")
        
        if isinstance(body, str):
            body = json.loads(body)

        content = body.get('content')
        target_language = body.get('targetLanguage')

        if not content:
            return response.error("Missing 'content' field in body")
        
        if not target_language:
            return response.error("Missing 'targetLanguage' field in body")

        # 2. Initialize Service
        # Note: In a real heavy-load scenario, we might want to cache the provider outside the handler
        provider = TranslateProvider()
        service = TranslationService(provider)

        # 3. Perform Translation
        # If target is Spanish, we might just return original as per user snippets, 
        # but let's assume the frontend might handle that or we can do it here too.
        # The user's snippet showed: if (targetLang === 'ES') return of(sectionContent);
        # So sticking to that logic:
        if target_language.upper() == 'ES':
            return response.success(content)

        translated_content = service.translate_content(content, target_language)

        # 4. Return Success
        return response.success(translated_content)

    except Exception as e:
        print(f"Error processing translation: {str(e)}")
        return response.error(f"Internal processing error: {str(e)}", 500)
