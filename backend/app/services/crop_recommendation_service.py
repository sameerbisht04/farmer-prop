import json
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.crop import Crop, CropRecommendation
from app.models.soil import SoilType
from app.services.weather_service import WeatherService


class CropRecommendationService:
    def __init__(self):
        self.weather_service = WeatherService()
        
        # Crop suitability matrix
        self.crop_suitability = {
            "rice": {
                "soil_types": ["clay", "clay_loam"],
                "temperature_range": (20, 35),
                "rainfall_range": (1000, 2000),
                "season": "kharif",
                "water_requirement": "high"
            },
            "wheat": {
                "soil_types": ["loam", "clay_loam"],
                "temperature_range": (15, 25),
                "rainfall_range": (400, 800),
                "season": "rabi",
                "water_requirement": "medium"
            },
            "maize": {
                "soil_types": ["loam", "sandy_loam"],
                "temperature_range": (18, 30),
                "rainfall_range": (600, 1000),
                "season": "kharif",
                "water_requirement": "medium"
            },
            "cotton": {
                "soil_types": ["black_soil", "clay_loam"],
                "temperature_range": (20, 35),
                "rainfall_range": (500, 1000),
                "season": "kharif",
                "water_requirement": "medium"
            },
            "sugarcane": {
                "soil_types": ["clay", "clay_loam"],
                "temperature_range": (25, 35),
                "rainfall_range": (1000, 1500),
                "season": "kharif",
                "water_requirement": "high"
            },
            "potato": {
                "soil_types": ["loam", "sandy_loam"],
                "temperature_range": (15, 25),
                "rainfall_range": (300, 600),
                "season": "rabi",
                "water_requirement": "medium"
            },
            "tomato": {
                "soil_types": ["loam", "sandy_loam"],
                "temperature_range": (18, 28),
                "rainfall_range": (400, 800),
                "season": "zaid",
                "water_requirement": "medium"
            },
            "onion": {
                "soil_types": ["loam", "sandy_loam"],
                "temperature_range": (15, 25),
                "rainfall_range": (300, 600),
                "season": "rabi",
                "water_requirement": "low"
            }
        }

    async def get_crop_recommendations(
        self, 
        location: str, 
        season: str, 
        soil_type: str, 
        farm_size: float,
        db: Session
    ) -> List[Dict[str, Any]]:
        """
        Get crop recommendations based on various factors
        """
        try:
            # Get weather data
            weather_data = await self.weather_service.get_current_weather(location)
            
            # Get available crops from database
            crops = db.query(Crop).all()
            
            recommendations = []
            
            for crop in crops:
                if crop.name.lower() in self.crop_suitability:
                    suitability_data = self.crop_suitability[crop.name.lower()]
                    
                    # Calculate suitability score
                    score = self._calculate_suitability_score(
                        crop.name.lower(),
                        suitability_data,
                        season,
                        soil_type,
                        weather_data
                    )
                    
                    if score > 0.5:  # Only recommend crops with >50% suitability
                        recommendations.append({
                            "crop_id": crop.id,
                            "crop_name": crop.name,
                            "scientific_name": crop.scientific_name,
                            "local_name_hindi": crop.local_name_hindi,
                            "suitability_score": score,
                            "season": season,
                            "expected_yield": self._estimate_yield(crop.name.lower(), farm_size),
                            "market_price": self._get_market_price(crop.name.lower()),
                            "reason": self._get_recommendation_reason(
                                crop.name.lower(), suitability_data, season, soil_type
                            )
                        })
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            print(f"Crop recommendation error: {e}")
            return []

    def _calculate_suitability_score(
        self, 
        crop_name: str, 
        suitability_data: Dict[str, Any], 
        season: str, 
        soil_type: str, 
        weather_data: Dict[str, Any]
    ) -> float:
        """
        Calculate suitability score for a crop
        """
        score = 0.0
        factors = 0
        
        # Season match (40% weight)
        if suitability_data["season"] == season:
            score += 0.4
        factors += 1
        
        # Soil type match (30% weight)
        if soil_type in suitability_data["soil_types"]:
            score += 0.3
        factors += 1
        
        # Temperature suitability (20% weight)
        if weather_data and "temperature" in weather_data:
            temp = weather_data["temperature"]
            temp_range = suitability_data["temperature_range"]
            if temp_range[0] <= temp <= temp_range[1]:
                score += 0.2
            else:
                # Partial score based on how close temperature is to range
                if temp < temp_range[0]:
                    score += 0.2 * (1 - (temp_range[0] - temp) / 10)
                else:
                    score += 0.2 * (1 - (temp - temp_range[1]) / 10)
        factors += 1
        
        # Rainfall suitability (10% weight)
        if weather_data and "humidity" in weather_data:
            # Use humidity as proxy for rainfall availability
            humidity = weather_data["humidity"]
            if humidity >= 60:  # Good moisture availability
                score += 0.1
        factors += 1
        
        return max(0.0, min(1.0, score))

    def _estimate_yield(self, crop_name: str, farm_size: float) -> float:
        """
        Estimate yield for a crop based on farm size
        """
        # Average yield per acre (in quintals)
        yield_per_acre = {
            "rice": 25,
            "wheat": 30,
            "maize": 20,
            "cotton": 15,
            "sugarcane": 300,
            "potato": 200,
            "tomato": 150,
            "onion": 100
        }
        
        base_yield = yield_per_acre.get(crop_name, 20)
        return base_yield * farm_size

    def _get_market_price(self, crop_name: str) -> Dict[str, float]:
        """
        Get estimated market price for a crop
        """
        # Average market prices per quintal (in INR)
        prices = {
            "rice": {"min": 2000, "max": 3000},
            "wheat": {"min": 1800, "max": 2500},
            "maize": {"min": 1500, "max": 2000},
            "cotton": {"min": 5000, "max": 7000},
            "sugarcane": {"min": 300, "max": 400},
            "potato": {"min": 800, "max": 1200},
            "tomato": {"min": 2000, "max": 4000},
            "onion": {"min": 1500, "max": 3000}
        }
        
        return prices.get(crop_name, {"min": 1000, "max": 2000})

    def _get_recommendation_reason(
        self, 
        crop_name: str, 
        suitability_data: Dict[str, Any], 
        season: str, 
        soil_type: str
    ) -> str:
        """
        Generate human-readable reason for recommendation
        """
        reasons = []
        
        if suitability_data["season"] == season:
            reasons.append(f"सही मौसम ({season})")
        
        if soil_type in suitability_data["soil_types"]:
            reasons.append(f"उपयुक्त मिट्टी ({soil_type})")
        
        if suitability_data["water_requirement"] == "low":
            reasons.append("कम पानी की आवश्यकता")
        elif suitability_data["water_requirement"] == "medium":
            reasons.append("मध्यम पानी की आवश्यकता")
        else:
            reasons.append("अधिक पानी की आवश्यकता")
        
        return ", ".join(reasons) if reasons else "सामान्य सुझाव"

    async def save_crop_recommendation(
        self, 
        user_id: int, 
        crop_id: int, 
        recommendation_data: Dict[str, Any], 
        db: Session
    ) -> CropRecommendation:
        """
        Save crop recommendation to database
        """
        try:
            recommendation = CropRecommendation(
                user_id=user_id,
                crop_id=crop_id,
                confidence_score=recommendation_data["suitability_score"],
                reason=recommendation_data["reason"],
                season=recommendation_data["season"],
                soil_type=recommendation_data.get("soil_type"),
                weather_conditions=json.dumps(recommendation_data.get("weather_conditions", {})),
                market_conditions=json.dumps(recommendation_data.get("market_conditions", {}))
            )
            
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)
            
            return recommendation
            
        except Exception as e:
            db.rollback()
            print(f"Error saving crop recommendation: {e}")
            raise e
