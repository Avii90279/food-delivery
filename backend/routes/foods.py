"""
Food routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Food, Restaurant
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/foods", tags=["Foods"])


class FoodResponse(BaseModel):
    """Food response schema"""
    id: int
    name: str
    description: Optional[str]
    image_url: Optional[str]
    price: float
    is_vegetarian: bool
    is_available: bool
    restaurant_id: int
    category_id: Optional[int]
    
    class Config:
        from_attributes = True


class FoodCreate(BaseModel):
    """Food creation schema"""
    name: str
    description: Optional[str]
    image_url: Optional[str]
    price: float
    is_vegetarian: bool
    is_available: bool
    restaurant_id: int
    category_id: Optional[int]


@router.get("", response_model=List[FoodResponse])
async def get_foods(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    restaurant_id: Optional[int] = None,
    category_id: Optional[int] = None,
    vegetarian: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all foods with optional filters
    """
    query = db.query(Food).filter(Food.is_available == True)
    
    if restaurant_id:
        query = query.filter(Food.restaurant_id == restaurant_id)
    
    if category_id:
        query = query.filter(Food.category_id == category_id)
    
    if vegetarian is not None:
        query = query.filter(Food.is_vegetarian == vegetarian)
    
    if search:
        query = query.filter(Food.name.ilike(f"%{search}%"))
    
    foods = query.offset(skip).limit(limit).all()
    return foods


@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(food_id: int, db: Session = Depends(get_db)):
    """
    Get food by ID
    """
    food = db.query(Food).filter(Food.id == food_id).first()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    return food


@router.post("", response_model=FoodResponse, status_code=201)
async def create_food(
    food_data: FoodCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new food item (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == food_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    new_food = Food(**food_data.dict())
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    
    return new_food


@router.put("/{food_id}", response_model=FoodResponse)
async def update_food(
    food_id: int,
    food_data: FoodCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update food item (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    food = db.query(Food).filter(Food.id == food_id).first()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    for key, value in food_data.dict().items():
        setattr(food, key, value)
    
    db.commit()
    db.refresh(food)
    
    return food


@router.delete("/{food_id}")
async def delete_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete food item (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    food = db.query(Food).filter(Food.id == food_id).first()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    db.delete(food)
    db.commit()
    
    return {"message": "Food deleted successfully"}
