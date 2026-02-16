import asyncio
from typing import Dict, Any
from googletrans import Translator
import json


class TranslationService:
    def __init__(self):
        self.translator = Translator()
        self.language_codes = {
            "hi": "hindi",
            "en": "english", 
            "pa": "punjabi"
        }
        
        # Agricultural terminology dictionary for better translations
        self.agricultural_terms = {
            "crop": {
                "hi": "फसल",
                "pa": "ਫਸਲ",
                "en": "crop"
            },
            "fertilizer": {
                "hi": "उर्वरक",
                "pa": "ਖਾਦ",
                "en": "fertilizer"
            },
            "pest": {
                "hi": "कीट",
                "pa": "ਕੀਟ",
                "en": "pest"
            },
            "irrigation": {
                "hi": "सिंचाई",
                "pa": "ਸਿੰਚਾਈ",
                "en": "irrigation"
            },
            "soil": {
                "hi": "मिट्टी",
                "pa": "ਮਿੱਟੀ",
                "en": "soil"
            },
            "weather": {
                "hi": "मौसम",
                "pa": "ਮੌਸਮ",
                "en": "weather"
            },
            "harvest": {
                "hi": "फसल कटाई",
                "pa": "ਫਸਲ ਕਟਾਈ",
                "en": "harvest"
            }
        }

    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source language to target language
        """
        try:
            if source_lang == target_lang:
                return text
            
            # Use Google Translate for general translation
            result = self.translator.translate(
                text, 
                src=source_lang, 
                dest=target_lang
            )
            
            # Post-process for agricultural terms
            translated_text = self._post_process_agricultural_terms(
                result.text, target_lang
            )
            
            return translated_text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails

    def _post_process_agricultural_terms(self, text: str, target_lang: str) -> str:
        """
        Post-process translated text to ensure agricultural terms are correctly translated
        """
        try:
            for term, translations in self.agricultural_terms.items():
                if target_lang in translations:
                    # Replace common mistranslations with correct agricultural terms
                    if term in text.lower() and translations[target_lang] not in text:
                        text = text.replace(term, translations[target_lang])
            
            return text
        except Exception as e:
            print(f"Post-processing error: {e}")
            return text

    async def translate_batch(self, texts: list, source_lang: str, target_lang: str) -> list:
        """
        Translate multiple texts in batch
        """
        try:
            if source_lang == target_lang:
                return texts
            
            results = []
            for text in texts:
                translated = await self.translate_text(text, source_lang, target_lang)
                results.append(translated)
            
            return results
            
        except Exception as e:
            print(f"Batch translation error: {e}")
            return texts

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        """
        return self.language_codes

    async def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        """
        try:
            result = self.translator.detect(text)
            return result.lang
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"  # Default to English

    def get_agricultural_terms(self, language: str) -> Dict[str, str]:
        """
        Get agricultural terms for a specific language
        """
        terms = {}
        for term, translations in self.agricultural_terms.items():
            if language in translations:
                terms[term] = translations[language]
        return terms
