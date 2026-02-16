from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.user import User
from app.models.advisory import Advisory
from app.models.notification import Notification
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self):
        pass

    async def update_user_profile(
        self, 
        user_id: int, 
        user_update: UserUpdate, 
        db: Session
    ) -> User:
        """
        Update user profile
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            # Update fields that are provided
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            db.commit()
            db.refresh(user)
            return user
            
        except Exception as e:
            db.rollback()
            raise e

    async def get_user_notifications(
        self, 
        user_id: int, 
        limit: int, 
        offset: int, 
        db: Session
    ) -> Dict[str, Any]:
        """
        Get user notifications
        """
        try:
            notifications = db.query(Notification).filter(
                Notification.user_id == user_id
            ).order_by(desc(Notification.created_at)).offset(offset).limit(limit).all()
            
            total = db.query(Notification).filter(
                Notification.user_id == user_id
            ).count()
            
            return {
                "notifications": [
                    {
                        "id": notification.id,
                        "title": notification.title,
                        "message": notification.message,
                        "type": notification.notification_type,
                        "priority": notification.priority,
                        "is_read": notification.is_read,
                        "created_at": notification.created_at,
                        "delivery_status": notification.delivery_status
                    }
                    for notification in notifications
                ],
                "total": total,
                "unread_count": db.query(Notification).filter(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                ).count()
            }
            
        except Exception as e:
            raise e

    async def update_notification_preferences(
        self, 
        user_id: int, 
        preferences: Dict[str, Any], 
        db: Session
    ) -> None:
        """
        Update user notification preferences
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            import json
            user.notification_preferences = json.dumps(preferences)
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise e

    async def get_user_statistics(self, user_id: int, db: Session) -> Dict[str, Any]:
        """
        Get user statistics
        """
        try:
            # Get advisory statistics
            total_advisories = db.query(Advisory).filter(
                Advisory.user_id == user_id
            ).count()
            
            unread_advisories = db.query(Advisory).filter(
                Advisory.user_id == user_id,
                Advisory.is_read == False
            ).count()
            
            # Get notification statistics
            total_notifications = db.query(Notification).filter(
                Notification.user_id == user_id
            ).count()
            
            unread_notifications = db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).count()
            
            # Get advisory types distribution
            advisory_types = db.query(
                Advisory.advisory_type,
                func.count(Advisory.id).label('count')
            ).filter(
                Advisory.user_id == user_id
            ).group_by(Advisory.advisory_type).all()
            
            return {
                "advisories": {
                    "total": total_advisories,
                    "unread": unread_advisories,
                    "by_type": [
                        {"type": adv_type, "count": count}
                        for adv_type, count in advisory_types
                    ]
                },
                "notifications": {
                    "total": total_notifications,
                    "unread": unread_notifications
                },
                "account": {
                    "created_at": db.query(User.created_at).filter(
                        User.id == user_id
                    ).scalar(),
                    "last_login": db.query(User.last_login).filter(
                        User.id == user_id
                    ).scalar()
                }
            }
            
        except Exception as e:
            raise e

    async def get_user_by_phone(self, phone_number: str, db: Session) -> User:
        """
        Get user by phone number
        """
        try:
            user = db.query(User).filter(User.phone_number == phone_number).first()
            return user
        except Exception as e:
            raise e

    async def create_user(self, user_data: Dict[str, Any], db: Session) -> User:
        """
        Create new user
        """
        try:
            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e

    async def verify_user(self, user_id: int, db: Session) -> User:
        """
        Verify user account
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise ValueError("User not found")
            
            user.is_verified = True
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            raise e
