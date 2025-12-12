import json
from utils import response
from application.translation_service import TranslationService
from infrastructure.translate_provider import TranslateProvider

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    print("1. Parsing Request Body")
    try:
        # 1. Parse Input
        body = event.get('body')
        if not body:
             print("ERROR: Missing request body")
             return response.error("Missing request body")
        
        if isinstance(body, str):
            print("Body is string, parsing JSON...")
            body = json.loads(body)

        print(f"Parsed Body: {json.dumps(body)}")

        content = body.get('content')
        target_language = body.get('targetLanguage')

        if not content:
            print("ERROR: Missing 'content' field")
            return response.error("Missing 'content' field in body")
        
        if not target_language:
            print("ERROR: Missing 'targetLanguage' field")
            return response.error("Missing 'targetLanguage' field in body")

        print(f"Target Language: {target_language}")
        print(f"Content Structure Type: {type(content)}")


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
            print(f"Target is ES, skipping translation. Returning original content.")
            return response.success(content)

        print("Starting translation service...")
        translated_content = service.translate_content(content, target_language)
        print("Translation complete.")


        # 4. Return Success
        return response.success(translated_content)

    except Exception as e:
        print(f"Error processing translation: {str(e)}")
        return response.error(f"Internal processing error: {str(e)}", 500)
