from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.advisory import Advisory, AdvisoryFeedback

router = APIRouter()


@router.get("/")
async def get_advisories(
    limit: int = 20,
    offset: int = 0,
    advisory_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's advisories
    """
    try:
        query = db.query(Advisory).filter(Advisory.user_id == current_user.id)
        
        if advisory_type:
            query = query.filter(Advisory.advisory_type == advisory_type)
        
        advisories = query.order_by(Advisory.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "advisories": [
                {
                    "id": advisory.id,
                    "title": advisory.title,
                    "content": advisory.content,
                    "advisory_type": advisory.advisory_type,
                    "crop_name": advisory.crop_name,
                    "season": advisory.season,
                    "is_ai_generated": advisory.is_ai_generated,
                    "confidence_score": advisory.confidence_score,
                    "language": advisory.localized_content or advisory.language,
                    "is_read": advisory.is_read,
                    "is_helpful": advisory.is_helpful,
                    "created_at": advisory.created_at
                }
                for advisory in advisories
            ],
            "total": len(advisories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching advisories: {str(e)}")


@router.get("/{advisory_id}")
async def get_advisory_details(
    advisory_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed advisory information
    """
    try:
        advisory = db.query(Advisory).filter(
            Advisory.id == advisory_id,
            Advisory.user_id == current_user.id
        ).first()
        
        if not advisory:
            raise HTTPException(status_code=404, detail="Advisory not found")
        
        # Mark as read
        advisory.is_read = True
        db.commit()
        
        return {
            "id": advisory.id,
            "title": advisory.title,
            "content": advisory.content,
            "advisory_type": advisory.advisory_type,
            "crop_name": advisory.crop_name,
            "season": advisory.season,
            "soil_type": advisory.soil_type,
            "weather_conditions": advisory.weather_conditions,
            "is_ai_generated": advisory.is_ai_generated,
            "confidence_score": advisory.confidence_score,
            "model_version": advisory.model_version,
            "language": advisory.language,
            "localized_content": advisory.localized_content,
            "image_urls": advisory.image_urls,
            "video_urls": advisory.video_urls,
            "is_read": advisory.is_read,
            "is_helpful": advisory.is_helpful,
            "created_at": advisory.created_at,
            "read_at": advisory.read_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching advisory details: {str(e)}")


@router.post("/{advisory_id}/feedback")
async def submit_advisory_feedback(
    advisory_id: int,
    rating: int,
    is_helpful: bool,
    feedback_text: Optional[str] = None,
    accuracy_rating: Optional[int] = None,
    clarity_rating: Optional[int] = None,
    timeliness_rating: Optional[int] = None,
    suggestions: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback for an advisory
    """
    try:
        # Check if advisory exists and belongs to user
        advisory = db.query(Advisory).filter(
            Advisory.id == advisory_id,
            Advisory.user_id == current_user.id
        ).first()
        
        if not advisory:
            raise HTTPException(status_code=404, detail="Advisory not found")
        
        # Create feedback
        feedback = AdvisoryFeedback(
            advisory_id=advisory_id,
            user_id=current_user.id,
            rating=rating,
            is_helpful=is_helpful,
            feedback_text=feedback_text,
            accuracy_rating=accuracy_rating,
            clarity_rating=clarity_rating,
            timeliness_rating=timeliness_rating,
            suggestions=suggestions
        )
        
        db.add(feedback)
        
        # Update advisory helpful status
        advisory.is_helpful = is_helpful
        db.commit()
        
        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback.id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting feedback: {str(e)}")


@router.patch("/{advisory_id}/read")
async def mark_advisory_as_read(
    advisory_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark an advisory as read
    """
    try:
        advisory = db.query(Advisory).filter(
            Advisory.id == advisory_id,
            Advisory.user_id == current_user.id
        ).first()
        
        if not advisory:
            raise HTTPException(status_code=404, detail="Advisory not found")
        
        advisory.is_read = True
        db.commit()
        
        return {"message": "Advisory marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking advisory as read: {str(e)}")


@router.get("/stats/summary")
async def get_advisory_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get advisory statistics for the user
    """
    try:
        total_advisories = db.query(Advisory).filter(Advisory.user_id == current_user.id).count()
        unread_advisories = db.query(Advisory).filter(
            Advisory.user_id == current_user.id,
            Advisory.is_read == False
        ).count()
        
        # Get advisories by type
        advisories_by_type = db.query(
            Advisory.advisory_type,
            db.func.count(Advisory.id).label('count')
        ).filter(Advisory.user_id == current_user.id).group_by(Advisory.advisory_type).all()
        
        return {
            "total_advisories": total_advisories,
            "unread_advisories": unread_advisories,
            "advisories_by_type": [
                {"type": adv_type, "count": count}
                for adv_type, count in advisories_by_type
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching advisory stats: {str(e)}")
