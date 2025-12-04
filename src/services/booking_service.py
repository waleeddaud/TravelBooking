"""
Booking service for managing flight and hotel bookings.

Provides in-memory storage for bookings with CRUD operations.
"""

from datetime import datetime
from typing import List, Optional
import uuid

from src.schemas.booking_schema import Booking, BookingCreate
from src.services.search_service import SearchService


# In-memory booking storage
bookings_db: dict[str, dict] = {}


class BookingService:
    """Service for managing bookings."""
    
    @staticmethod
    def create_booking(booking_data: BookingCreate, user_email: str) -> Booking:
        """
        Create a new booking.
        
        Args:
            booking_data: Booking creation data
            user_email: Email of the user creating the booking
            
        Returns:
            Created booking object
            
        Raises:
            ValueError: If item (flight/hotel) not found or unavailable
        """
        # Validate item exists and get price
        total_price = 0.0
        if booking_data.booking_type == "flight":
            flight = SearchService.get_flight_by_id(booking_data.item_id)
            if not flight:
                raise ValueError(f"Flight {booking_data.item_id} not found")
            if flight.available_seats < booking_data.passengers:
                raise ValueError(f"Not enough available seats")
            total_price = flight.price * booking_data.passengers
        else:  # hotel
            hotel = SearchService.get_hotel_by_id(booking_data.item_id)
            if not hotel:
                raise ValueError(f"Hotel {booking_data.item_id} not found")
            if hotel.available_rooms < 1:
                raise ValueError(f"No available rooms")
            total_price = hotel.price_per_night  # Simplified: 1 night
        
        # Create booking
        booking_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        booking = {
            "booking_id": booking_id,
            "user_email": user_email,
            "booking_type": booking_data.booking_type,
            "item_id": booking_data.item_id,
            "status": "pending",
            "passengers": booking_data.passengers,
            "special_requests": booking_data.special_requests,
            "total_price": total_price,
            "currency": "USD",
            "created_at": now,
    
    
    @staticmethod
    def get_booking(booking_id: str, user_email: str) -> Optional[Booking]:
        """
        Get a booking by ID.
        
        Args:
            booking_id: Booking identifier
            user_email: Email of the requesting user
            
        Returns:
            Booking object if found and belongs to user, None otherwise
        """
        booking = bookings_db.get(booking_id)
        if booking and booking["user_email"] == user_email:
            return Booking(**booking)
        return None
    
    @staticmethod
    def get_user_bookings(user_email: str) -> List[Booking]:
        """
        Get all bookings for a user.
        
        Args:
            user_email: User's email address
            
        Returns:
            List of user's bookings
        """
        user_bookings = [
            Booking(**booking) 
            for booking in bookings_db.values() 
            if booking["user_email"] == user_email
        ]
        return user_bookings
    
    @staticmethod
    def update_booking_status(
        booking_id: str, 
        user_email: str, 
        new_status: str
    ) -> Optional[Booking]:
        """
        Update booking status (confirm or cancel).
        
        Args:
            booking_id: Booking identifier
            user_email: Email of the requesting user
            new_status: New status value
            
        Returns:
            Updated booking if successful, None otherwise
        """
        booking = bookings_db.get(booking_id)
        if not booking or booking["user_email"] != user_email:
            return None
        
        booking["status"] = new_status
        booking["updated_at"] = datetime.utcnow()
        
        return Booking(**booking)
    
    @staticmethod
    def cancel_booking(booking_id: str, user_email: str) -> Optional[Booking]:
        """
        Cancel a booking.
        
        Args:
            booking_id: Booking identifier
            user_email: Email of the requesting user
            
        Returns:
            Cancelled booking if successful, None otherwise
        """
        return BookingService.update_booking_status(
            booking_id, 
            user_email, 
            "cancelled"
        )
