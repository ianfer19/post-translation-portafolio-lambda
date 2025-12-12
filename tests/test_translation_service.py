import unittest
from unittest.mock import MagicMock
from application.translation_service import TranslationService
from infrastructure.translate_provider import TranslateProvider

class TestTranslationService(unittest.TestCase):
    def setUp(self):
        self.mock_provider = MagicMock(spec=TranslateProvider)
        self.service = TranslationService(self.mock_provider)

    def test_translate_string(self):
        self.mock_provider.translate_text.return_value = "Hola"
        result = self.service.translate_content("Hello", "es")
        self.assertEqual(result, "Hola")
        self.mock_provider.translate_text.assert_called_with("Hello", "es")

    def test_translate_list_of_strings(self):
        self.mock_provider.translate_text.side_effect = lambda t, l: f"TR-{t}"
        data = ["One", "Two"]
        result = self.service.translate_content(data, "fr")
        self.assertEqual(result, ["TR-One", "TR-Two"])

    def test_translate_dict(self):
        self.mock_provider.translate_text.side_effect = lambda t, l: f"Translated-{t}"
        data = {"title": "Hello", "count": 10}
        result = self.service.translate_content(data, "de")
        
        # "count" is number, should remain number
        self.assertEqual(result["count"], 10)
        # "title" is string, should be translated
        self.assertEqual(result["title"], "Translated-Hello")

    def test_nested_structure(self):
        self.mock_provider.translate_text.side_effect = lambda t, l: f"T({t})"
        data = {
            "header": "Welcome",
            "items": [
                {"name": "Item 1", "active": True},
                {"name": "Item 2", "active": False}
            ]
        }
        result = self.service.translate_content(data, "pt")
        
        self.assertEqual(result["header"], "T(Welcome)")
        self.assertEqual(result["items"][0]["name"], "T(Item 1)")
        self.assertEqual(result["items"][0]["active"], True)
        self.assertEqual(result["items"][1]["name"], "T(Item 2)")

if __name__ == '__main__':
    unittest.main()
