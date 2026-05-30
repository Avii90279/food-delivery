"""
Cart routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Cart, CartItem, Food, User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


class CartItemResponse(BaseModel):
    """Cart item response schema"""
    id: int
    food_id: int
    quantity: int
    food_name: str
    food_price: float
    food_image: Optional[str]
    restaurant_id: int
    restaurant_name: str
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Cart response schema"""
    id: int
    items: List[CartItemResponse]
    total_amount: float
    item_count: int


class AddToCartRequest(BaseModel):
    """Add to cart request schema"""
    food_id: int
    quantity: int = 1


class UpdateCartItemRequest(BaseModel):
    """Update cart item request schema"""
    quantity: int


@router.get("", response_model=CartResponse)
async def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's cart
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    items = []
    total_amount = 0
    item_count = 0
    
    for item in cart.items:
        food = db.query(Food).filter(Food.id == item.food_id).first()
        if food and food.is_available:
            items.append(CartItemResponse(
                id=item.id,
                food_id=item.food_id,
                quantity=item.quantity,
                food_name=food.name,
                food_price=food.price,
                food_image=food.image_url,
                restaurant_id=food.restaurant_id,
                restaurant_name=food.restaurant.name if food.restaurant else ""
            ))
            total_amount += food.price * item.quantity
            item_count += item.quantity
    
    return CartResponse(
        id=cart.id,
        items=items,
        total_amount=total_amount,
        item_count=item_count
    )


@router.post("/add", response_model=CartResponse)
async def add_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add item to cart
    """
    food = db.query(Food).filter(Food.id == request.food_id).first()
    
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    if not food.is_available:
        raise HTTPException(status_code=400, detail="Food is not available")
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.food_id == request.food_id
    ).first()
    
    if existing_item:
        existing_item.quantity += request.quantity
    else:
        new_item = CartItem(
            cart_id=cart.id,
            food_id=request.food_id,
            quantity=request.quantity
        )
        db.add(new_item)
    
    db.commit()
    db.refresh(cart)
    
    # Return updated cart
    return await get_cart(db, current_user)


@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update cart item quantity
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if request.quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = request.quantity
    
    db.commit()
    
    return await get_cart(db, current_user)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove item from cart
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    
    return await get_cart(db, current_user)


@router.delete("", response_model=CartResponse)
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Clear all items from cart
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    return await get_cart(db, current_user)
