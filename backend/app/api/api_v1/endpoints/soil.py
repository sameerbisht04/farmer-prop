from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.soil import SoilType, SoilTest

router = APIRouter()


@router.get("/types")
async def get_soil_types(db: Session = Depends(get_db)):
    """
    Get list of available soil types
    """
    try:
        soil_types = db.query(SoilType).all()
        
        return {
            "soil_types": [
                {
                    "id": soil_type.id,
                    "name": soil_type.name,
                    "description": soil_type.description,
                    "ph_range_min": soil_type.ph_range_min,
                    "ph_range_max": soil_type.ph_range_max,
                    "organic_matter_percentage": soil_type.organic_matter_percentage,
                    "water_retention_capacity": soil_type.water_retention_capacity
                }
                for soil_type in soil_types
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching soil types: {str(e)}")


@router.get("/tests")
async def get_soil_tests(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's soil test history
    """
    try:
        soil_tests = db.query(SoilTest).filter(
            SoilTest.user_id == current_user.id
        ).order_by(SoilTest.test_date.desc()).offset(offset).limit(limit).all()
        
        return {
            "soil_tests": [
                {
                    "id": test.id,
                    "ph_level": test.ph_level,
                    "nitrogen_content": test.nitrogen_content,
                    "phosphorus_content": test.phosphorus_content,
                    "potassium_content": test.potassium_content,
                    "organic_matter": test.organic_matter,
                    "soil_type": test.soil_type,
                    "texture": test.texture,
                    "test_date": test.test_date,
                    "lab_name": test.lab_name,
                    "recommendations": test.recommendations
                }
                for test in soil_tests
            ],
            "total": len(soil_tests)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching soil tests: {str(e)}")


@router.post("/tests")
async def add_soil_test(
    ph_level: Optional[float] = None,
    nitrogen_content: Optional[float] = None,
    phosphorus_content: Optional[float] = None,
    potassium_content: Optional[float] = None,
    organic_matter: Optional[float] = None,
    soil_type: Optional[str] = None,
    texture: Optional[str] = None,
    lab_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new soil test result
    """
    try:
        from datetime import datetime
        
        soil_test = SoilTest(
            user_id=current_user.id,
            ph_level=ph_level,
            nitrogen_content=nitrogen_content,
            phosphorus_content=phosphorus_content,
            potassium_content=potassium_content,
            organic_matter=organic_matter,
            soil_type=soil_type,
            texture=texture,
            test_date=datetime.utcnow(),
            lab_name=lab_name
        )
        
        db.add(soil_test)
        db.commit()
        db.refresh(soil_test)
        
        return {
            "message": "Soil test added successfully",
            "soil_test_id": soil_test.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding soil test: {str(e)}")


@router.get("/tests/{test_id}")
async def get_soil_test_details(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed soil test information
    """
    try:
        soil_test = db.query(SoilTest).filter(
            SoilTest.id == test_id,
            SoilTest.user_id == current_user.id
        ).first()
        
        if not soil_test:
            raise HTTPException(status_code=404, detail="Soil test not found")
        
        return {
            "id": soil_test.id,
            "ph_level": soil_test.ph_level,
            "nitrogen_content": soil_test.nitrogen_content,
            "phosphorus_content": soil_test.phosphorus_content,
            "potassium_content": soil_test.potassium_content,
            "organic_matter": soil_test.organic_matter,
            "soil_type": soil_test.soil_type,
            "texture": soil_test.texture,
            "moisture_content": soil_test.moisture_content,
            "test_date": soil_test.test_date,
            "lab_name": soil_test.lab_name,
            "test_method": soil_test.test_method,
            "recommendations": soil_test.recommendations,
            "fertilizer_suggestions": soil_test.fertilizer_suggestions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching soil test details: {str(e)}")
