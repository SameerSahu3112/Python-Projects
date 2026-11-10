"""
Apple Store — Pydantic Models (Request/Response Schemas)
Used for validating API inputs and structuring responses.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ─── Auth & Users ──────────────────────────────────────────────
class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str = Field(..., min_length=6, max_length=100)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


# ─── Address ───────────────────────────────────────────────────
class AddressCreate(BaseModel):
    label: str = Field("Home", max_length=50)
    address_line1: str = Field(..., max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=10)
    country: str = Field("India", max_length=50)
    is_default: bool = False


# ─── Cart ──────────────────────────────────────────────────────
class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1, le=10)


class CartUpdate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=0, le=10)


# ─── Coupon ────────────────────────────────────────────────────
class CouponApply(BaseModel):
    code: str = Field(..., min_length=1, max_length=30)


# ─── Order ─────────────────────────────────────────────────────
class PaymentMethod(str, Enum):
    COD = "COD"
    UPI = "UPI"
    Card = "Card"
    NetBanking = "Net Banking"


class OrderCreate(BaseModel):
    address_id: Optional[int] = None
    new_address: Optional[AddressCreate] = None
    payment_method: str = "COD"
    coupon_code: Optional[str] = None
    notes: Optional[str] = None


# ─── Review ────────────────────────────────────────────────────
class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    review_text: Optional[str] = None


# ─── Product (for admin) ──────────────────────────────────────
class ProductCreate(BaseModel):
    category_id: int
    product_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    mrp: Optional[float] = None
    stock_quantity: int = Field(0, ge=0)
    color: Optional[str] = None
    is_featured: bool = False
