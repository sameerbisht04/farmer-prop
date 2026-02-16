import json
import asyncio
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.crop import Crop
from app.models.soil import SoilType
from app.models.weather import WeatherData
from app.services.weather_service import WeatherService
from app.services.crop_recommendation_service import CropRecommendationService


class ChatbotService:
    def __init__(self):
        self.weather_service = WeatherService()
        self.crop_service = CropRecommendationService()
        
        # Agricultural knowledge base
        self.knowledge_base = {
            "crop_selection": {
                "keywords": ["crop", "grow", "plant", "season", "soil"],
                "responses": {
                    "kharif": "Kharif crops like rice, maize, cotton are suitable for monsoon season (June-October)",
                    "rabi": "Rabi crops like wheat, barley, mustard are suitable for winter season (October-March)",
                    "zaid": "Zaid crops like cucumber, watermelon are suitable for summer season (March-June)"
                }
            },
            "pest_control": {
                "keywords": ["pest", "insect", "disease", "spray", "treatment"],
                "responses": {
                    "general": "For pest control, use integrated pest management. Identify the pest first, then use appropriate organic or chemical treatment."
                }
            },
            "fertilizer": {
                "keywords": ["fertilizer", "manure", "nutrient", "npk"],
                "responses": {
                    "general": "Use soil test results to determine fertilizer requirements. Organic manure improves soil health."
                }
            },
            "irrigation": {
                "keywords": ["water", "irrigation", "drip", "sprinkler"],
                "responses": {
                    "general": "Water requirements depend on crop type, soil, and weather. Drip irrigation is most efficient."
                }
            }
        }

    async def get_response(self, user_message: str, user_id: int, user_context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Generate AI response based on user message and context
        """
        try:
            # Analyze user intent
            intent = self._analyze_intent(user_message)
            
            # Get contextual information
            context_data = await self._get_contextual_data(user_context, db)
            
            # Generate response based on intent
            if intent == "crop_selection":
                response = await self._handle_crop_selection(user_message, context_data, db)
            elif intent == "pest_control":
                response = await self._handle_pest_control(user_message, context_data, db)
            elif intent == "fertilizer":
                response = await self._handle_fertilizer_advice(user_message, context_data, db)
            elif intent == "weather":
                response = await self._handle_weather_query(user_message, context_data, db)
            elif intent == "market":
                response = await self._handle_market_query(user_message, context_data, db)
            else:
                response = await self._handle_general_query(user_message, context_data, db)
            
            return response
            
        except Exception as e:
            return {
                "content": "मुझे क्षमा करें, मैं आपकी सहायता नहीं कर सकता। कृपया बाद में पुनः प्रयास करें।",
                "type": "error",
                "confidence": 0.0,
                "suggestions": ["सहायता के लिए हमारे विशेषज्ञ से संपर्क करें"]
            }

    def _analyze_intent(self, message: str) -> str:
        """
        Analyze user message to determine intent
        """
        message_lower = message.lower()
        
        # Check for crop selection intent
        if any(keyword in message_lower for keyword in ["crop", "grow", "plant", "season"]):
            return "crop_selection"
        
        # Check for pest control intent
        if any(keyword in message_lower for keyword in ["pest", "insect", "disease", "spray"]):
            return "pest_control"
        
        # Check for fertilizer intent
        if any(keyword in message_lower for keyword in ["fertilizer", "manure", "nutrient"]):
            return "fertilizer"
        
        # Check for weather intent
        if any(keyword in message_lower for keyword in ["weather", "rain", "temperature"]):
            return "weather"
        
        # Check for market intent
        if any(keyword in message_lower for keyword in ["price", "market", "sell"]):
            return "market"
        
        return "general"

    async def _get_contextual_data(self, user_context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Gather contextual data for better responses
        """
        context = {
            "location": user_context.get("location", ""),
            "farm_size": user_context.get("farm_size", 0),
            "primary_crops": user_context.get("primary_crops", ""),
            "language": user_context.get("language", "hi")
        }
        
        # Get weather data if location is available
        if context["location"]:
            try:
                weather_data = await self.weather_service.get_current_weather(context["location"])
                context["weather"] = weather_data
            except:
                context["weather"] = None
        
        # Get available crops from database
        crops = db.query(Crop).limit(10).all()
        context["available_crops"] = [crop.name for crop in crops]
        
        return context

    async def _handle_crop_selection(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle crop selection queries
        """
        try:
            # Get crop recommendations based on context
            recommendations = await self.crop_service.get_crop_recommendations(
                location=context.get("location", ""),
                season=self._get_current_season(),
                soil_type="loam",  # Default, should be from soil test
                farm_size=context.get("farm_size", 1),
                db=db
            )
            
            if recommendations:
                crop_names = [rec["crop_name"] for rec in recommendations[:3]]
                response_text = f"आपकी जमीन और मौसम के अनुसार, आप इन फसलों को उगा सकते हैं: {', '.join(crop_names)}।"
                suggestions = [f"{crop} के बारे में अधिक जानकारी" for crop in crop_names]
            else:
                response_text = "कृपया अपनी मिट्टी की जांच करवाएं और मौसम की जानकारी दें ताकि मैं बेहतर सुझाव दे सकूं।"
                suggestions = ["मिट्टी की जांच करवाएं", "मौसम की जानकारी देखें"]
            
            return {
                "content": response_text,
                "type": "crop_selection",
                "confidence": 0.8,
                "suggestions": suggestions
            }
            
        except Exception as e:
            return {
                "content": "फसल चयन में सहायता के लिए कृपया अपनी जमीन की जानकारी दें।",
                "type": "crop_selection",
                "confidence": 0.5,
                "suggestions": ["मिट्टी की जांच करवाएं"]
            }

    async def _handle_pest_control(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle pest control queries
        """
        response_text = "कीट नियंत्रण के लिए पहले कीट की पहचान करें। फिर उपयुक्त जैविक या रासायनिक उपचार का उपयोग करें।"
        
        return {
            "content": response_text,
            "type": "pest_control",
            "confidence": 0.7,
            "suggestions": ["कीट की तस्वीर भेजें", "रोग की पहचान करें"]
        }

    async def _handle_fertilizer_advice(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle fertilizer advice queries
        """
        response_text = "उर्वरक की मात्रा मिट्टी की जांच के परिणामों पर निर्भर करती है। जैविक खाद मिट्टी की सेहत के लिए अच्छी होती है।"
        
        return {
            "content": response_text,
            "type": "fertilizer",
            "confidence": 0.8,
            "suggestions": ["मिट्टी की जांच करवाएं", "जैविक खाद के बारे में जानें"]
        }

    async def _handle_weather_query(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle weather-related queries
        """
        weather_data = context.get("weather")
        if weather_data:
            response_text = f"आज का मौसम: तापमान {weather_data.get('temperature', 'N/A')}°C, आर्द्रता {weather_data.get('humidity', 'N/A')}%।"
        else:
            response_text = "मौसम की जानकारी उपलब्ध नहीं है। कृपया अपना स्थान अपडेट करें।"
        
        return {
            "content": response_text,
            "type": "weather",
            "confidence": 0.9 if weather_data else 0.3,
            "suggestions": ["स्थान अपडेट करें", "मौसम पूर्वानुमान देखें"]
        }

    async def _handle_market_query(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle market price queries
        """
        response_text = "बाजार की कीमतों के लिए कृपया मार्केट सेक्शन देखें। वहां आपको नवीनतम कीमतें मिलेंगी।"
        
        return {
            "content": response_text,
            "type": "market",
            "confidence": 0.6,
            "suggestions": ["मार्केट सेक्शन देखें", "कीमत अलर्ट सेट करें"]
        }

    async def _handle_general_query(self, message: str, context: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Handle general agricultural queries
        """
        response_text = "मैं आपकी कृषि संबंधी सहायता कर सकता हूं। आप फसल चयन, कीट नियंत्रण, उर्वरक या मौसम के बारे में पूछ सकते हैं।"
        
        return {
            "content": response_text,
            "type": "general",
            "confidence": 0.7,
            "suggestions": ["फसल चयन", "कीट नियंत्रण", "उर्वरक सलाह"]
        }

    def _get_current_season(self) -> str:
        """
        Determine current agricultural season
        """
        import datetime
        month = datetime.datetime.now().month
        
        if month in [6, 7, 8, 9, 10]:
            return "kharif"
        elif month in [11, 12, 1, 2, 3]:
            return "rabi"
        else:
            return "zaid"
