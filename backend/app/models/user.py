from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    
    # Location Information
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    village = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Farm Information
    farm_size = Column(Float, nullable=True)  # in acres
    primary_crops = Column(Text, nullable=True)  # JSON string of crop names
    farming_experience = Column(Integer, nullable=True)  # years
    
    # Preferences
    preferred_language = Column(String(5), default="hi")  # en, hi, pa
    notification_preferences = Column(Text, nullable=True)  # JSON string
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    advisories = relationship("Advisory", back_populates="user")
    soil_tests = relationship("SoilTest", back_populates="user")
    community_posts = relationship("CommunityPost", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
