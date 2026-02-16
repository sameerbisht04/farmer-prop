from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# OTP-based authentication for phone numbers
def generate_otp() -> str:
    """Generate 6-digit OTP"""
    import random
    return str(random.randint(100000, 999999))


def verify_otp(provided_otp: str, stored_otp: str) -> bool:
    """Verify OTP"""
    return provided_otp == stored_otp


# Simple in-memory OTP storage (in production, use Redis)
otp_storage = {}


def store_otp(phone_number: str, otp: str):
    """Store OTP for phone number"""
    otp_storage[phone_number] = {
        "otp": otp,
        "timestamp": datetime.utcnow(),
        "attempts": 0
    }


def get_stored_otp(phone_number: str) -> Optional[dict]:
    """Get stored OTP for phone number"""
    return otp_storage.get(phone_number)


def increment_otp_attempts(phone_number: str):
    """Increment OTP verification attempts"""
    if phone_number in otp_storage:
        otp_storage[phone_number]["attempts"] += 1


def is_otp_expired(otp_data: dict) -> bool:
    """Check if OTP is expired (5 minutes)"""
    if not otp_data:
        return True
    
    expiry_time = otp_data["timestamp"] + timedelta(minutes=5)
    return datetime.utcnow() > expiry_time


def is_otp_max_attempts_reached(otp_data: dict) -> bool:
    """Check if maximum OTP attempts reached (3 attempts)"""
    if not otp_data:
        return True
    
    return otp_data["attempts"] >= 3
