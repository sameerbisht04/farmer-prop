from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.market import MarketPrice, MarketInsight

router = APIRouter()


@router.get("/prices")
async def get_market_prices(
    crop_name: Optional[str] = None,
    market_name: Optional[str] = None,
    state: Optional[str] = None,
    district: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get market prices for crops
    """
    try:
        query = db.query(MarketPrice)
        
        if crop_name:
            query = query.filter(MarketPrice.crop_name.ilike(f"%{crop_name}%"))
        
        if market_name:
            query = query.filter(MarketPrice.market_name.ilike(f"%{market_name}%"))
        
        if state:
            query = query.filter(MarketPrice.state == state)
        
        if district:
            query = query.filter(MarketPrice.district == district)
        
        prices = query.order_by(MarketPrice.price_date.desc()).offset(offset).limit(limit).all()
        
        return {
            "prices": [
                {
                    "id": price.id,
                    "crop_name": price.crop_name,
                    "variety": price.variety,
                    "market_name": price.market_name,
                    "state": price.state,
                    "district": price.district,
                    "min_price": price.min_price,
                    "max_price": price.max_price,
                    "modal_price": price.modal_price,
                    "arrival_quantity": price.arrival_quantity,
                    "quality_grade": price.quality_grade,
                    "source": price.source,
                    "price_date": price.price_date
                }
                for price in prices
            ],
            "total": len(prices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market prices: {str(e)}")


@router.get("/price-history/{crop_name}")
async def get_price_history(
    crop_name: str,
    days: int = 30,
    market_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get price history for a specific crop
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(MarketPrice).filter(
            MarketPrice.crop_name.ilike(f"%{crop_name}%"),
            MarketPrice.price_date >= start_date
        )
        
        if market_name:
            query = query.filter(MarketPrice.market_name.ilike(f"%{market_name}%"))
        
        prices = query.order_by(MarketPrice.price_date.asc()).all()
        
        # Group by date and calculate average prices
        price_history = {}
        for price in prices:
            date_key = price.price_date.date().isoformat()
            if date_key not in price_history:
                price_history[date_key] = {
                    "date": date_key,
                    "prices": [],
                    "avg_min": 0,
                    "avg_max": 0,
                    "avg_modal": 0
                }
            price_history[date_key]["prices"].append(price)
        
        # Calculate averages
        for date_key, data in price_history.items():
            prices_list = data["prices"]
            data["avg_min"] = sum(p.min_price for p in prices_list) / len(prices_list)
            data["avg_max"] = sum(p.max_price for p in prices_list) / len(prices_list)
            data["avg_modal"] = sum(p.modal_price for p in prices_list if p.modal_price) / len([p for p in prices_list if p.modal_price])
            del data["prices"]  # Remove raw prices from response
        
        return {
            "crop_name": crop_name,
            "days": days,
            "market_name": market_name,
            "price_history": list(price_history.values())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching price history: {str(e)}")


@router.get("/insights")
async def get_market_insights(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get market insights and analysis
    """
    try:
        insights = db.query(MarketInsight).order_by(
            MarketInsight.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "insights": [
                {
                    "id": insight.id,
                    "title": insight.title,
                    "content": insight.content,
                    "insight_type": insight.insight_type,
                    "crop_name": insight.crop_name,
                    "region": insight.region,
                    "trend_direction": insight.trend_direction,
                    "confidence_level": insight.confidence_level,
                    "time_horizon": insight.time_horizon,
                    "is_ai_generated": insight.is_ai_generated,
                    "model_version": insight.model_version,
                    "language": insight.language,
                    "created_at": insight.created_at
                }
                for insight in insights
            ],
            "total": len(insights)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market insights: {str(e)}")


@router.post("/price-alerts")
async def set_price_alert(
    crop_name: str,
    target_price: float,
    alert_type: str,  # "above" or "below"
    market_name: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set a price alert for a crop
    """
    try:
        # This would typically create a price alert record
        # For now, we'll just return a success message
        
        return {
            "message": "Price alert set successfully",
            "crop_name": crop_name,
            "target_price": target_price,
            "alert_type": alert_type,
            "market_name": market_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting price alert: {str(e)}")


@router.get("/trends")
async def get_market_trends(
    crop_name: Optional[str] = None,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get market trends for crops
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.query(MarketPrice).filter(
            MarketPrice.price_date >= start_date
        )
        
        if crop_name:
            query = query.filter(MarketPrice.crop_name.ilike(f"%{crop_name}%"))
        
        prices = query.order_by(MarketPrice.price_date.desc()).all()
        
        # Calculate trends
        trends = {}
        for price in prices:
            if price.crop_name not in trends:
                trends[price.crop_name] = {
                    "crop_name": price.crop_name,
                    "current_price": price.modal_price or ((price.min_price + price.max_price) / 2),
                    "price_change": 0,
                    "trend": "stable",
                    "markets": []
                }
            
            trends[price.crop_name]["markets"].append({
                "market_name": price.market_name,
                "price": price.modal_price or ((price.min_price + price.max_price) / 2),
                "date": price.price_date
            })
        
        return {
            "trends": list(trends.values()),
            "period_days": days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market trends: {str(e)}")


@router.get("/markets")
async def get_available_markets(
    state: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of available markets
    """
    try:
        query = db.query(MarketPrice.market_name, MarketPrice.state, MarketPrice.district).distinct()
        
        if state:
            query = query.filter(MarketPrice.state == state)
        
        if district:
            query = query.filter(MarketPrice.district == district)
        
        markets = query.all()
        
        return {
            "markets": [
                {
                    "market_name": market.market_name,
                    "state": market.state,
                    "district": market.district
                }
                for market in markets
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching markets: {str(e)}")
