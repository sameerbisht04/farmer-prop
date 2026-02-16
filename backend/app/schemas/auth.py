from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class PhoneNumberRequest(BaseModel):
    phone_number: str
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic phone number validation for Indian numbers
        if not v.startswith('+91') and not v.startswith('91') and not v.isdigit():
            raise ValueError('Invalid phone number format')
        
        # Remove country code if present
        if v.startswith('+91'):
            v = v[3:]
        elif v.startswith('91'):
            v = v[2:]
        
        # Check if it's a 10-digit number
        if len(v) != 10 or not v.isdigit():
            raise ValueError('Phone number must be 10 digits')
        
        return v


class OTPVerification(BaseModel):
    phone_number: str
    otp: str
    name: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    language: Optional[str] = "hi"
    
    @validator('otp')
    def validate_otp(cls, v):
        if len(v) != 6 or not v.isdigit():
            raise ValueError('OTP must be 6 digits')
        return v


class UserRegistration(BaseModel):
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
    preferred_language: str = "hi"
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic phone number validation for Indian numbers
        if not v.startswith('+91') and not v.startswith('91') and not v.isdigit():
            raise ValueError('Invalid phone number format')
        
        # Remove country code if present
        if v.startswith('+91'):
            v = v[3:]
        elif v.startswith('91'):
            v = v[2:]
        
        # Check if it's a 10-digit number
        if len(v) != 10 or not v.isdigit():
            raise ValueError('Phone number must be 10 digits')
        
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v


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


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserProfile


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
