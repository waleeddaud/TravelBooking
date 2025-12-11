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
        # Check existing flights count
        existing_count = db.query(Flight).count()
        print(f"📊 Current flights in database: {existing_count}")
        
        # Get existing flight IDs to avoid duplicates
        existing_ids = {f.flight_id for f in db.query(Flight.flight_id).all()}
        
        # Sample flights - New flights only (avoid duplicates)
        all_flights = [
            Flight(
                flight_id="SW405",
                airline="Southwest Airlines",
                origin="LAX",
                destination="SFO",
                departure_time=datetime.now() + timedelta(days=3, hours=7),
                arrival_time=datetime.now() + timedelta(days=3, hours=8),
                price=89.99,
                available_seats=140
            ),
            Flight(
                flight_id="AA506",
                airline="American Airlines",
                origin="MIA",
                destination="JFK",
                departure_time=datetime.now() + timedelta(days=8, hours=14),
                arrival_time=datetime.now() + timedelta(days=8, hours=17),
                price=179.99,
                available_seats=160
            ),
            
            Flight(
                flight_id="LH607",
                airline="Lufthansa",
                origin="JFK",
                destination="FRA",
                departure_time=datetime.now() + timedelta(days=12, hours=18),
                arrival_time=datetime.now() + timedelta(days=13, hours=7),
                price=849.99,
                available_seats=220
            ),
            Flight(
                flight_id="AF708",
                airline="Air France",
                origin="LAX",
                destination="CDG",
                departure_time=datetime.now() + timedelta(days=16, hours=22),
                arrival_time=datetime.now() + timedelta(days=17, hours=16),
                price=899.99,
                available_seats=250
            ),
            
            # International Routes - Middle East
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
            Flight(
                flight_id="QR809",
                airline="Qatar Airways",
                origin="JFK",
                destination="DOH",
                departure_time=datetime.now() + timedelta(days=18, hours=23),
                arrival_time=datetime.now() + timedelta(days=19, hours=17),
                price=1199.99,
                available_seats=280
            ),
            
            # Pakistani Routes - International
            Flight(
                flight_id="PK701",
                airline="Pakistan International Airlines",
                origin="JFK",
                destination="ISB",
                departure_time=datetime.now() + timedelta(days=15, hours=21),
                arrival_time=datetime.now() + timedelta(days=16, hours=19),
                price=899.99,
                available_seats=240
            ),
            Flight(
                flight_id="PK702",
                airline="Pakistan International Airlines",
                origin="LHR",
                destination="KHI",
                departure_time=datetime.now() + timedelta(days=10, hours=22),
                arrival_time=datetime.now() + timedelta(days=11, hours=11),
                price=699.99,
                available_seats=260
            ),
            Flight(
                flight_id="EK303",
                airline="Emirates",
                origin="DXB",
                destination="LHE",
                departure_time=datetime.now() + timedelta(days=9, hours=3),
                arrival_time=datetime.now() + timedelta(days=9, hours=6),
                price=399.99,
                available_seats=180
            ),
            Flight(
                flight_id="QR450",
                airline="Qatar Airways",
                origin="DOH",
                destination="ISB",
                departure_time=datetime.now() + timedelta(days=11, hours=2),
                arrival_time=datetime.now() + timedelta(days=11, hours=5),
                price=349.99,
                available_seats=200
            ),
            
            # Pakistani Domestic Routes
            Flight(
                flight_id="PK301",
                airline="Pakistan International Airlines",
                origin="ISB",
                destination="KHI",
                departure_time=datetime.now() + timedelta(days=5, hours=8),
                arrival_time=datetime.now() + timedelta(days=5, hours=10),
                price=89.99,
                available_seats=150
            ),
            Flight(
                flight_id="PK302",
                airline="Pakistan International Airlines",
                origin="KHI",
                destination="LHE",
                departure_time=datetime.now() + timedelta(days=6, hours=14),
                arrival_time=datetime.now() + timedelta(days=6, hours=16),
                price=79.99,
                available_seats=150
            ),
            Flight(
                flight_id="PK303",
                airline="Pakistan International Airlines",
                origin="LHE",
                destination="ISB",
                departure_time=datetime.now() + timedelta(days=7, hours=10),
                arrival_time=datetime.now() + timedelta(days=7, hours=11),
                price=69.99,
                available_seats=140
            ),
            Flight(
                flight_id="AP201",
                airline="Airblue",
                origin="ISB",
                destination="PEW",
                departure_time=datetime.now() + timedelta(days=4, hours=9),
                arrival_time=datetime.now() + timedelta(days=4, hours=10),
                price=59.99,
                available_seats=120
            ),
            Flight(
                flight_id="AP202",
                airline="Airblue",
                origin="KHI",
                destination="ISB",
                departure_time=datetime.now() + timedelta(days=8, hours=12),
                arrival_time=datetime.now() + timedelta(days=8, hours=14),
                price=85.99,
                available_seats=130
            ),
            Flight(
                flight_id="SJ101",
                airline="Serene Air",
                origin="LHE",
                destination="KHI",
                departure_time=datetime.now() + timedelta(days=9, hours=7),
                arrival_time=datetime.now() + timedelta(days=9, hours=9),
                price=74.99,
                available_seats=160
            ),
            
            # Asian Routes
            Flight(
                flight_id="SQ901",
                airline="Singapore Airlines",
                origin="JFK",
                destination="SIN",
                departure_time=datetime.now() + timedelta(days=20, hours=23),
                arrival_time=datetime.now() + timedelta(days=22, hours=5),
                price=1499.99,
                available_seats=290
            ),
            Flight(
                flight_id="TK801",
                airline="Turkish Airlines",
                origin="ISB",
                destination="IST",
                departure_time=datetime.now() + timedelta(days=13, hours=4),
                arrival_time=datetime.now() + timedelta(days=13, hours=10),
                price=549.99,
                available_seats=230
            ),
            Flight(
                flight_id="EY601",
                airline="Etihad Airways",
                origin="KHI",
                destination="AUH",
                departure_time=datetime.now() + timedelta(days=12, hours=3),
                arrival_time=datetime.now() + timedelta(days=12, hours=6),
                price=429.99,
                available_seats=210
            ),
        ]
        
        # Filter out flights that already exist
        flights = [f for f in all_flights if f.flight_id not in existing_ids]
        
        if not flights:
            print("✓ All flights already exist in database. No new flights to add.")
            return
        
        for flight in flights:
            db.add(flight)
        
        db.commit()
        print(f"✓ Successfully seeded {len(flights)} new flights into the database!")
        print(f"📊 Total flights in database now: {existing_count + len(flights)}")
        
        # Display seeded flights
        print("\nNewly Added Flights:")
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
