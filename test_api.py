"""
Simple test script to verify Travel Booking API is working correctly.
Run this after starting the server with start.bat or start.sh
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test health check endpoint"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print_section("Testing User Registration")
    
    # Generate unique email
    timestamp = int(datetime.now().timestamp())
    user_data = {
        "email": f"testuser{timestamp}@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        return user_data["email"], user_data["password"]
    return None, None

def test_login(email, password):
    """Test user login"""
    print_section("Testing User Login")
    
    login_data = {
        "username": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✓ Login successful! Token received.")
        return token
    else:
        print(f"✗ Login failed: {response.json()}")
        return None

def test_search_flights():
    """Test flight search"""
    print_section("Testing Flight Search")
    
    params = {"origin": "LHE", "destination": "DXB"}
    response = requests.get(f"{BASE_URL}/search/flights", params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        flights = response.json()
        print(f"✓ Found {len(flights)} flights")
        if flights:
            print(f"Sample Flight: {flights[0]['airline']} - ${flights[0]['price']}")
            return flights[0]['flight_id']
    return None

def test_search_hotels():
    """Test hotel search"""
    print_section("Testing Hotel Search")
    
    params = {"city": "Dubai"}
    response = requests.get(f"{BASE_URL}/search/hotels", params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        hotels = response.json()
        print(f"✓ Found {len(hotels)} hotels")
        if hotels:
            print(f"Sample Hotel: {hotels[0]['name']} - ${hotels[0]['price_per_night']}/night")
    return response.status_code == 200

def test_create_booking(token, flight_id):
    """Test booking creation"""
    print_section("Testing Booking Creation")
    
    headers = {"Authorization": f"Bearer {token}"}
    booking_data = {
        "booking_type": "flight",
        "item_id": flight_id,
        "passengers": 2,
        "special_requests": "Window seats preferred"
    }
    
    response = requests.post(f"{BASE_URL}/bookings", json=booking_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        booking = response.json()
        print(f"✓ Booking created! ID: {booking['booking_id']}")
        print(f"  Status: {booking['status']}")
        print(f"  Total: ${booking['total_price']}")
        return booking['booking_id']
    else:
        print(f"✗ Booking failed: {response.json()}")
    return None

def test_get_user_profile(token):
    """Test getting user profile"""
    print_section("Testing User Profile")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        profile = response.json()
        print(f"✓ Profile retrieved")
        print(f"  Name: {profile['full_name']}")
        print(f"  Email: {profile['email']}")
    return response.status_code == 200

def test_get_booking_history(token):
    """Test getting booking history"""
    print_section("Testing Booking History")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/users/me/bookings", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        bookings = response.json()
        print(f"✓ Found {len(bookings)} booking(s)")
        for booking in bookings:
            print(f"  - {booking['booking_type'].title()}: {booking['status']}")
    return response.status_code == 200

def test_cancel_booking(token, booking_id):
    """Test booking cancellation"""
    print_section("Testing Booking Cancellation")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id}/cancel", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        booking = response.json()
        print(f"✓ Booking cancelled")
        print(f"  New Status: {booking['status']}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "TRAVEL BOOKING API TEST" + " "*20 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Test basic endpoints
        if not test_health():
            print("\n✗ Health check failed! Is the server running?")
            return
        
        if not test_root():
            print("\n✗ Root endpoint failed!")
            return
        
        # Test authentication flow
        email, password = test_register()
        if not email:
            print("\n✗ Registration failed!")
            return
        
        token = test_login(email, password)
        if not token:
            print("\n✗ Login failed!")
            return
        
        # Test search functionality
        flight_id = test_search_flights()
        test_search_hotels()
        
        # Test booking flow
        if flight_id:
            booking_id = test_create_booking(token, flight_id)
            
            if booking_id:
                test_get_user_profile(token)
                test_get_booking_history(token)
                test_cancel_booking(token, booking_id)
        
        # Final summary
        print_section("TEST SUMMARY")
        print("✓ All tests completed successfully!")
        print(f"\n📚 API Documentation: {BASE_URL}/docs")
        print(f"🔍 Alternative Docs: {BASE_URL}/redoc")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to server!")
        print("  Please make sure the server is running:")
        print("  - Run: start.bat (Windows) or ./start.sh (Linux/Mac)")
        print(f"  - Check: {BASE_URL}/docs")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
