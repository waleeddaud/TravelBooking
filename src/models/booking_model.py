"""
Booking database model.

SQLAlchemy model for bookings table.
"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.database import Base


class BookingStatus(str, enum.Enum):
    """Booking status enumeration."""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Booking(Base):
    """Booking model for database storage."""
    
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    status = Column(String, default="PENDING", nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    passenger_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", backref="bookings")
    flight = relationship("Flight", backref="bookings")
    
    def __repr__(self):
        return f"<Booking(id={self.id}, booking_id={self.booking_id}, status={self.status})>"

