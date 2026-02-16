from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    scientific_name = Column(String(100), nullable=True)
    local_name_hindi = Column(String(100), nullable=True)
    local_name_punjabi = Column(String(100), nullable=True)
    
    # Crop Characteristics
    crop_type = Column(String(50), nullable=False)  # cereal, vegetable, fruit, etc.
    season = Column(String(20), nullable=False)  # kharif, rabi, zaid
    duration_days = Column(Integer, nullable=True)  # days to harvest
    
    # Growing Requirements
    min_temperature = Column(Float, nullable=True)
    max_temperature = Column(Float, nullable=True)
    optimal_rainfall = Column(Float, nullable=True)
    soil_types = Column(Text, nullable=True)  # JSON string of suitable soil types
    
    # Yield Information
    average_yield_per_acre = Column(Float, nullable=True)
    market_price_range = Column(Text, nullable=True)  # JSON string with min/max prices
    
    # Care Information
    water_requirements = Column(Text, nullable=True)
    fertilizer_requirements = Column(Text, nullable=True)
    common_pests = Column(Text, nullable=True)  # JSON string
    common_diseases = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendations = relationship("CropRecommendation", back_populates="crop")


class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    
    # Recommendation Details
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    reason = Column(Text, nullable=True)
    season = Column(String(20), nullable=False)
    
    # Soil and Weather Context
    soil_type = Column(String(50), nullable=True)
    weather_conditions = Column(Text, nullable=True)  # JSON string
    market_conditions = Column(Text, nullable=True)  # JSON string
    
    # User Response
    is_accepted = Column(Boolean, nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    crop = relationship("Crop", back_populates="recommendations")
