"""
Booking request and response schemas.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional, List
from decimal import Decimal


class PassengerInfo(BaseModel):
    """Passenger information schema."""
    first_name: str
    last_name: str
    passport_number: str
    date_of_birth: str  # Format: YYYY-MM-DD


class BookingCreate(BaseModel):
    """Create booking request schema."""
    flight_id: int
    passengers: List[PassengerInfo]


class Booking(BaseModel):
    """Booking response schema."""
    id: int
    user_id: int
    flight_id: int
    status: str
    total_price: float
    passenger_data: dict
    created_at: datetime

    class Config:
        from_attributes = True
