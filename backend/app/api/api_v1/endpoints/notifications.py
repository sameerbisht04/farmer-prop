from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.notification import Notification

router = APIRouter()


@router.get("/")
async def get_notifications(
    limit: int = 20,
    offset: int = 0,
    notification_type: Optional[str] = None,
    is_read: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's notifications
    """
    try:
        query = db.query(Notification).filter(Notification.user_id == current_user.id)
        
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        
        notifications = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "notifications": [
                {
                    "id": notification.id,
                    "title": notification.title,
                    "message": notification.message,
                    "notification_type": notification.notification_type,
                    "crop_name": notification.crop_name,
                    "action_required": notification.action_required,
                    "priority": notification.priority,
                    "delivery_method": notification.delivery_method,
                    "delivery_status": notification.delivery_status,
                    "scheduled_at": notification.scheduled_at,
                    "sent_at": notification.sent_at,
                    "delivered_at": notification.delivered_at,
                    "is_read": notification.is_read,
                    "is_acknowledged": notification.is_acknowledged,
                    "read_at": notification.read_at,
                    "acknowledged_at": notification.acknowledged_at,
                    "language": notification.language,
                    "created_at": notification.created_at
                }
                for notification in notifications
            ],
            "total": len(notifications)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")


@router.patch("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as read
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.is_read = True
        db.commit()
        
        return {"message": "Notification marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")


@router.patch("/mark-all-read")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read
    """
    try:
        from datetime import datetime
        
        notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ).all()
        
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": f"Marked {len(notifications)} notifications as read"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking all notifications as read: {str(e)}")


@router.patch("/{notification_id}/acknowledge")
async def acknowledge_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Acknowledge a notification
    """
    try:
        from datetime import datetime
        
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.is_acknowledged = True
        notification.acknowledged_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Notification acknowledged"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error acknowledging notification: {str(e)}")


@router.patch("/preferences")
async def update_notification_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's notification preferences
    """
    try:
        import json
        
        current_user.notification_preferences = json.dumps(preferences)
        db.commit()
        
        return {
            "message": "Notification preferences updated successfully",
            "preferences": preferences
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating notification preferences: {str(e)}")


@router.get("/preferences")
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's notification preferences
    """
    try:
        import json
        
        preferences = {}
        if current_user.notification_preferences:
            preferences = json.loads(current_user.notification_preferences)
        
        return {
            "preferences": preferences
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notification preferences: {str(e)}")


@router.get("/stats")
async def get_notification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notification statistics for the user
    """
    try:
        total_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id
        ).count()
        
        unread_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        ).count()
        
        unacknowledged_notifications = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.is_acknowledged == False
        ).count()
        
        # Get notifications by type
        notifications_by_type = db.query(
            Notification.notification_type,
            db.func.count(Notification.id).label('count')
        ).filter(Notification.user_id == current_user.id).group_by(Notification.notification_type).all()
        
        return {
            "total_notifications": total_notifications,
            "unread_notifications": unread_notifications,
            "unacknowledged_notifications": unacknowledged_notifications,
            "notifications_by_type": [
                {"type": notif_type, "count": count}
                for notif_type, count in notifications_by_type
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notification stats: {str(e)}")


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a notification
    """
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        db.delete(notification)
        db.commit()
        
        return {"message": "Notification deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")
