from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.models.user import User
from app.models.advisory import Advisory
from app.services.chatbot_service import ChatbotService
from app.services.translation_service import TranslationService
from app.schemas.chatbot import ChatMessage, ChatResponse, VoiceMessage
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    message: ChatMessage,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI advisory bot
    """
    try:
        chatbot_service = ChatbotService()
        translation_service = TranslationService()
        
        # Translate message to English if needed
        if message.language != "en":
            translated_message = await translation_service.translate_text(
                message.content, message.language, "en"
            )
        else:
            translated_message = message.content
        
        # Get AI response
        ai_response = await chatbot_service.get_response(
            user_message=translated_message,
            user_id=current_user.id,
            user_context={
                "location": f"{current_user.state}, {current_user.district}",
                "farm_size": current_user.farm_size,
                "primary_crops": current_user.primary_crops,
                "language": current_user.preferred_language
            },
            db=db
        )
        
        # Translate response back to user's language
        if message.language != "en":
            localized_response = await translation_service.translate_text(
                ai_response["content"], "en", message.language
            )
        else:
            localized_response = ai_response["content"]
        
        # Save advisory to database
        advisory = Advisory(
            user_id=current_user.id,
            title=ai_response.get("title", "Chat Response"),
            content=localized_response,
            advisory_type=ai_response.get("type", "general"),
            language=message.language,
            is_ai_generated=True,
            confidence_score=ai_response.get("confidence", 0.8)
        )
        
        background_tasks.add_task(save_advisory, advisory, db)
        
        return ChatResponse(
            message=localized_response,
            advisory_type=ai_response.get("type", "general"),
            confidence=ai_response.get("confidence", 0.8),
            suggestions=ai_response.get("suggestions", []),
            language=message.language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.post("/voice-chat", response_model=ChatResponse)
async def voice_chat(
    voice_message: VoiceMessage,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Voice-based chat with the AI advisory bot
    """
    try:
        chatbot_service = ChatbotService()
        translation_service = TranslationService()
        
        # Convert speech to text (this would integrate with speech recognition)
        # For now, we'll assume the text is already extracted
        user_message = voice_message.transcribed_text
        
        # Process the message similar to text chat
        if voice_message.language != "en":
            translated_message = await translation_service.translate_text(
                user_message, voice_message.language, "en"
            )
        else:
            translated_message = user_message
        
        # Get AI response
        ai_response = await chatbot_service.get_response(
            user_message=translated_message,
            user_id=current_user.id,
            user_context={
                "location": f"{current_user.state}, {current_user.district}",
                "farm_size": current_user.farm_size,
                "primary_crops": current_user.primary_crops,
                "language": current_user.preferred_language
            },
            db=db
        )
        
        # Translate response back to user's language
        if voice_message.language != "en":
            localized_response = await translation_service.translate_text(
                ai_response["content"], "en", voice_message.language
            )
        else:
            localized_response = ai_response["content"]
        
        # Save advisory
        advisory = Advisory(
            user_id=current_user.id,
            title=ai_response.get("title", "Voice Chat Response"),
            content=localized_response,
            advisory_type=ai_response.get("type", "general"),
            language=voice_message.language,
            is_ai_generated=True,
            confidence_score=ai_response.get("confidence", 0.8)
        )
        
        background_tasks.add_task(save_advisory, advisory, db)
        
        return ChatResponse(
            message=localized_response,
            advisory_type=ai_response.get("type", "general"),
            confidence=ai_response.get("confidence", 0.8),
            suggestions=ai_response.get("suggestions", []),
            language=voice_message.language,
            audio_response_url=ai_response.get("audio_url")  # For text-to-speech
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice chat error: {str(e)}")


@router.get("/chat-history")
async def get_chat_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's chat history
    """
    advisories = db.query(Advisory).filter(
        Advisory.user_id == current_user.id,
        Advisory.is_ai_generated == True
    ).order_by(Advisory.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "advisories": [
            {
                "id": advisory.id,
                "title": advisory.title,
                "content": advisory.content,
                "type": advisory.advisory_type,
                "created_at": advisory.created_at,
                "is_read": advisory.is_read
            }
            for advisory in advisories
        ],
        "total": len(advisories)
    }


async def save_advisory(advisory: Advisory, db: Session):
    """Background task to save advisory to database"""
    try:
        db.add(advisory)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving advisory: {e}")
