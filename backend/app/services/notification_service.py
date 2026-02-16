import asyncio
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.notification import Notification
from app.models.user import User


class NotificationService:
    def __init__(self):
        self.twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER
        self.whatsapp_access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.whatsapp_phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID

    async def send_sms_otp(self, phone_number: str, otp: str) -> bool:
        """
        Send OTP via SMS using Twilio
        """
        try:
            if not self.twilio_account_sid or not self.twilio_auth_token:
                print("Twilio credentials not configured, using mock SMS")
                return self._mock_sms_send(phone_number, otp)
            
            # Format phone number for India
            formatted_phone = f"+91{phone_number}" if not phone_number.startswith('+') else phone_number
            
            message = f"Your Smart Crop Advisory OTP is: {otp}. Valid for 5 minutes. Do not share with anyone."
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"
            
            data = {
                "From": self.twilio_phone_number,
                "To": formatted_phone,
                "Body": message
            }
            
            response = requests.post(
                url,
                data=data,
                auth=(self.twilio_account_sid, self.twilio_auth_token)
            )
            
            if response.status_code == 201:
                print(f"OTP SMS sent successfully to {phone_number}")
                return True
            else:
                print(f"SMS sending failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"SMS sending error: {e}")
            return self._mock_sms_send(phone_number, otp)

    async def send_whatsapp_message(self, phone_number: str, message: str) -> bool:
        """
        Send message via WhatsApp Business API
        """
        try:
            if not self.whatsapp_access_token or not self.whatsapp_phone_number_id:
                print("WhatsApp credentials not configured, using mock WhatsApp")
                return self._mock_whatsapp_send(phone_number, message)
            
            # Format phone number for India
            formatted_phone = f"91{phone_number}" if not phone_number.startswith('91') else phone_number
            
            url = f"https://graph.facebook.com/v17.0/{self.whatsapp_phone_number_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.whatsapp_access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": formatted_phone,
                "type": "text",
                "text": {"body": message}
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"WhatsApp message sent successfully to {phone_number}")
                return True
            else:
                print(f"WhatsApp sending failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"WhatsApp sending error: {e}")
            return self._mock_whatsapp_send(phone_number, message)

    async def send_farming_reminder(
        self, 
        user: User, 
        reminder_type: str, 
        message: str,
        scheduled_time: Optional[datetime] = None
    ) -> bool:
        """
        Send farming reminder to user
        """
        try:
            # Determine delivery method based on user preferences
            delivery_method = self._get_user_preferred_delivery_method(user)
            
            if delivery_method == "sms":
                success = await self.send_sms_otp(user.phone_number, message)
            elif delivery_method == "whatsapp":
                success = await self.send_whatsapp_message(user.phone_number, message)
            else:
                # Default to SMS
                success = await self.send_sms_otp(user.phone_number, message)
            
            return success
            
        except Exception as e:
            print(f"Farming reminder sending error: {e}")
            return False

    async def send_weather_alert(self, user: User, weather_data: Dict[str, Any]) -> bool:
        """
        Send weather alert to user
        """
        try:
            temperature = weather_data.get("temperature", 0)
            humidity = weather_data.get("humidity", 0)
            rainfall = weather_data.get("rainfall", 0)
            
            # Generate weather alert message
            if rainfall > 10:
                message = f"🌧️ भारी बारिश की चेतावनी! तापमान: {temperature}°C, आर्द्रता: {humidity}%। खेत की सुरक्षा के लिए उचित कदम उठाएं।"
            elif temperature > 35:
                message = f"🌡️ उच्च तापमान चेतावनी! तापमान: {temperature}°C। पौधों को अधिक पानी दें और छाया का प्रबंध करें।"
            elif humidity > 80:
                message = f"💧 उच्च आर्द्रता! आर्द्रता: {humidity}%। फंगल रोगों से सावधान रहें।"
            else:
                message = f"🌤️ मौसम अपडेट: तापमान {temperature}°C, आर्द्रता {humidity}%। खेती के लिए अनुकूल मौसम।"
            
            return await self.send_farming_reminder(user, "weather_alert", message)
            
        except Exception as e:
            print(f"Weather alert sending error: {e}")
            return False

    async def send_market_price_alert(
        self, 
        user: User, 
        crop_name: str, 
        price_data: Dict[str, Any]
    ) -> bool:
        """
        Send market price alert to user
        """
        try:
            min_price = price_data.get("min_price", 0)
            max_price = price_data.get("max_price", 0)
            market_name = price_data.get("market_name", "Local Market")
            
            message = f"💰 {crop_name} की कीमत अपडेट: {market_name} में ₹{min_price}-{max_price} प्रति क्विंटल। बेहतर मूल्य के लिए बाजार की जांच करें।"
            
            return await self.send_farming_reminder(user, "market_alert", message)
            
        except Exception as e:
            print(f"Market price alert sending error: {e}")
            return False

    async def send_pest_disease_alert(
        self, 
        user: User, 
        crop_name: str, 
        disease_name: str,
        severity: str
    ) -> bool:
        """
        Send pest/disease alert to user
        """
        try:
            severity_emoji = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"
            
            message = f"{severity_emoji} {crop_name} में {disease_name} की पहचान हुई है। तुरंत उपचार की आवश्यकता है। विशेषज्ञ सलाह लें।"
            
            return await self.send_farming_reminder(user, "disease_alert", message)
            
        except Exception as e:
            print(f"Pest/disease alert sending error: {e}")
            return False

    def _get_user_preferred_delivery_method(self, user: User) -> str:
        """
        Get user's preferred notification delivery method
        """
        try:
            if user.notification_preferences:
                import json
                preferences = json.loads(user.notification_preferences)
                return preferences.get("delivery_method", "sms")
        except:
            pass
        
        return "sms"  # Default to SMS

    def _mock_sms_send(self, phone_number: str, message: str) -> bool:
        """
        Mock SMS sending for development
        """
        print(f"📱 Mock SMS to {phone_number}: {message}")
        return True

    def _mock_whatsapp_send(self, phone_number: str, message: str) -> bool:
        """
        Mock WhatsApp sending for development
        """
        print(f"💬 Mock WhatsApp to {phone_number}: {message}")
        return True

    async def schedule_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        scheduled_time: datetime,
        delivery_method: str = "sms",
        db: Session = None
    ) -> Notification:
        """
        Schedule a notification for future delivery
        """
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                delivery_method=delivery_method,
                scheduled_at=scheduled_time,
                delivery_status="pending"
            )
            
            if db:
                db.add(notification)
                db.commit()
                db.refresh(notification)
            
            return notification
            
        except Exception as e:
            print(f"Notification scheduling error: {e}")
            raise e

    async def send_bulk_notifications(
        self,
        users: List[User],
        title: str,
        message: str,
        notification_type: str = "general"
    ) -> Dict[str, int]:
        """
        Send bulk notifications to multiple users
        """
        results = {"success": 0, "failed": 0}
        
        for user in users:
            try:
                success = await self.send_farming_reminder(user, notification_type, message)
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1
            except Exception as e:
                print(f"Bulk notification error for user {user.id}: {e}")
                results["failed"] += 1
        
        return results
