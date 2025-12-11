"""
Booking routes for creating and managing bookings.
"""

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session

from src.schemas.booking_schema import Booking, BookingCreate
from src.schemas.auth_schema import User
from src.services.booking_service import BookingService
from src.dependencies import get_db, get_current_user


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new booking (requires authentication).
    
    Args:
        booking_data: Booking creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Created booking object
        
    Raises:
        HTTPException: If booking creation fails
    """
    try:
        booking = BookingService.create_booking(db, booking_data, current_user.id)
        return booking
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking creation failed: {str(e)}"
        ) from e


@router.get("/{booking_id}", response_model=Booking)
async def get_booking(
    booking_id: int = Path(..., description="Booking ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get booking details by ID (requires authentication).
    
    Args:
        booking_id: Booking identifier
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Booking object
        
    Raises:
        HTTPException: If booking not found
    """
    try:
        booking = BookingService.get_booking(db, booking_id, current_user.id)
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
        ) from e


@router.delete("/{booking_id}", response_model=Booking)
async def cancel_booking(
    booking_id: int = Path(..., description="Booking ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a booking (requires authentication).
    
    Args:
        booking_id: Booking identifier
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Cancelled booking object
        
    Raises:
        HTTPException: If booking not found or cancellation fails
    """
    try:
        booking = BookingService.cancel_booking(db, booking_id, current_user.id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        return booking
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Booking cancellation failed: {str(e)}"
        ) from e

