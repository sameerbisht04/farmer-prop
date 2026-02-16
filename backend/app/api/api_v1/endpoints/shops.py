from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.shop import Shop, ShopInventory

router = APIRouter()


@router.get("/")
async def get_shops(
    shop_type: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    is_government_approved: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get list of shops
    """
    try:
        query = db.query(Shop).filter(Shop.is_active == True)
        
        if shop_type:
            query = query.filter(Shop.shop_type == shop_type)
        
        if state:
            query = query.filter(Shop.state == state)
        
        if district:
            query = query.filter(Shop.district == district)
        
        if is_government_approved is not None:
            query = query.filter(Shop.is_government_approved == is_government_approved)
        
        shops = query.offset(offset).limit(limit).all()
        
        return {
            "shops": [
                {
                    "id": shop.id,
                    "name": shop.name,
                    "shop_type": shop.shop_type,
                    "phone_number": shop.phone_number,
                    "email": shop.email,
                    "contact_person": shop.contact_person,
                    "address": shop.address,
                    "state": shop.state,
                    "district": shop.district,
                    "village": shop.village,
                    "pincode": shop.pincode,
                    "latitude": shop.latitude,
                    "longitude": shop.longitude,
                    "license_number": shop.license_number,
                    "is_verified": shop.is_verified,
                    "is_government_approved": shop.is_government_approved,
                    "services": shop.services,
                    "payment_methods": shop.payment_methods,
                    "operating_hours": shop.operating_hours,
                    "average_rating": shop.average_rating,
                    "total_reviews": shop.total_reviews
                }
                for shop in shops
            ],
            "total": len(shops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shops: {str(e)}")


@router.get("/{shop_id}")
async def get_shop_details(
    shop_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific shop
    """
    try:
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        return {
            "id": shop.id,
            "name": shop.name,
            "shop_type": shop.shop_type,
            "phone_number": shop.phone_number,
            "email": shop.email,
            "contact_person": shop.contact_person,
            "address": shop.address,
            "state": shop.state,
            "district": shop.district,
            "village": shop.village,
            "pincode": shop.pincode,
            "latitude": shop.latitude,
            "longitude": shop.longitude,
            "license_number": shop.license_number,
            "is_verified": shop.is_verified,
            "is_government_approved": shop.is_government_approved,
            "services": shop.services,
            "payment_methods": shop.payment_methods,
            "operating_hours": shop.operating_hours,
            "average_rating": shop.average_rating,
            "total_reviews": shop.total_reviews
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shop details: {str(e)}")


@router.get("/{shop_id}/inventory")
async def get_shop_inventory(
    shop_id: int,
    product_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get inventory for a specific shop
    """
    try:
        # Check if shop exists
        shop = db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            raise HTTPException(status_code=404, detail="Shop not found")
        
        query = db.query(ShopInventory).filter(ShopInventory.shop_id == shop_id)
        
        if product_type:
            query = query.filter(ShopInventory.product_type == product_type)
        
        if search:
            query = query.filter(ShopInventory.product_name.ilike(f"%{search}%"))
        
        inventory = query.offset(offset).limit(limit).all()
        
        return {
            "shop_id": shop_id,
            "shop_name": shop.name,
            "inventory": [
                {
                    "id": item.id,
                    "product_name": item.product_name,
                    "product_type": item.product_type,
                    "brand": item.brand,
                    "variety": item.variety,
                    "description": item.description,
                    "specifications": item.specifications,
                    "price_per_unit": item.price_per_unit,
                    "unit": item.unit,
                    "discount_percentage": item.discount_percentage,
                    "current_stock": item.current_stock,
                    "minimum_stock": item.minimum_stock,
                    "is_available": item.is_available,
                    "is_organic": item.is_organic,
                    "is_government_subsidized": item.is_government_subsidized,
                    "quality_grade": item.quality_grade,
                    "expiry_date": item.expiry_date
                }
                for item in inventory
            ],
            "total": len(inventory)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching shop inventory: {str(e)}")


@router.get("/search-products")
async def search_products(
    q: str,
    product_type: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Search for products across all shops
    """
    try:
        query = db.query(ShopInventory).join(Shop).filter(
            ShopInventory.product_name.ilike(f"%{q}%"),
            ShopInventory.is_available == True,
            Shop.is_active == True
        )
        
        if product_type:
            query = query.filter(ShopInventory.product_type == product_type)
        
        if state:
            query = query.filter(Shop.state == state)
        
        if district:
            query = query.filter(Shop.district == district)
        
        products = query.offset(offset).limit(limit).all()
        
        return {
            "products": [
                {
                    "id": product.id,
                    "product_name": product.product_name,
                    "product_type": product.product_type,
                    "brand": product.brand,
                    "variety": product.variety,
                    "price_per_unit": product.price_per_unit,
                    "unit": product.unit,
                    "discount_percentage": product.discount_percentage,
                    "is_organic": product.is_organic,
                    "is_government_subsidized": product.is_government_subsidized,
                    "shop": {
                        "id": product.shop.id,
                        "name": product.shop.name,
                        "shop_type": product.shop.shop_type,
                        "address": product.shop.address,
                        "state": product.shop.state,
                        "district": product.shop.district,
                        "phone_number": product.shop.phone_number,
                        "is_government_approved": product.shop.is_government_approved
                    }
                }
                for product in products
            ],
            "total": len(products),
            "search_query": q
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")


@router.get("/nearby")
async def get_nearby_shops(
    latitude: float,
    longitude: float,
    radius_km: float = 10.0,
    shop_type: Optional[str] = None,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get shops near a specific location
    """
    try:
        # This is a simplified version - in production, you'd use proper geospatial queries
        shops = db.query(Shop).filter(
            Shop.is_active == True,
            Shop.latitude.isnot(None),
            Shop.longitude.isnot(None)
        ).all()
        
        if shop_type:
            shops = [shop for shop in shops if shop.shop_type == shop_type]
        
        # Calculate distances (simplified)
        nearby_shops = []
        for shop in shops:
            if shop.latitude and shop.longitude:
                # Simple distance calculation (not accurate for large distances)
                distance = ((shop.latitude - latitude) ** 2 + (shop.longitude - longitude) ** 2) ** 0.5 * 111  # Rough km conversion
                if distance <= radius_km:
                    nearby_shops.append({
                        "shop": {
                            "id": shop.id,
                            "name": shop.name,
                            "shop_type": shop.shop_type,
                            "address": shop.address,
                            "state": shop.state,
                            "district": shop.district,
                            "phone_number": shop.phone_number,
                            "is_government_approved": shop.is_government_approved
                        },
                        "distance_km": round(distance, 2)
                    })
        
        # Sort by distance
        nearby_shops.sort(key=lambda x: x["distance_km"])
        
        return {
            "nearby_shops": nearby_shops[:limit],
            "center_latitude": latitude,
            "center_longitude": longitude,
            "radius_km": radius_km,
            "total_found": len(nearby_shops)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching nearby shops: {str(e)}")
