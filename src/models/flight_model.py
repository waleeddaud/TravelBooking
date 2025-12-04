"""
Flight database model.

SQLAlchemy model for flights table.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database import Base


class Flight(Base):
    """Flight model for database storage."""
    
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(String, unique=True, index=True, nullable=False)
    airline = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    available_seats = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Flight(id={self.id}, flight_id={self.flight_id}, route={self.origin}-{self.destination})>"
