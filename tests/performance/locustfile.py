"""
Performance Testing for Travel Booking API using Locust
Run with: locust -f tests/performance/locustfile.py --host=http://localhost:8000
Web UI: http://localhost:8089
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random


class UserJourney(SequentialTaskSet):
    """Sequential user flow: Register -> Login -> Search -> Book -> View Profile"""
    
    token = None
    booking_id = None
    
    @task
    def register(self):
        """User registration"""
        random_id = random.randint(1000, 999999)
        response = self.client.post("/auth/register", json={
            "email": f"perftest{random_id}@example.com",
            "password": "TestPass123!",
            "full_name": f"Perf Test User {random_id}",
            "phone": f"+1234567{random_id % 10000:04d}"
        })
        if response.status_code == 201:
            self.user.email = f"perftest{random_id}@example.com"
    
    @task
    def login(self):
        """User authentication"""
        response = self.client.post("/auth/login", json={
            "email": getattr(self.user, 'email', 'test@example.com'),
            "password": "TestPass123!"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
    
    @task
    def search_flights(self):
        """Search available flights"""
        origins = ["NYC", "LAX", "CHI", "MIA"]
        destinations = ["LON", "PAR", "TOK", "DXB"]
        self.client.get(
            f"/search/flights?origin={random.choice(origins)}&destination={random.choice(destinations)}&date=2025-12-20",
            name="/search/flights"
        )
    
    @task
    def view_profile(self):
        """View user profile"""
        if self.token:
            self.client.get("/users/me", headers={
                "Authorization": f"Bearer {self.token}"
            })


class TravelAPIUser(HttpUser):
    """Simulates typical API user behavior - Public endpoints only"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    @task(7)
    def search_flights(self):
        """Search flights - most common operation"""
        origins = ["NYC", "LAX", "CHI", "MIA", "SFO"]
        destinations = ["LON", "PAR", "TOK", "DXB", "SYD"]
        self.client.get(
            f"/search/flights?origin={random.choice(origins)}&destination={random.choice(destinations)}&date=2025-12-25",
            name="/search/flights"
        )
    
    @task(3)
    def search_hotels(self):
        """Search hotels"""
        cities = ["London", "Paris", "Tokyo", "Dubai", "Sydney"]
        self.client.get(
            f"/search/hotels?city={random.choice(cities)}&check_in=2025-12-20&check_out=2025-12-25&guests=2",
            name="/search/hotels"
        )


class AuthenticatedUser(HttpUser):
    """User that creates account and performs authenticated actions"""
    wait_time = between(1, 2)
    token = None
    user_email = None
    
    def on_start(self):
        """Register a new user on start"""
        random_id = random.randint(10000, 999999)
        self.user_email = f"loadtest{random_id}@test.com"
        
        # Register
        response = self.client.post("/auth/register", json={
            "email": self.user_email,
            "password": "Test123456!",
            "full_name": f"Load Test User {random_id}",
            "phone": f"+1555{random_id % 10000:04d}"
        }, name="/auth/register")
        
        # Login to get token
        if response.status_code == 201:
            login_response = self.client.post("/auth/login", json={
                "email": self.user_email,
                "password": "Test123456!"
            }, name="/auth/login")
            
            if login_response.status_code == 200:
                self.token = login_response.json().get("access_token")
    
    @task(3)
    def view_profile(self):
        """View own profile"""
        if self.token:
            self.client.get("/users/me", headers={
                "Authorization": f"Bearer {self.token}"
            })
    
    @task(2)
    def search_flights(self):
        """Search flights"""
        origins = ["NYC", "LAX", "CHI"]
        destinations = ["LON", "PAR", "TOK"]
        self.client.get(
            f"/search/flights?origin={random.choice(origins)}&destination={random.choice(destinations)}&date=2025-12-25",
            name="/search/flights"
        )
    
    @task(1)
    def view_booking_history(self):
        """View booking history"""
        if self.token:
            self.client.get("/users/me/bookings", headers={
                "Authorization": f"Bearer {self.token}"
            })


class QuickLoadTest(HttpUser):
    """Quick load test focusing only on public endpoints"""
    wait_time = between(0.5, 1.5)
    
    @task
    def search_flights_load(self):
        """Rapid flight searches"""
        origins = ["NYC", "LAX", "CHI"]
        destinations = ["LON", "PAR", "TOK"]
        self.client.get(
            f"/search/flights?origin={random.choice(origins)}&destination={random.choice(destinations)}",
            name="/search/flights [load]"
        )
