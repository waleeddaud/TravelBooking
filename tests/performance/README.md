# Performance Testing with Locust

## Setup

Install Locust:
```cmd
pip install locust
```

## Running Tests

### Basic Performance Test
```cmd
locust -f tests/performance/locustfile.py --host=http://localhost:8000
```

Then open: **http://localhost:8089**

**Web UI Configuration:**
- Number of users: 10-50 (start small)
- Spawn rate: 2-5 users/second
- Host: http://localhost:8000

### Headless Mode (Command Line)
```cmd
locust -f tests/performance/locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 2 --run-time 1m --headless
```

### Generate HTML Report
```cmd
locust -f tests/performance/locustfile.py --host=http://localhost:8000 --users 20 --spawn-rate 2 --run-time 1m --headless --html=performance_report.html
```

## Available User Classes

### 1. TravelAPIUser (Default)
Simulates typical user behavior with weighted tasks:
- 5x Flight searches
- 3x Hotel searches
- 2x Profile views
- 1x Booking creation

**Use for:** General load testing

### 2. UserJourney
Sequential flow testing:
1. Register
2. Login
3. Search
4. Book
5. View Profile

**Use for:** End-to-end flow validation

**Run specific class:**
```cmd
locust -f tests/performance/locustfile.py UserJourney --host=http://localhost:8000
```

### 3. QuickLoadTest
Rapid public endpoint testing (no auth):
- High-frequency search requests
- Minimal wait time

**Use for:** Maximum load stress testing

**Run specific class:**
```cmd
locust -f tests/performance/locustfile.py QuickLoadTest --host=http://localhost:8000
```

## Performance Metrics

Locust tracks:
- **Requests/sec**: Throughput
- **Response Time**: Average, Min, Max, Median (50th percentile)
- **95th/99th Percentile**: Response time for 95%/99% of requests
- **Failure Rate**: Percentage of failed requests

## Expected Results (Local Development)

| Metric | Expected Value |
|--------|---------------|
| Average Response Time | <500ms |
| 95th Percentile | <1000ms |
| Failure Rate | <1% |
| Requests/sec | 20-50 (depends on hardware) |

## Tips

1. **Start Server First:**
   ```cmd
   uvicorn src.main:app --reload
   ```

2. **Start Small:** Begin with 5-10 users, increase gradually

3. **Monitor Resources:** Watch CPU/RAM usage during tests

4. **Pre-seed Data:** Ensure test database has users/flights/hotels before load testing

5. **Auth Tokens:** Tests use hardcoded test credentials; ensure `test@example.com` exists in DB

## Troubleshooting

**Issue:** 401 Unauthorized errors
- **Fix:** Create test user: `email: test@example.com, password: testpass123`

**Issue:** 404 Not Found on bookings
- **Fix:** Ensure flight/hotel IDs exist in database

**Issue:** Connection refused
- **Fix:** Verify FastAPI server is running on port 8000
