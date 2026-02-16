from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String(100), nullable=True)
    
    # Weather Conditions
    temperature = Column(Float, nullable=True)  # Celsius
    humidity = Column(Float, nullable=True)  # percentage
    rainfall = Column(Float, nullable=True)  # mm
    wind_speed = Column(Float, nullable=True)  # km/h
    wind_direction = Column(String(10), nullable=True)
    pressure = Column(Float, nullable=True)  # hPa
    visibility = Column(Float, nullable=True)  # km
    
    # Forecast Data
    forecast_data = Column(Text, nullable=True)  # JSON string for 7-day forecast
    
    # Weather Alerts
    alerts = Column(Text, nullable=True)  # JSON string of weather warnings
    
    # Data Source
    source = Column(String(50), default="openweather")  # openweather, imd, etc.
    
    # Timestamps
    recorded_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
