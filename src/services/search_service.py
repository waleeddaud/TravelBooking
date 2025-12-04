"""
Search service for flights and hotels.

Provides in-memory mock data for search functionality.
This is structured to be easily replaced with database queries.
"""

from typing import List
from src.schemas.search_schema import Flight, Hotel


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

# Mock hotel data
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
    def search_flights(origin: str, destination: str) -> List[Flight]:
        """
        Search for flights matching origin and destination.
        
        Args:
            origin: Origin airport code
            destination: Destination airport code
            
        Returns:
            List of matching flights
        """
        results = [
            Flight(**flight) 
            for flight in MOCK_FLIGHTS 
            if flight["origin"].upper() == origin.upper() 
            and flight["destination"].upper() == destination.upper()
        ]
        return results
    
    @staticmethod
    def search_hotels(city: str) -> List[Hotel]:
        """
        Search for hotels in a specific city.
        
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
    def get_flight_by_id(flight_id: str) -> Flight | None:
        """
        Get a specific flight by ID.
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight object if found, None otherwise
        """
        for flight in MOCK_FLIGHTS:
            if flight["flight_id"] == flight_id:
                return Flight(**flight)
        return None
    
    @staticmethod
    def get_hotel_by_id(hotel_id: str) -> Hotel | None:
        """
        Get a specific hotel by ID.
        
        Args:
            hotel_id: Hotel identifier
            
        Returns:
            Hotel object if found, None otherwise
        """
        for hotel in MOCK_HOTELS:
            if hotel["hotel_id"] == hotel_id:
                return Hotel(**hotel)
        return None
