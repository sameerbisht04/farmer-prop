from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    auth,
    users,
    chatbot,
    simple_chatbot,
    crops,
    soil,
    weather,
    advisories,
    community,
    market,
    shops,
    notifications,
    image_classification
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(simple_chatbot.router, prefix="/simple-chatbot", tags=["simple-chatbot"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(soil.router, prefix="/soil", tags=["soil"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(advisories.router, prefix="/advisories", tags=["advisories"])
api_router.include_router(community.router, prefix="/community", tags=["community"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(image_classification.router, prefix="/image", tags=["image-classification"])
