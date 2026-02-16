from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatMessage(BaseModel):
    content: str
    language: str = "hi"  # en, hi, pa
    message_type: str = "text"  # text, voice, image


class VoiceMessage(BaseModel):
    audio_data: Optional[str] = None  # Base64 encoded audio
    transcribed_text: str
    language: str = "hi"
    audio_format: str = "wav"


class ChatResponse(BaseModel):
    message: str
    advisory_type: str
    confidence: float
    suggestions: List[str] = []
    language: str
    audio_response_url: Optional[str] = None
    timestamp: datetime = datetime.now()


class ChatHistory(BaseModel):
    id: int
    title: str
    content: str
    type: str
    created_at: datetime
    is_read: bool
