"""
Address routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from database import get_db
from models import Address, User
from auth.dependencies import get_current_user

router = APIRouter(prefix="/api/addresses", tags=["Addresses"])


class AddressResponse(BaseModel):
    """Address response schema"""
    id: int
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    is_default: bool
    
    class Config:
        from_attributes = True


class AddressCreate(BaseModel):
    """Address creation schema"""
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    is_default: bool = False


@router.get("", response_model=List[AddressResponse])
async def get_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's addresses
    """
    addresses = db.query(Address).filter(
        Address.user_id == current_user.id
    ).order_by(Address.is_default.desc()).all()
    
    return addresses


@router.post("", response_model=AddressResponse, status_code=201)
async def create_address(
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new address
    """
    # If setting as default, remove default from other addresses
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.is_default == True
        ).update({"is_default": False})
    
    new_address = Address(
        user_id=current_user.id,
        **address_data.dict()
    )
    
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    
    return new_address


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update address
    """
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    # If setting as default, remove default from other addresses
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.id != address_id,
            Address.is_default == True
        ).update({"is_default": False})
    
    for key, value in address_data.dict().items():
        setattr(address, key, value)
    
    db.commit()
    db.refresh(address)
    
    return address


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete address
    """
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(address)
    db.commit()
    
    return {"message": "Address deleted successfully"}
