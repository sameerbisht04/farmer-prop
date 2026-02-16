from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/current")
async def get_current_weather(
    location: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current weather data for a location
    """
    try:
        weather_service = WeatherService()
        weather_data = await weather_service.get_current_weather(location)
        
        return {
            "location": location,
            "weather": weather_data,
            "timestamp": weather_data.get("timestamp")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")


@router.get("/forecast")
async def get_weather_forecast(
    location: str,
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get weather forecast for a location
    """
    try:
        weather_service = WeatherService()
        forecast_data = await weather_service.get_weather_forecast(location, days)
        
        return {
            "location": location,
            "forecast": forecast_data,
            "days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather forecast: {str(e)}")


@router.get("/alerts")
async def get_weather_alerts(
    location: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get weather alerts for a location
    """
    try:
        weather_service = WeatherService()
        alerts = await weather_service.get_weather_alerts(location)
        
        return {
            "location": location,
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather alerts: {str(e)}")


@router.get("/agricultural-advice")
async def get_agricultural_weather_advice(
    location: str,
    crop_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get weather-based agricultural advice
    """
    try:
        weather_service = WeatherService()
        advice = await weather_service.get_agricultural_weather_advice(location, crop_type)
        
        return {
            "location": location,
            "crop_type": crop_type,
            "advice": advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agricultural advice: {str(e)}")
