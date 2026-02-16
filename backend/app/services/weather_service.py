import asyncio
import requests
from typing import Dict, Any, Optional
from app.core.config import settings


class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    async def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather data for a location
        """
        try:
            if not self.api_key:
                return self._get_mock_weather_data()
            
            # For now, use a default location if coordinates not provided
            # In production, this would use geocoding to get coordinates
            lat, lon = self._get_coordinates_from_location(location)
            
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"]["deg"],
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                "description": data["weather"][0]["description"],
                "location": location
            }
            
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather_data()

    async def get_weather_forecast(self, location: str, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for a location
        """
        try:
            if not self.api_key:
                return self._get_mock_forecast_data()
            
            lat, lon = self._get_coordinates_from_location(location)
            
            url = f"{self.base_url}/forecast"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data
            forecast = []
            for item in data["list"][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                forecast.append({
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "rainfall": item.get("rain", {}).get("3h", 0),
                    "description": item["weather"][0]["description"]
                })
            
            return {
                "location": location,
                "forecast": forecast
            }
            
        except Exception as e:
            print(f"Weather forecast error: {e}")
            return self._get_mock_forecast_data()

    async def get_weather_alerts(self, location: str) -> list:
        """
        Get weather alerts for a location
        """
        try:
            # This would integrate with weather alert services
            # For now, return empty list
            return []
            
        except Exception as e:
            print(f"Weather alerts error: {e}")
            return []

    def _get_coordinates_from_location(self, location: str) -> tuple:
        """
        Get coordinates from location string
        This is a simplified version - in production, use proper geocoding
        """
        # Default coordinates for India (Delhi)
        default_coords = (28.6139, 77.2090)
        
        # Simple mapping for common locations
        location_mapping = {
            "delhi": (28.6139, 77.2090),
            "mumbai": (19.0760, 72.8777),
            "bangalore": (12.9716, 77.5946),
            "kolkata": (22.5726, 88.3639),
            "chennai": (13.0827, 80.2707),
            "hyderabad": (17.3850, 78.4867),
            "pune": (18.5204, 73.8567),
            "ahmedabad": (23.0225, 72.5714),
            "jaipur": (26.9124, 75.7873),
            "lucknow": (26.8467, 80.9462)
        }
        
        location_lower = location.lower()
        for city, coords in location_mapping.items():
            if city in location_lower:
                return coords
        
        return default_coords

    def _get_mock_weather_data(self) -> Dict[str, Any]:
        """
        Return mock weather data when API is not available
        """
        return {
            "temperature": 25.0,
            "humidity": 65.0,
            "pressure": 1013.25,
            "wind_speed": 5.0,
            "wind_direction": 180,
            "visibility": 10.0,
            "description": "clear sky",
            "location": "mock_location"
        }

    def _get_mock_forecast_data(self) -> Dict[str, Any]:
        """
        Return mock forecast data when API is not available
        """
        import datetime
        
        forecast = []
        for i in range(7):
            date = datetime.datetime.now() + datetime.timedelta(days=i)
            forecast.append({
                "datetime": date.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": 25.0 + (i * 2),
                "humidity": 65.0 - (i * 2),
                "rainfall": 0.0 if i % 2 == 0 else 2.5,
                "description": "clear sky" if i % 2 == 0 else "light rain"
            })
        
        return {
            "location": "mock_location",
            "forecast": forecast
        }

    async def get_agricultural_weather_advice(self, location: str, crop_type: str = None) -> Dict[str, Any]:
        """
        Get weather-based agricultural advice
        """
        try:
            current_weather = await self.get_current_weather(location)
            forecast = await self.get_weather_forecast(location, 3)
            
            advice = {
                "current_conditions": current_weather,
                "recommendations": []
            }
            
            # Generate recommendations based on weather
            if current_weather["humidity"] > 80:
                advice["recommendations"].append("High humidity - watch for fungal diseases")
            
            if current_weather["temperature"] > 35:
                advice["recommendations"].append("High temperature - ensure adequate irrigation")
            
            if current_weather["wind_speed"] > 10:
                advice["recommendations"].append("Strong winds - avoid spraying pesticides")
            
            # Check forecast for rain
            upcoming_rain = any(
                day["rainfall"] > 0 for day in forecast["forecast"][:3]
            )
            if upcoming_rain:
                advice["recommendations"].append("Rain expected - plan irrigation accordingly")
            
            return advice
            
        except Exception as e:
            print(f"Agricultural weather advice error: {e}")
            return {
                "current_conditions": self._get_mock_weather_data(),
                "recommendations": ["Check weather conditions before farming activities"]
            }
