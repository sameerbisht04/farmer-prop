from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import cv2
import numpy as np
from PIL import Image
import io
import base64

from app.core.database import get_db
from app.models.user import User
from app.models.advisory import Advisory
from app.services.image_classification_service import ImageClassificationService
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/classify-crop-disease")
async def classify_crop_disease(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    crop_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Classify crop disease from uploaded image
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Initialize classification service
        classification_service = ImageClassificationService()
        
        # Classify the image
        result = await classification_service.classify_crop_disease(
            image_data=image_data,
            crop_type=crop_type
        )
        
        # Save advisory based on classification result
        if result["confidence"] > 0.5:
            advisory = Advisory(
                user_id=current_user.id,
                title=f"रोग पहचान: {result['disease_name']}",
                content=result["description"] + "\n\n" + result["treatment_advice"],
                advisory_type="disease_identification",
                crop_name=crop_type or result.get("crop_type", "Unknown"),
                language=current_user.preferred_language,
                is_ai_generated=True,
                confidence_score=result["confidence"],
                model_version=result.get("model_version", "v1.0")
            )
            
            background_tasks.add_task(save_advisory, advisory, db)
        
        return {
            "disease_name": result["disease_name"],
            "confidence": result["confidence"],
            "description": result["description"],
            "treatment_advice": result["treatment_advice"],
            "prevention_tips": result["prevention_tips"],
            "severity": result["severity"],
            "crop_type": result.get("crop_type", crop_type)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image classification error: {str(e)}")


@router.post("/classify-pest")
async def classify_pest(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    crop_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Classify pest from uploaded image
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Initialize classification service
        classification_service = ImageClassificationService()
        
        # Classify the pest
        result = await classification_service.classify_pest(
            image_data=image_data,
            crop_type=crop_type
        )
        
        # Save advisory based on classification result
        if result["confidence"] > 0.5:
            advisory = Advisory(
                user_id=current_user.id,
                title=f"कीट पहचान: {result['pest_name']}",
                content=result["description"] + "\n\n" + result["control_measures"],
                advisory_type="pest_identification",
                crop_name=crop_type or result.get("crop_type", "Unknown"),
                language=current_user.preferred_language,
                is_ai_generated=True,
                confidence_score=result["confidence"],
                model_version=result.get("model_version", "v1.0")
            )
            
            background_tasks.add_task(save_advisory, advisory, db)
        
        return {
            "pest_name": result["pest_name"],
            "confidence": result["confidence"],
            "description": result["description"],
            "control_measures": result["control_measures"],
            "prevention_tips": result["prevention_tips"],
            "damage_symptoms": result["damage_symptoms"],
            "crop_type": result.get("crop_type", crop_type)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pest classification error: {str(e)}")


@router.post("/classify-crop")
async def classify_crop(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Classify crop type from uploaded image
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Initialize classification service
        classification_service = ImageClassificationService()
        
        # Classify the crop
        result = await classification_service.classify_crop(image_data=image_data)
        
        return {
            "crop_name": result["crop_name"],
            "confidence": result["confidence"],
            "description": result["description"],
            "growth_stage": result["growth_stage"],
            "health_status": result["health_status"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop classification error: {str(e)}")


@router.post("/analyze-plant-health")
async def analyze_plant_health(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    crop_type: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Comprehensive plant health analysis
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image data
        image_data = await image.read()
        
        # Initialize classification service
        classification_service = ImageClassificationService()
        
        # Perform comprehensive analysis
        result = await classification_service.analyze_plant_health(
            image_data=image_data,
            crop_type=crop_type
        )
        
        # Save advisory based on analysis result
        if result["overall_health_score"] < 0.7:
            advisory = Advisory(
                user_id=current_user.id,
                title="पौधे की सेहत का विश्लेषण",
                content=result["health_summary"] + "\n\n" + result["recommendations"],
                advisory_type="plant_health_analysis",
                crop_name=crop_type or result.get("crop_type", "Unknown"),
                language=current_user.preferred_language,
                is_ai_generated=True,
                confidence_score=result["confidence"],
                model_version=result.get("model_version", "v1.0")
            )
            
            background_tasks.add_task(save_advisory, advisory, db)
        
        return {
            "overall_health_score": result["overall_health_score"],
            "health_status": result["health_status"],
            "issues_detected": result["issues_detected"],
            "health_summary": result["health_summary"],
            "recommendations": result["recommendations"],
            "confidence": result["confidence"],
            "crop_type": result.get("crop_type", crop_type)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plant health analysis error: {str(e)}")


async def save_advisory(advisory: Advisory, db: Session):
    """Background task to save advisory to database"""
    try:
        db.add(advisory)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving advisory: {e}")
