from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SoilType(Base):
    __tablename__ = "soil_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Soil Properties
    ph_range_min = Column(Float, nullable=True)
    ph_range_max = Column(Float, nullable=True)
    organic_matter_percentage = Column(Float, nullable=True)
    water_retention_capacity = Column(Float, nullable=True)
    
    # Suitable Crops
    suitable_crops = Column(Text, nullable=True)  # JSON string of crop IDs
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SoilTest(Base):
    __tablename__ = "soil_tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Test Results
    ph_level = Column(Float, nullable=True)
    nitrogen_content = Column(Float, nullable=True)  # ppm
    phosphorus_content = Column(Float, nullable=True)  # ppm
    potassium_content = Column(Float, nullable=True)  # ppm
    organic_matter = Column(Float, nullable=True)  # percentage
    
    # Additional Properties
    soil_type = Column(String(50), nullable=True)
    texture = Column(String(50), nullable=True)  # sandy, clay, loam, etc.
    moisture_content = Column(Float, nullable=True)
    
    # Test Information
    test_date = Column(DateTime(timezone=True), nullable=False)
    lab_name = Column(String(100), nullable=True)
    test_method = Column(String(50), nullable=True)
    
    # Recommendations
    recommendations = Column(Text, nullable=True)  # JSON string
    fertilizer_suggestions = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="soil_tests")
