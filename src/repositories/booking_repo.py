"""
Booking repository for database operations.

Handles CRUD operations for Booking model.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from src.models.booking_model import Booking, BookingStatus


class BookingRepository:
    """Repository for Booking database operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(
        self,
        user_id: int,
        flight_id: int,
        total_price: float,
        passenger_data: dict
    ) -> Booking:
        """
        Create a new booking.
        
        Args:
            user_id: ID of the user creating the booking
            flight_id: ID of the flight to book
            total_price: Calculated total price
            passenger_data: JSON data with passenger information
            
        Returns:
            Created booking object
        """
        db_booking = Booking(
            booking_id=str(uuid.uuid4()),
            user_id=user_id,
            flight_id=flight_id,
            status=BookingStatus.PENDING,
            total_price=total_price,
            passenger_data=passenger_data,
            created_at=datetime.utcnow()
        )
        self.db.add(db_booking)
        self.db.flush()
        return db_booking
    
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        """
        Get booking by ID.
        
        Args:
            booking_id: Booking ID
            
        Returns:
            Booking object if found, None otherwise
        """
        return self.db.query(Booking).filter(
            Booking.id == booking_id
        ).first()
    
    def get_user_bookings(self, user_id: int) -> List[Booking]:
        """
        Get all bookings for a user.
        
        Args:
            user_id: User's database ID
            
        Returns:
            List of user's bookings
        """
        return self.db.query(Booking).filter(
            Booking.user_id == user_id
        ).order_by(Booking.created_at.desc()).all()
    
    def update_status(
        self,
        booking_id: int,
        new_status: str
    ) -> Booking:
        """
        Update booking status.
        
        Args:
            booking_id: Booking ID
            new_status: New status value
            
        Returns:
            Updated booking
        """
        booking = self.get_by_id(booking_id)
        if booking:
            booking.status = new_status
            self.db.flush()
        return booking
    
    def delete(self, booking_id: int) -> bool:
        """
        Delete a booking.
        
        Args:
            booking_id: Booking ID
            
        Returns:
            True if deleted, False if not found
        """
        booking = self.get_by_id(booking_id)
        if booking:
            self.db.delete(booking)
            self.db.flush()
            return True
        return False
