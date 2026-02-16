from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.crop import Crop, CropRecommendation
from app.services.crop_recommendation_service import CropRecommendationService

router = APIRouter()


@router.get("/")
async def get_crops(
    limit: int = 20,
    offset: int = 0,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of available crops
    """
    try:
        query = db.query(Crop)
        
        if search:
            query = query.filter(Crop.name.ilike(f"%{search}%"))
        
        crops = query.offset(offset).limit(limit).all()
        
        return {
            "crops": [
                {
                    "id": crop.id,
                    "name": crop.name,
                    "scientific_name": crop.scientific_name,
                    "local_name_hindi": crop.local_name_hindi,
                    "local_name_punjabi": crop.local_name_punjabi,
                    "crop_type": crop.crop_type,
                    "season": crop.season,
                    "duration_days": crop.duration_days
                }
                for crop in crops
            ],
            "total": len(crops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crops: {str(e)}")


@router.get("/{crop_id}")
async def get_crop_details(
    crop_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific crop
    """
    try:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return {
            "id": crop.id,
            "name": crop.name,
            "scientific_name": crop.scientific_name,
            "local_name_hindi": crop.local_name_hindi,
            "local_name_punjabi": crop.local_name_punjabi,
            "crop_type": crop.crop_type,
            "season": crop.season,
            "duration_days": crop.duration_days,
            "min_temperature": crop.min_temperature,
            "max_temperature": crop.max_temperature,
            "optimal_rainfall": crop.optimal_rainfall,
            "average_yield_per_acre": crop.average_yield_per_acre,
            "water_requirements": crop.water_requirements,
            "fertilizer_requirements": crop.fertilizer_requirements,
            "common_pests": crop.common_pests,
            "common_diseases": crop.common_diseases
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching crop details: {str(e)}")


@router.post("/recommendations")
async def get_crop_recommendations(
    location: str,
    season: str,
    soil_type: str,
    farm_size: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get crop recommendations based on various factors
    """
    try:
        crop_service = CropRecommendationService()
        recommendations = await crop_service.get_crop_recommendations(
            location=location,
            season=season,
            soil_type=soil_type,
            farm_size=farm_size,
            db=db
        )
        
        return {
            "recommendations": recommendations,
            "location": location,
            "season": season,
            "soil_type": soil_type,
            "farm_size": farm_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")


@router.get("/user/recommendations")
async def get_user_recommendations(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's crop recommendations history
    """
    try:
        recommendations = db.query(CropRecommendation).filter(
            CropRecommendation.user_id == current_user.id
        ).order_by(CropRecommendation.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "recommendations": [
                {
                    "id": rec.id,
                    "crop_name": rec.crop.name if rec.crop else "Unknown",
                    "confidence_score": rec.confidence_score,
                    "reason": rec.reason,
                    "season": rec.season,
                    "is_accepted": rec.is_accepted,
                    "created_at": rec.created_at
                }
                for rec in recommendations
            ],
            "total": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user recommendations: {str(e)}")
