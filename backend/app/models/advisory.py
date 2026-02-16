from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Advisory Content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    advisory_type = Column(String(50), nullable=False)  # crop_selection, pest_control, fertilizer, etc.
    
    # Context Information
    crop_name = Column(String(100), nullable=True)
    season = Column(String(20), nullable=True)
    soil_type = Column(String(50), nullable=True)
    weather_conditions = Column(Text, nullable=True)  # JSON string
    
    # AI Generated
    is_ai_generated = Column(Boolean, default=True)
    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(20), nullable=True)
    
    # Language and Localization
    language = Column(String(5), default="hi")
    localized_content = Column(Text, nullable=True)  # Content in user's preferred language
    
    # Media Attachments
    image_urls = Column(Text, nullable=True)  # JSON string of image URLs
    video_urls = Column(Text, nullable=True)  # JSON string of video URLs
    
    # Status
    is_read = Column(Boolean, default=False)
    is_helpful = Column(Boolean, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="advisories")
    feedback = relationship("AdvisoryFeedback", back_populates="advisory")


class AdvisoryFeedback(Base):
    __tablename__ = "advisory_feedback"

    id = Column(Integer, primary_key=True, index=True)
    advisory_id = Column(Integer, ForeignKey("advisories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Feedback Details
    rating = Column(Integer, nullable=False)  # 1-5 scale
    is_helpful = Column(Boolean, nullable=False)
    feedback_text = Column(Text, nullable=True)
    
    # Specific Feedback Categories
    accuracy_rating = Column(Integer, nullable=True)  # 1-5
    clarity_rating = Column(Integer, nullable=True)  # 1-5
    timeliness_rating = Column(Integer, nullable=True)  # 1-5
    
    # Improvement Suggestions
    suggestions = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    advisory = relationship("Advisory", back_populates="feedback")
    user = relationship("User")
