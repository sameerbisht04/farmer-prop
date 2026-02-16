from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta, datetime

from app.core.database import get_db
from app.core.auth import (
    create_access_token, 
    generate_otp, 
    store_otp, 
    get_stored_otp,
    verify_otp,
    increment_otp_attempts,
    is_otp_expired,
    is_otp_max_attempts_reached,
    get_password_hash,
    verify_password
)
from app.models.user import User
from app.schemas.auth import (
    PhoneNumberRequest, 
    OTPVerification, 
    UserRegistration, 
    LoginResponse,
    UserProfile
)
from app.services.notification_service import NotificationService
from app.core.config import settings

router = APIRouter()


@router.post("/send-otp")
async def send_otp(
    request: PhoneNumberRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send OTP to phone number for authentication
    """
    try:
        # Check if user already exists
        user = db.query(User).filter(User.phone_number == request.phone_number).first()
        
        # Generate OTP
        otp = generate_otp()
        
        # Store OTP
        store_otp(request.phone_number, otp)
        
        # Send OTP via SMS (background task)
        notification_service = NotificationService()
        background_tasks.add_task(
            notification_service.send_sms_otp,
            request.phone_number,
            otp
        )
        
        return {
            "message": "OTP sent successfully",
            "phone_number": request.phone_number,
            "user_exists": user is not None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send OTP: {str(e)}"
        )


@router.post("/verify-otp", response_model=LoginResponse)
async def verify_otp_and_login(
    request: OTPVerification,
    db: Session = Depends(get_db)
):
    """
    Verify OTP and login user
    """
    try:
        # Get stored OTP
        stored_otp_data = get_stored_otp(request.phone_number)
        
        if not stored_otp_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP not found. Please request a new OTP."
            )
        
        # Check if OTP is expired
        if is_otp_expired(stored_otp_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP expired. Please request a new OTP."
            )
        
        # Check if max attempts reached
        if is_otp_max_attempts_reached(stored_otp_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum OTP attempts reached. Please request a new OTP."
            )
        
        # Verify OTP
        if not verify_otp(request.otp, stored_otp_data["otp"]):
            increment_otp_attempts(request.phone_number)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        # Get or create user
        user = db.query(User).filter(User.phone_number == request.phone_number).first()
        
        if not user:
            # Create new user with minimal information
            user = User(
                phone_number=request.phone_number,
                name=request.name or "User",
                state=request.state or "",
                district=request.district or "",
                preferred_language=request.language or "hi"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserProfile(
                id=user.id,
                phone_number=user.phone_number,
                name=user.name,
                state=user.state,
                district=user.district,
                preferred_language=user.preferred_language,
                is_verified=user.is_verified
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/register", response_model=LoginResponse)
async def register_user(
    request: UserRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new user with complete profile
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.phone_number == request.phone_number).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this phone number"
            )
        
        # Create new user
        user = User(
            phone_number=request.phone_number,
            name=request.name,
            email=request.email,
            state=request.state,
            district=request.district,
            village=request.village,
            pincode=request.pincode,
            latitude=request.latitude,
            longitude=request.longitude,
            farm_size=request.farm_size,
            primary_crops=request.primary_crops,
            farming_experience=request.farming_experience,
            preferred_language=request.preferred_language,
            is_verified=True  # Auto-verify for now
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserProfile(
                id=user.id,
                phone_number=user.phone_number,
                name=user.name,
                state=user.state,
                district=user.district,
                preferred_language=user.preferred_language,
                is_verified=user.is_verified
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/refresh-token")
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresh access token
    """
    try:
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(current_user.id)}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user (client-side token removal)
    """
    return {"message": "Logged out successfully"}


