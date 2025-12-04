"""
Booking routes for creating and managing bookings.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Path
from typing import List

from src.schemas.booking_schema import Booking, BookingCreate
from src.schemas.auth_schema import User
from src.services.booking_service import BookingService
from src.routes.auth import get_current_active_user


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new booking (requires authentication).
    
    Args:
        booking_data: Booking creation data
        current_user: Current authenticated user
        
    Returns:
        Created booking object
        
    Raises:
        HTTPException: If booking creation fails
    """
    try:
        booking = BookingService.create_booking(booking_data, current_user.email)
        return booking
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking creation failed: {str(e)}"
        )


@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: str = Path(..., description="Booking ID"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get booking details by ID (requires authentication).
    
    Args:
        booking_id: Booking identifier
        current_user: Current authenticated user
        
    Returns:
        Booking object
        
    Raises:
        HTTPException: If booking not found
    """
    try:
        booking = BookingService.get_booking(booking_id, current_user.email)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve booking: {str(e)}"
        )


@router.patch("/{booking_id}/cancel", response_model=Booking)
async def cancel_booking(
    booking_id: str = Path(..., description="Booking ID"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Cancel a booking (requires authentication).
    
    Args:
        booking_id: Booking identifier
        current_user: Current authenticated user
        
    Returns:
        Cancelled booking object
        
    Raises:
        HTTPException: If booking not found or cancellation fails
    """
    try:
        booking = BookingService.cancel_booking(booking_id, current_user.email)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking cancellation failed: {str(e)}"
        )
