from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class UserProfile(BaseModel):
    id: int
    phone_number: str
    name: str
    email: Optional[str] = None
    state: str
    district: str
    village: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    farm_size: Optional[float] = None
    primary_crops: Optional[str] = None
    farming_experience: Optional[int] = None
    preferred_language: str
    is_verified: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    farm_size: Optional[float] = None
    primary_crops: Optional[str] = None
    farming_experience: Optional[int] = None
    preferred_language: Optional[str] = None
    notification_preferences: Optional[dict] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('preferred_language')
    def validate_language(cls, v):
        if v and v not in ['hi', 'en', 'pa']:
            raise ValueError('Invalid language code')
        return v
