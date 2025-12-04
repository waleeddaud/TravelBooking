"""
Search service for flights and hotels.

Provides database-backed search functionality for flights and hotels.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.schemas.search_schema import Flight, Hotel
from src.models.flight_model import Flight as FlightModel


# Mock flight data
MOCK_FLIGHTS = [
    {
        "flight_id": "FL001",
        "airline": "Emirates",
        "origin": "LHE",
        "destination": "DXB",
        "departure_time": "2025-01-15T08:00:00",
        "arrival_time": "2025-01-15T11:30:00",
        "price": 450.00,
        "currency": "USD",
        "available_seats": 120
    },
    {
        "flight_id": "FL002",
        "airline": "PIA",
        "origin": "LHE",
        "destination": "DXB",
        "departure_time": "2025-01-15T14:00:00",
        "arrival_time": "2025-01-15T17:30:00",
        "price": 380.00,
        "currency": "USD",
        "available_seats": 85
    },
    {
        "flight_id": "FL003",
        "airline": "British Airways",
        "origin": "LHE",
        "destination": "LHR",
        "departure_time": "2025-01-16T22:00:00",
        "arrival_time": "2025-01-17T02:30:00",
        "price": 650.00,
        "currency": "USD",
        "available_seats": 95
    }
]

# Mock hotel data (hotels will be added to database later)
MOCK_HOTELS = [
    {
        "hotel_id": "HT001",
        "name": "Burj Al Arab",
        "city": "Dubai",
        "address": "Jumeirah Street, Dubai",
        "rating": 5.0,
        "price_per_night": 1200.00,
        "currency": "USD",
        "available_rooms": 15
    },
    {
        "hotel_id": "HT002",
        "name": "Atlantis The Palm",
        "city": "Dubai",
        "address": "Crescent Road, Palm Jumeirah",
        "rating": 4.8,
        "price_per_night": 850.00,
        "currency": "USD",
        "available_rooms": 32
    },
    {
        "hotel_id": "HT003",
        "name": "Pearl Continental",
        "city": "Lahore",
        "address": "Shahrah-e-Quaid-e-Azam",
        "rating": 4.5,
        "price_per_night": 180.00,
        "currency": "USD",
        "available_rooms": 45
    }
]


class SearchService:
    """Service for searching flights and hotels."""
    
    @staticmethod
    def search_flights(db: Session, origin: Optional[str] = None, destination: Optional[str] = None) -> List[Flight]:
        """
        Search for flights matching criteria from database.
        
        Args:
            db: Database session
            origin: Origin airport code (optional)
            destination: Destination airport code (optional)
            
        Returns:
            List of matching flights
        """
        query = db.query(FlightModel)
        
        if origin:
            query = query.filter(FlightModel.origin.ilike(origin))
        if destination:
            query = query.filter(FlightModel.destination.ilike(destination))
        
        db_flights = query.all()
        
        # Convert to Pydantic models
        results = [
            Flight(
                id=f.id,
                flight_id=f.flight_id,
                airline=f.airline,
                origin=f.origin,
                destination=f.destination,
                departure_time=f.departure_time.isoformat(),
                arrival_time=f.arrival_time.isoformat(),
                price=float(f.price),
                currency=f.currency,
                available_seats=f.available_seats
            )
            for f in db_flights
        ]
        
        return results
    
    @staticmethod
    def search_hotels(city: str) -> List[Hotel]:
        """
        Search for hotels in a specific city (mock data).
        
        Args:
            city: City name to search in
            
        Returns:
            List of matching hotels
        """
        results = [
            Hotel(**hotel) 
            for hotel in MOCK_HOTELS 
            if hotel["city"].lower() == city.lower()
        ]
        return results
    
    @staticmethod
    def get_flight_by_id(db: Session, flight_id: int) -> Optional[Flight]:
        """
        Get a specific flight by ID from database.
        
        Args:
            db: Database session
            flight_id: Flight identifier
            
        Returns:
            Flight object if found, None otherwise
        """
        db_flight = db.query(FlightModel).filter(FlightModel.id == flight_id).first()
        
        if not db_flight:
            return None
        
        return Flight(
            id=db_flight.id,
            flight_id=db_flight.flight_id,
            airline=db_flight.airline,
            origin=db_flight.origin,
            destination=db_flight.destination,
            departure_time=db_flight.departure_time.isoformat(),
            arrival_time=db_flight.arrival_time.isoformat(),
            price=float(db_flight.price),
            currency=db_flight.currency,
            available_seats=db_flight.available_seats
        )
    
    @staticmethod
    def get_hotel_by_id(hotel_id: str) -> Optional[Hotel]:
        """
        Get a specific hotel by ID (mock data).
        
        Args:
            hotel_id: Hotel identifier
            
        Returns:
            Hotel object if found, None otherwise
        """
        for hotel in MOCK_HOTELS:
            if hotel["hotel_id"] == hotel_id:
                return Hotel(**hotel)
        return None

