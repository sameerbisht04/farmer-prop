from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)
    
    # Crop Information
    crop_name = Column(String(100), nullable=False, index=True)
    variety = Column(String(100), nullable=True)
    
    # Location Information
    market_name = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    
    # Price Information
    min_price = Column(Float, nullable=False)  # per quintal
    max_price = Column(Float, nullable=False)  # per quintal
    modal_price = Column(Float, nullable=True)  # most common price
    
    # Market Details
    arrival_quantity = Column(Float, nullable=True)  # quintals
    quality_grade = Column(String(20), nullable=True)  # A, B, C grade
    
    # Data Source
    source = Column(String(50), default="mandi")  # mandi, government, private
    
    # Timestamps
    price_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Index for efficient querying
    __table_args__ = (
        {"extend_existing": True}
    )


class MarketInsight(Base):
    __tablename__ = "market_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Insight Content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    insight_type = Column(String(50), nullable=False)  # price_trend, demand_forecast, etc.
    
    # Crop and Location Context
    crop_name = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    
    # Data Analysis
    trend_direction = Column(String(20), nullable=True)  # up, down, stable
    confidence_level = Column(Float, nullable=True)  # 0.0 to 1.0
    time_horizon = Column(String(20), nullable=True)  # short_term, medium_term, long_term
    
    # Supporting Data
    historical_data = Column(Text, nullable=True)  # JSON string
    forecast_data = Column(Text, nullable=True)  # JSON string
    
    # AI Generated
    is_ai_generated = Column(Boolean, default=True)
    model_version = Column(String(20), nullable=True)
    
    # Language
    language = Column(String(5), default="hi")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
