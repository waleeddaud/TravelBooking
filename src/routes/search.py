"""
Search routes for flights and hotels.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session

from src.schemas.search_schema import Flight, Hotel
from src.services.search_service import SearchService
from src.dependencies import get_db


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/flights", response_model=List[Flight])
async def search_flights(
    origin: Optional[str] = Query(None, description="Origin airport code (e.g., JFK)"),
    destination: Optional[str] = Query(None, description="Destination airport code (e.g., LAX)"),
    db: Session = Depends(get_db)
):
    """
    Search for flights by origin and destination.
    
    Args:
        origin: Origin airport code (optional)
        destination: Destination airport code (optional)
        db: Database session
        
    Returns:
        List of matching flights
    """
    try:
        flights = SearchService.search_flights(db, origin, destination)
        return flights
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Flight search failed: {str(e)}"
        ) from e


@router.get("/hotels", response_model=List[Hotel])
async def search_hotels(
    city: str = Query(..., description="City name (e.g., Dubai)")
):
    """
    Search for hotels by city.
    
    Args:
        city: City name to search in
        
    Returns:
        List of matching hotels
    """
    try:
        hotels = SearchService.search_hotels(city)
        return hotels
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hotel search failed: {str(e)}"
        ) from e
