"""
User profile routes.
"""

from fastapi import APIRouter, Depends
from typing import List

from src.schemas.auth_schema import User
from src.schemas.booking_schema import Booking
from src.services.booking_service import BookingService
from src.routes.auth import get_current_active_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
async def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile (requires authentication).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User profile object
    """
    return current_user


@router.get("/me/bookings", response_model=List[Booking])
async def get_user_bookings(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's booking history (requires authentication).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of user's bookings
    """
    bookings = BookingService.get_user_bookings(current_user.email)
    return bookings
