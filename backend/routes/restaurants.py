"""
Restaurant routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Restaurant, Category
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


class RestaurantResponse(BaseModel):
    """Restaurant response schema"""
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    address: str
    phone: str
    rating: float
    delivery_time: Optional[str]
    delivery_fee: float
    is_active: bool
    category_id: Optional[int]
    
    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    """Restaurant creation schema"""
    name: str
    description: Optional[str]
    image_url: Optional[str]
    address: str
    phone: str
    delivery_time: Optional[str]
    delivery_fee: float
    category_id: Optional[int]


@router.get("", response_model=List[RestaurantResponse])
async def get_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all restaurants with optional filters
    """
    query = db.query(Restaurant).filter(Restaurant.is_active == True)
    
    if category_id:
        query = query.filter(Restaurant.category_id == category_id)
    
    if min_rating:
        query = query.filter(Restaurant.rating >= min_rating)
    
    if search:
        query = query.filter(Restaurant.name.ilike(f"%{search}%"))
    
    restaurants = query.offset(skip).limit(limit).all()
    return restaurants


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Get restaurant by ID
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return restaurant


@router.post("", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new restaurant (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_restaurant = Restaurant(**restaurant_data.dict())
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    
    return new_restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update restaurant (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    for key, value in restaurant_data.dict().items():
        setattr(restaurant, key, value)
    
    db.commit()
    db.refresh(restaurant)
    
    return restaurant


@router.delete("/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete restaurant (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(restaurant)
    db.commit()
    
    return {"message": "Restaurant deleted successfully"}
