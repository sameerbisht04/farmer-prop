from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    language: str = "hi"


class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    language: str


# AI Response Generator
def generate_ai_response(user_message: str, language: str) -> str:
    """Generate AI response based on user message and language"""
    message = user_message.lower()
    
    # Hindi responses
    if language == "hi":
        if any(word in message for word in ["सिंचाई", "irrigation", "पानी"]):
            return "सिंचाई के लिए सुबह या शाम का समय सबसे अच्छा है। अपनी फसल के अनुसार पानी दें - गेहूं को सप्ताह में 2-3 बार, चावल को रोजाना पानी चाहिए।"
        if any(word in message for word in ["कीट", "pest", "बीमारी"]):
            return "कीट नियंत्रण के लिए नीम का तेल या जैविक कीटनाशक का उपयोग करें। नियमित रूप से पत्तियों की जांच करें और संक्रमित पौधों को तुरंत हटा दें।"
        if any(word in message for word in ["खाद", "fertilizer", "उर्वरक"]):
            return "खाद डालने का सही समय बुवाई के 15-20 दिन बाद है। NPK अनुपात 20:20:20 का उपयोग करें। मिट्टी की जांच के बाद ही खाद डालें।"
        if any(word in message for word in ["मौसम", "weather", "बारिश"]):
            return "आज का मौसम अच्छा है। तापमान 28°C है। अगले 2 दिनों में बारिश की संभावना है, इसलिए अपनी फसल की सुरक्षा करें।"
        if any(word in message for word in ["फसल", "crop", "बीज"]):
            return "सही फसल चुनने के लिए मिट्टी की जांच कराएं। रबी सीजन में गेहूं, सरसों, चना उगा सकते हैं। खरीफ सीजन में चावल, मक्का, कपास अच्छे विकल्प हैं।"
        if any(word in message for word in ["नमस्ते", "hello", "hi"]):
            return "नमस्ते! मैं आपका AI कृषि सलाहकार हूं। मैं आपकी फसल, कीट नियंत्रण, सिंचाई, खाद और मौसम के बारे में सलाह दे सकता हूं। आप क्या जानना चाहते हैं?"
        return "मैं आपकी मदद करने के लिए यहां हूं। कृपया अपनी समस्या या सवाल विस्तार से बताएं। मैं आपको सबसे अच्छी सलाह दूंगा।"
    
    # English responses
    if language == "en":
        if any(word in message for word in ["irrigation", "water", "watering"]):
            return "For irrigation, early morning or evening is the best time. Water according to your crop - wheat needs water 2-3 times a week, rice needs daily watering."
        if any(word in message for word in ["pest", "disease", "insect"]):
            return "For pest control, use neem oil or organic pesticides. Regularly check leaves and remove infected plants immediately."
        if any(word in message for word in ["fertilizer", "manure", "nutrient"]):
            return "The right time to apply fertilizer is 15-20 days after sowing. Use NPK ratio 20:20:20. Apply fertilizer only after soil testing."
        if any(word in message for word in ["weather", "rain", "temperature"]):
            return "Today's weather is good. Temperature is 28°C. There is a chance of rain in the next 2 days, so protect your crops."
        if any(word in message for word in ["crop", "seed", "planting"]):
            return "For choosing the right crop, get your soil tested. In Rabi season, you can grow wheat, mustard, gram. In Kharif season, rice, maize, cotton are good options."
        if any(word in message for word in ["hello", "hi", "namaste"]):
            return "Hello! I am your AI agriculture advisor. I can help you with crop advice, pest control, irrigation, fertilizer, and weather information. What would you like to know?"
        return "I am here to help you. Please describe your problem or question in detail. I will give you the best advice."
    
    # Punjabi responses
    if language == "pa":
        if any(word in message for word in ["ਸਿੰਚਾਈ", "ਪਾਣੀ"]):
            return "ਸਿੰਚਾਈ ਲਈ ਸਵੇਰ ਜਾਂ ਸ਼ਾਮ ਦਾ ਸਮਾਂ ਸਭ ਤੋਂ ਵਧੀਆ ਹੈ। ਆਪਣੀ ਫਸਲ ਦੇ ਅਨੁਸਾਰ ਪਾਣੀ ਦਿਓ - ਕਣਕ ਨੂੰ ਹਫ਼ਤੇ ਵਿੱਚ 2-3 ਵਾਰ, ਚੌਲਾਂ ਨੂੰ ਰੋਜ਼ਾਨਾ ਪਾਣੀ ਚਾਹੀਦਾ ਹੈ।"
        if any(word in message for word in ["ਕੀਟ", "ਰੋਗ"]):
            return "ਕੀਟ ਨਿਯੰਤਰਣ ਲਈ ਨੀਮ ਦਾ ਤੇਲ ਜਾਂ ਜੈਵਿਕ ਕੀਟਨਾਸ਼ਕ ਦਾ ਉਪਯੋਗ ਕਰੋ। ਨਿਯਮਿਤ ਤੌਰ 'ਤੇ ਪੱਤਿਆਂ ਦੀ ਜਾਂਚ ਕਰੋ ਅਤੇ ਸੰਕਰਮਿਤ ਪੌਦਿਆਂ ਨੂੰ ਤੁਰੰਤ ਹਟਾ ਦਿਓ।"
        if any(word in message for word in ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "hello", "hi"]):
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ AI ਖੇਤੀ ਸਲਾਹਕਾਰ ਹਾਂ। ਮੈਂ ਤੁਹਾਡੀ ਫਸਲ, ਕੀਟ ਨਿਯੰਤਰਣ, ਸਿੰਚਾਈ, ਖਾਦ ਅਤੇ ਮੌਸਮ ਬਾਰੇ ਸਲਾਹ ਦੇ ਸਕਦਾ ਹਾਂ। ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?"
        return "ਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰਨ ਲਈ ਇੱਥੇ ਹਾਂ। ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਸਮਸਿਆ ਜਾਂ ਸਵਾਲ ਵਿਸਤਾਰ ਨਾਲ ਦੱਸੋ। ਮੈਂ ਤੁਹਾਨੂੰ ਸਭ ਤੋਂ ਵਧੀਆ ਸਲਾਹ ਦਵਾਂਗਾ।"
    
    return "I am here to help you. Please describe your problem or question in detail."


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(message: ChatMessage):
    """
    Chat with the AI crop advisor bot - No authentication required for demo
    """
    try:
        response_text = generate_ai_response(message.message, message.language)
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.utcnow(),
            language=message.language
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/quick-questions")
async def get_quick_questions(language: str = "hi"):
    """
    Get quick questions based on language - No authentication required for demo
    """
    try:
        questions = {
            "hi": [
                "सिंचाई कब करें?",
                "कीट नियंत्रण कैसे करें?",
                "खाद कब डालें?",
                "मौसम कैसा है?",
                "फसल कैसे चुनें?",
                "नमस्ते"
            ],
            "en": [
                "When to irrigate?",
                "How to control pests?",
                "When to apply fertilizer?",
                "What is the weather?",
                "How to choose crops?",
                "Hello"
            ],
            "pa": [
                "ਸਿੰਚਾਈ ਕਦੋਂ ਕਰੀਏ?",
                "ਕੀਟ ਨਿਯੰਤਰਣ ਕਿਵੇਂ ਕਰੀਏ?",
                "ਖਾਦ ਕਦੋਂ ਪਾਈਏ?",
                "ਮੌਸਮ ਕਿਵੇਂ ਹੈ?",
                "ਫਸਲ ਕਿਵੇਂ ਚੁਣੀਏ?",
                "ਸਤ ਸ੍ਰੀ ਅਕਾਲ"
            ]
        }
        
        return {
            "questions": questions.get(language, questions["hi"]),
            "language": language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quick questions: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Chatbot",
        "timestamp": datetime.utcnow()
    }
