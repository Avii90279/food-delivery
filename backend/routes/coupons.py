"""
Coupon routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Coupon
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])


class CouponResponse(BaseModel):
    """Coupon response schema"""
    id: int
    code: str
    description: Optional[str]
    discount_type: str
    discount_value: float
    min_order_amount: float
    max_discount_amount: Optional[float]
    is_active: bool
    
    class Config:
        from_attributes = True


class CouponCreate(BaseModel):
    """Coupon creation schema"""
    code: str
    description: Optional[str]
    discount_type: str
    discount_value: float
    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None


@router.get("", response_model=List[CouponResponse])
async def get_coupons(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all active coupons
    """
    coupons = db.query(Coupon).filter(Coupon.is_active == True).all()
    return coupons


@router.post("/validate")
async def validate_coupon(
    code: str,
    order_amount: float,
    db: Session = Depends(get_db)
):
    """
    Validate a coupon code
    """
    coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.is_active == True
    ).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid coupon code")
    
    if order_amount < coupon.min_order_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Minimum order amount of {coupon.min_order_amount} required"
        )
    
    # Calculate discount
    if coupon.discount_type == "percentage":
        discount = order_amount * (coupon.discount_value / 100)
        if coupon.max_discount_amount:
            discount = min(discount, coupon.max_discount_amount)
    else:
        discount = coupon.discount_value
    
    return {
        "valid": True,
        "discount": discount,
        "discount_type": coupon.discount_type,
        "discount_value": coupon.discount_value
    }


@router.post("", response_model=CouponResponse, status_code=201)
async def create_coupon(
    coupon_data: CouponCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new coupon (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if coupon code already exists
    existing_coupon = db.query(Coupon).filter(Coupon.code == coupon_data.code).first()
    if existing_coupon:
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    
    new_coupon = Coupon(**coupon_data.dict())
    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    
    return new_coupon


@router.delete("/{coupon_id}")
async def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete coupon (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    db.delete(coupon)
    db.commit()
    
    return {"message": "Coupon deleted successfully"}
