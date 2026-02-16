from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification Content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # reminder, alert, advisory, market_update
    
    # Context Information
    crop_name = Column(String(100), nullable=True)
    action_required = Column(String(100), nullable=True)  # irrigation, spraying, harvesting, etc.
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    # Delivery Information
    delivery_method = Column(String(20), nullable=False)  # sms, whatsapp, push, email
    delivery_status = Column(String(20), default="pending")  # pending, sent, delivered, failed
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    
    # User Interaction
    is_read = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    
    # Language
    language = Column(String(5), default="hi")
    
    # Related Data
    related_advisory_id = Column(Integer, nullable=True)
    related_market_insight_id = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
