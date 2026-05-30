"""
Review routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Review, User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


class ReviewResponse(BaseModel):
    """Review response schema"""
    id: int
    user_id: int
    username: str
    restaurant_id: Optional[int]
    food_id: Optional[int]
    rating: int
    comment: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True


class CreateReviewRequest(BaseModel):
    """Create review request schema"""
    restaurant_id: Optional[int] = None
    food_id: Optional[int] = None
    rating: int
    comment: Optional[str] = None


@router.get("", response_model=List[ReviewResponse])
async def get_reviews(
    restaurant_id: Optional[int] = None,
    food_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get reviews with optional filters
    """
    query = db.query(Review)
    
    if restaurant_id:
        query = query.filter(Review.restaurant_id == restaurant_id)
    
    if food_id:
        query = query.filter(Review.food_id == food_id)
    
    reviews = query.order_by(Review.created_at.desc()).all()
    
    result = []
    for review in reviews:
        result.append(ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            username=review.user.username if review.user else "Unknown",
            restaurant_id=review.restaurant_id,
            food_id=review.food_id,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at.isoformat()
        ))
    
    return result


@router.post("", response_model=ReviewResponse, status_code=201)
async def create_review(
    request: CreateReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new review
    """
    if not request.restaurant_id and not request.food_id:
        raise HTTPException(status_code=400, detail="Either restaurant_id or food_id must be provided")
    
    if request.rating < 1 or request.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Check if user already reviewed this item
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.restaurant_id == request.restaurant_id,
        Review.food_id == request.food_id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this item")
    
    new_review = Review(
        user_id=current_user.id,
        restaurant_id=request.restaurant_id,
        food_id=request.food_id,
        rating=request.rating,
        comment=request.comment
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return ReviewResponse(
        id=new_review.id,
        user_id=new_review.user_id,
        username=current_user.username,
        restaurant_id=new_review.restaurant_id,
        food_id=new_review.food_id,
        rating=new_review.rating,
        comment=new_review.comment,
        created_at=new_review.created_at.isoformat()
    )
