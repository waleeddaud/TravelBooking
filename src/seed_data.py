"""
Seed database with initial flight data for testing.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.flight_model import Flight


def seed_flights():
    """Add sample flights to the database."""
    db: Session = SessionLocal()
    
    try:
        # Check if flights already exist
        existing_count = db.query(Flight).count()
        if existing_count > 0:
            print(f"✓ Database already has {existing_count} flights. Skipping seed.")
            return
        
        # Sample flights
        flights = [
            Flight(
                flight_id="AA101",
                airline="American Airlines",
                origin="JFK",
                destination="LAX",
                departure_time=datetime.now() + timedelta(days=7, hours=8),
                arrival_time=datetime.now() + timedelta(days=7, hours=14),
                price=299.99,
                available_seats=150
            ),
            Flight(
                flight_id="UA202",
                airline="United Airlines",
                origin="LAX",
                destination="ORD",
                departure_time=datetime.now() + timedelta(days=10, hours=10),
                arrival_time=datetime.now() + timedelta(days=10, hours=14),
                price=249.99,
                available_seats=180
            ),
            Flight(
                flight_id="DL303",
                airline="Delta Airlines",
                origin="ORD",
                destination="MIA",
                departure_time=datetime.now() + timedelta(days=5, hours=6),
                arrival_time=datetime.now() + timedelta(days=5, hours=9),
                price=199.99,
                available_seats=120
            ),
            Flight(
                flight_id="BA404",
                airline="British Airways",
                origin="JFK",
                destination="LHR",
                departure_time=datetime.now() + timedelta(days=14, hours=20),
                arrival_time=datetime.now() + timedelta(days=15, hours=8),
                price=799.99,
                available_seats=200
            ),
            Flight(
                flight_id="EK505",
                airline="Emirates",
                origin="LAX",
                destination="DXB",
                departure_time=datetime.now() + timedelta(days=21, hours=1),
                arrival_time=datetime.now() + timedelta(days=21, hours=17),
                price=1299.99,
                available_seats=300
            ),
        ]
        
        for flight in flights:
            db.add(flight)
        
        db.commit()
        print(f"✓ Successfully seeded {len(flights)} flights into the database!")
        
        # Display seeded flights
        print("\nSeeded Flights:")
        for flight in flights:
            print(f"  • {flight.flight_id}: {flight.origin} → {flight.destination} (${flight.price})")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_flights()
