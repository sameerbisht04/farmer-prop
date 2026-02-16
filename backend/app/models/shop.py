from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    
    # Shop Information
    name = Column(String(200), nullable=False)
    shop_type = Column(String(50), nullable=False)  # government, ngo, private, cooperative
    
    # Contact Information
    phone_number = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    contact_person = Column(String(100), nullable=True)
    
    # Location Information
    address = Column(Text, nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    village = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Shop Details
    license_number = Column(String(100), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_government_approved = Column(Boolean, default=False)
    
    # Services Offered
    services = Column(Text, nullable=True)  # JSON string of services
    payment_methods = Column(Text, nullable=True)  # JSON string
    
    # Operating Hours
    operating_hours = Column(Text, nullable=True)  # JSON string
    
    # Ratings and Reviews
    average_rating = Column(Float, nullable=True)
    total_reviews = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    inventory = relationship("ShopInventory", back_populates="shop")


class ShopInventory(Base):
    __tablename__ = "shop_inventory"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    
    # Product Information
    product_name = Column(String(200), nullable=False)
    product_type = Column(String(50), nullable=False)  # seed, fertilizer, pesticide, equipment
    brand = Column(String(100), nullable=True)
    variety = Column(String(100), nullable=True)
    
    # Product Details
    description = Column(Text, nullable=True)
    specifications = Column(Text, nullable=True)  # JSON string
    
    # Pricing
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # kg, liter, packet, etc.
    discount_percentage = Column(Float, nullable=True)
    
    # Stock Information
    current_stock = Column(Float, nullable=False)
    minimum_stock = Column(Float, nullable=True)
    maximum_stock = Column(Float, nullable=True)
    
    # Product Status
    is_available = Column(Boolean, default=True)
    is_organic = Column(Boolean, default=False)
    is_government_subsidized = Column(Boolean, default=False)
    
    # Quality Information
    quality_grade = Column(String(10), nullable=True)
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    shop = relationship("Shop", back_populates="inventory")
