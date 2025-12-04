"""
Booking service for managing flight bookings with database integration.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
import json

from src.repositories.booking_repo import BookingRepository
from src.schemas.booking_schema import Booking, BookingCreate
from src.services.search_service import SearchService


class BookingService:
    """Service for managing bookings with database."""
    
    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate, user_id: int) -> Booking:
        """
        Create a new booking.
        
        Args:
            db: Database session
            booking_data: Booking creation data
            user_id: ID of the user creating the booking
            
        Returns:
            Created booking object
            
        Raises:
            ValueError: If flight not found or unavailable
        """
        # Validate flight exists
        flight = SearchService.get_flight_by_id(db, booking_data.flight_id)
        if not flight:
            raise ValueError(f"Flight {booking_data.flight_id} not found")
        if flight.available_seats < len(booking_data.passengers):
            raise ValueError("Not enough available seats")
        
        # Calculate total price
        total_price = Decimal(str(flight.price)) * len(booking_data.passengers)
        
        # Convert passenger list to dict for JSON storage
        passenger_data = {
            "passengers": [p.model_dump() for p in booking_data.passengers],
            "flight_info": {
                "flight_id": flight.flight_id,
                "airline": flight.airline,
                "origin": flight.origin,
                "destination": flight.destination
            }
        }
        
        # Create booking
        booking_repo = BookingRepository(db)
        db_booking = booking_repo.create(
            user_id=user_id,
            flight_id=booking_data.flight_id,
            total_price=total_price,
            passenger_data=passenger_data
        )
        
        db.commit()
        db.refresh(db_booking)
        
        return Booking.model_validate(db_booking)
    
    @staticmethod
    def get_booking(db: Session, booking_id: int, user_id: int) -> Optional[Booking]:
        """
        Get a booking by ID.
        
        Args:
            db: Database session
            booking_id: Booking identifier
            user_id: ID of the requesting user
            
        Returns:
            Booking object if found and belongs to user, None otherwise
        """
        booking_repo = BookingRepository(db)
        db_booking = booking_repo.get_by_id(booking_id)
        
        if not db_booking or db_booking.user_id != user_id:
            return None
        
        return Booking.model_validate(db_booking)
    
    @staticmethod
    def get_user_bookings(db: Session, user_id: int) -> List[Booking]:
        """
        Get all bookings for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of booking objects
        """
        booking_repo = BookingRepository(db)
        db_bookings = booking_repo.get_user_bookings(user_id)
        
        return [Booking.model_validate(b) for b in db_bookings]
    
    @staticmethod
    def cancel_booking(db: Session, booking_id: int, user_id: int) -> Optional[Booking]:
        """
        Cancel a booking.
        
        Args:
            db: Database session
            booking_id: Booking identifier
            user_id: ID of the user cancelling
            
        Returns:
            Updated booking object or None if not found
            
        Raises:
            ValueError: If booking already cancelled
        """
        booking_repo = BookingRepository(db)
        db_booking = booking_repo.get_by_id(booking_id)
        
        if not db_booking or db_booking.user_id != user_id:
            return None
        
        if db_booking.status == "CANCELLED":
            raise ValueError("Booking already cancelled")
        
        updated_booking = booking_repo.update_status(booking_id, "CANCELLED")
        db.commit()
        db.refresh(updated_booking)
        
        return Booking.model_validate(updated_booking)
