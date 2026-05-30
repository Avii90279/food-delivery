"""
Order routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database import get_db
from models import Order, OrderItem, Cart, CartItem, Food, Address, User, Coupon
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/orders", tags=["Orders"])


class OrderItemResponse(BaseModel):
    """Order item response schema"""
    id: int
    food_id: int
    food_name: str
    food_image: Optional[str]
    quantity: int
    price: float
    total_price: float
    restaurant_name: str
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema"""
    id: int
    user_id: int
    total_amount: float
    delivery_fee: float
    gst_amount: float
    discount_amount: float
    final_amount: float
    status: str
    payment_method: str
    coupon_code: Optional[str]
    created_at: datetime
    items: List[OrderItemResponse]
    delivery_address: str
    
    class Config:
        from_attributes = True


class CreateOrderRequest(BaseModel):
    """Create order request schema"""
    address_id: int
    payment_method: str
    coupon_code: Optional[str] = None


@router.get("", response_model=List[OrderResponse])
async def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's orders
    """
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        items = []
        for item in order.items:
            food = db.query(Food).filter(Food.id == item.food_id).first()
            items.append(OrderItemResponse(
                id=item.id,
                food_id=item.food_id,
                food_name=food.name if food else "Unknown",
                food_image=food.image_url if food else None,
                quantity=item.quantity,
                price=item.price,
                total_price=item.total_price,
                restaurant_name=item.restaurant.name if item.restaurant else "Unknown"
            ))
        
        address = db.query(Address).filter(Address.id == order.address_id).first()
        delivery_address = f"{address.address_line1}, {address.city}" if address else ""
        
        result.append(OrderResponse(
            id=order.id,
            user_id=order.user_id,
            total_amount=order.total_amount,
            delivery_fee=order.delivery_fee,
            gst_amount=order.gst_amount,
            discount_amount=order.discount_amount,
            final_amount=order.final_amount,
            status=order.status.value,
            payment_method=order.payment_method,
            coupon_code=order.coupon_code,
            created_at=order.created_at,
            items=items,
            delivery_address=delivery_address
        ))
    
    return result


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get order by ID
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = []
    for item in order.items:
        food = db.query(Food).filter(Food.id == item.food_id).first()
        items.append(OrderItemResponse(
            id=item.id,
            food_id=item.food_id,
            food_name=food.name if food else "Unknown",
            food_image=food.image_url if food else None,
            quantity=item.quantity,
            price=item.price,
            total_price=item.total_price,
            restaurant_name=item.restaurant.name if item.restaurant else "Unknown"
        ))
    
    address = db.query(Address).filter(Address.id == order.address_id).first()
    delivery_address = f"{address.address_line1}, {address.city}" if address else ""
    
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        delivery_fee=order.delivery_fee,
        gst_amount=order.gst_amount,
        discount_amount=order.discount_amount,
        final_amount=order.final_amount,
        status=order.status.value,
        payment_method=order.payment_method,
        coupon_code=order.coupon_code,
        created_at=order.created_at,
        items=items,
        delivery_address=delivery_address
    )


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new order
    """
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Get address
    address = db.query(Address).filter(
        Address.id == request.address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # Calculate order totals
    total_amount = 0
    delivery_fee = 40  # Default delivery fee
    gst_rate = 0.05  # 5% GST
    discount_amount = 0
    
    for cart_item in cart.items:
        food = db.query(Food).filter(Food.id == cart_item.food_id).first()
        if food:
            total_amount += food.price * cart_item.quantity
    
    # Apply coupon if provided
    if request.coupon_code:
        coupon = db.query(Coupon).filter(
            Coupon.code == request.coupon_code,
            Coupon.is_active == True
        ).first()
        
        if coupon:
            if total_amount >= coupon.min_order_amount:
                if coupon.discount_type == "percentage":
                    discount = total_amount * (coupon.discount_value / 100)
                    if coupon.max_discount_amount:
                        discount = min(discount, coupon.max_discount_amount)
                    discount_amount = discount
                else:  # flat discount
                    discount_amount = coupon.discount_value
    
    gst_amount = (total_amount - discount_amount) * gst_rate
    final_amount = total_amount + delivery_fee + gst_amount - discount_amount
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        address_id=request.address_id,
        total_amount=total_amount,
        delivery_fee=delivery_fee,
        gst_amount=gst_amount,
        discount_amount=discount_amount,
        final_amount=final_amount,
        payment_method=request.payment_method,
        coupon_code=request.coupon_code
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Create order items
    for cart_item in cart.items:
        food = db.query(Food).filter(Food.id == cart_item.food_id).first()
        if food:
            order_item = OrderItem(
                order_id=new_order.id,
                food_id=cart_item.food_id,
                restaurant_id=food.restaurant_id,
                quantity=cart_item.quantity,
                price=food.price,
                total_price=food.price * cart_item.quantity
            )
            db.add(order_item)
    
    db.commit()
    
    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    # Return the created order
    return await get_order(new_order.id, db, current_user)


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update order status (admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    order.status = status
    db.commit()
    
    return {"message": "Order status updated successfully"}
