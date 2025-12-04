"""
Booking request and response schemas.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional


class BookingCreate(BaseModel):
    """Create booking request schema."""
    booking_type: Literal["flight", "hotel"]
    item_id: str  # flight_id or hotel_id
    passengers: Optional[int] = 1
    special_requests: Optional[str] = None


class Booking(BaseModel):
    """Booking response schema."""
    booking_id: str
    user_email: str
    booking_type: Literal["flight", "hotel"]
    item_id: str
    status: Literal["pending", "confirmed", "cancelled"]
    passengers: int
    special_requests: Optional[str] = None
    total_price: float
    currency: str = "USD"
    created_at: datetime
    updated_at: datetime


class BookingUpdate(BaseModel):
    """Update booking request schema."""
    status: Optional[Literal["confirmed", "cancelled"]] = None
    special_requests: Optional[str] = None


class PaymentRequest(BaseModel):
    """Mock payment request schema."""
    booking_id: str
    payment_method: str
    amount: float
