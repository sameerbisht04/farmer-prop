from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Post Content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(50), nullable=False)  # question, experience, tip, problem
    
    # Categories
    crop_category = Column(String(100), nullable=True)
    topic_tags = Column(Text, nullable=True)  # JSON string of tags
    
    # Media
    image_urls = Column(Text, nullable=True)  # JSON string
    video_urls = Column(Text, nullable=True)  # JSON string
    
    # Engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    # Moderation
    is_approved = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    
    # Language
    language = Column(String(5), default="hi")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="community_posts")
    comments = relationship("CommunityComment", back_populates="post")


class CommunityComment(Base):
    __tablename__ = "community_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("community_comments.id"), nullable=True)
    
    # Comment Content
    content = Column(Text, nullable=False)
    
    # Engagement
    likes_count = Column(Integer, default=0)
    
    # Moderation
    is_approved = Column(Boolean, default=True)
    
    # Language
    language = Column(String(5), default="hi")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    post = relationship("CommunityPost", back_populates="comments")
    user = relationship("User")
    parent_comment = relationship("CommunityComment", remote_side=[id])
    replies = relationship("CommunityComment", back_populates="parent_comment")
