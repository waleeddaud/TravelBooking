"""
Integration test script to verify complete API functionality.
Tests: Register → Login → Search → Book → Cancel flow
"""

import httpx
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"
client = httpx.Client(base_url=BASE_URL, timeout=30.0)


def print_step(step: str):
    """Print formatted test step."""
    print(f"\n{'='*60}")
    print(f"  {step}")
    print(f"{'='*60}")


def print_result(success: bool, message: str, data=None):
    """Print test result."""
    icon = "✓" if success else "✗"
    print(f"{icon} {message}")
    if data and success:
        print(f"   Response: {json.dumps(data, indent=2)}")


def test_complete_flow():
    """Test complete booking flow."""
    test_email = f"testuser_{datetime.now().timestamp()}@example.com"
    test_password = "SecurePass123!"
    token = None
    booking_id = None
    
    try:
        # Step 1: Register
        print_step("Step 1: User Registration")
        register_data = {
            "email": test_email,
            "password": test_password,
            "full_name": "Test User",
            "phone": "+1234567890"
        }
        response = client.post("/auth/register", json=register_data)
        if response.status_code == 201:
            user_data = response.json()
            print_result(True, f"User registered: {user_data['email']}", user_data)
        else:
            print_result(False, f"Registration failed: {response.text}")
            return False
        
        # Step 2: Login
        print_step("Step 2: User Login")
        login_data = {
            "username": test_email,
            "password": test_password
        }
        response = client.post("/auth/login", data=login_data)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            print_result(True, "Login successful", {"token_type": auth_data["token_type"]})
        else:
            print_result(False, f"Login failed: {response.text}")
            return False
        
        # Step 3: Get Profile
        print_step("Step 3: Get User Profile")
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/users/me", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print_result(True, f"Profile retrieved: {profile['email']}", profile)
        else:
            print_result(False, f"Profile retrieval failed: {response.text}")
            return False
        
        # Step 4: Search Flights
        print_step("Step 4: Search Flights")
        response = client.get("/search/flights?origin=JFK&destination=LAX")
        if response.status_code == 200:
            flights = response.json()
            print_result(True, f"Found {len(flights)} flights", flights[:2] if flights else [])
            if not flights:
                print_result(False, "No flights available for booking")
                return False
            selected_flight = flights[0]
        else:
            print_result(False, f"Flight search failed: {response.text}")
            return False
        
        # Step 5: Create Booking
        print_step("Step 5: Create Booking")
        booking_data = {
            "flight_id": selected_flight["id"],
            "passengers": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "passport_number": "AB1234567",
                    "date_of_birth": "1990-01-01"
                }
            ]
        }
        response = client.post("/bookings", json=booking_data, headers=headers)
        if response.status_code == 201:
            booking = response.json()
            booking_id = booking["id"]
            print_result(True, f"Booking created: ID {booking_id}", booking)
        else:
            print_result(False, f"Booking creation failed: {response.text}")
            return False
        
        # Step 6: Get Booking Details
        print_step("Step 6: Get Booking Details")
        response = client.get(f"/bookings/{booking_id}", headers=headers)
        if response.status_code == 200:
            booking_details = response.json()
            print_result(True, f"Booking status: {booking_details['status']}", booking_details)
        else:
            print_result(False, f"Get booking failed: {response.text}")
            return False
        
        # Step 7: Get User Bookings
        print_step("Step 7: Get User Booking History")
        response = client.get("/users/me/bookings", headers=headers)
        if response.status_code == 200:
            bookings = response.json()
            print_result(True, f"User has {len(bookings)} booking(s)", bookings)
        else:
            print_result(False, f"Get bookings failed: {response.text}")
            return False
        
        # Step 8: Cancel Booking
        print_step("Step 8: Cancel Booking")
        response = client.delete(f"/bookings/{booking_id}", headers=headers)
        if response.status_code == 200:
            cancelled_booking = response.json()
            print_result(True, f"Booking cancelled: Status {cancelled_booking['status']}", cancelled_booking)
        else:
            print_result(False, f"Booking cancellation failed: {response.text}")
            return False
        
        # Step 9: Test Search Hotels
        print_step("Step 9: Search Hotels")
        response = client.get("/search/hotels?city=New York&check_in=2025-12-15&check_out=2025-12-18")
        if response.status_code == 200:
            hotels = response.json()
            print_result(True, f"Found {len(hotels)} hotels", hotels[:2] if hotels else [])
        else:
            print_result(False, f"Hotel search failed: {response.text}")
            return False
        
        # Step 10: Test Authentication Error
        print_step("Step 10: Test Unauthorized Access (Negative Test)")
        response = client.get("/users/me")
        if response.status_code == 401:
            print_result(True, "Unauthorized access correctly blocked", {"status": 401})
        else:
            print_result(False, f"Should have returned 401, got {response.status_code}")
            return False
        
        print_step("✓ ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print_result(False, f"Test failed with exception: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  TRAVEL BOOKING API - INTEGRATION TEST SUITE")
    print("="*60)
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_complete_flow()
    
    print("\n" + "="*60)
    if success:
        print("  🎉 TEST SUITE COMPLETED SUCCESSFULLY 🎉")
    else:
        print("  ❌ TEST SUITE FAILED")
    print("="*60 + "\n")
    
    client.close()
