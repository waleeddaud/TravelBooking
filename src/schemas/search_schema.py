"""
Search request and response schemas for flights and hotels.
"""

from pydantic import BaseModel
from datetime import date
from typing import Optional


class FlightSearchParams(BaseModel):
    """Flight search query parameters."""
    origin: str
    destination: str
    departure_date: Optional[date] = None
    return_date: Optional[date] = None
    passengers: int = 1


class Flight(BaseModel):
    """Flight search result schema."""
    flight_id: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    price: float
    currency: str = "USD"
    available_seats: int


class HotelSearchParams(BaseModel):
    """Hotel search query parameters."""
    city: str
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    guests: int = 1


class Hotel(BaseModel):
    """Hotel search result schema."""
    hotel_id: str
    name: str
    city: str
    address: str
    rating: float
    price_per_night: float
    currency: str = "USD"
    available_rooms: int
