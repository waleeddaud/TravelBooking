# Karate DSL Testing Guide for Travel Booking API

## What is Karate?

**Karate** is an open-source test automation framework that combines:
- **API testing** (REST, SOAP, GraphQL)
- **UI automation** (web browser testing)
- **Performance testing** (load testing)

### Key Features:
- **BDD Syntax**: Write tests in Gherkin (Given-When-Then) format
- **No Java/Coding Required**: Tests are written in plain English-like syntax
- **Built-in Assertions**: Powerful JSON/XML matching
- **Data-Driven Testing**: Easy parameterization
- **Parallel Execution**: Fast test execution
- **Detailed Reports**: HTML reports with screenshots

---

## Why Use Karate for API Testing?

### Advantages:
1. **Readable Tests**: Business analysts can understand and write tests
2. **No Setup Overhead**: No need for separate assertion libraries
3. **Integrated**: Request, response validation, and assertions in one place
4. **Re-usable**: Share common setup across tests
5. **CI/CD Friendly**: Easy integration with Jenkins, GitHub Actions

### Comparison with Other Tools:

| Feature | Karate | Postman | Rest-Assured | Pytest |
|---------|--------|---------|--------------|--------|
| Learning Curve | Low | Low | Medium | Medium |
| Programming | No | No | Yes (Java) | Yes (Python) |
| BDD Support | Yes | No | No | Via plugin |
| Parallel Execution | Yes | Paid | Yes | Yes |
| Data-Driven | Built-in | Manual | Manual | Via fixtures |

---

## How to Use Karate with Our Travel Booking API

### Installation & Setup

#### 1. Prerequisites
```bash
# Java 11 or higher required
java -version

# Maven (build tool)
mvn -version
```

#### 2. Project Structure (Already Created)
```
tests/karate/
├── karate-config.js          # Global configuration
├── pom.xml                    # Maven dependencies
└── features/
    ├── auth.feature           # Authentication tests
    ├── flight-search.feature  # Flight search tests
    ├── booking-lifecycle.feature  # Full booking flow
    └── payment-mock.feature   # Payment simulation
```

---

## Running Karate Tests

### Method 1: Using Maven (Recommended)
```bash
# Navigate to karate directory
cd tests/karate

# Run all tests
mvn test

# Run specific feature
mvn test -Dkarate.options="--tags @smoke"

# Run with reports
mvn test -Dkarate.options="--tags @regression" -Dkarate.env=dev
```

### Method 2: Using Command Line
```bash
# Run all features
java -jar karate.jar features/

# Run specific feature
java -jar karate.jar features/auth.feature

# Parallel execution (4 threads)
java -jar karate.jar --threads 4 features/
```

### Method 3: IDE Integration
- **IntelliJ IDEA**: Install "Karate" plugin
- **VS Code**: Install "Karate Runner" extension
- Right-click on `.feature` file → Run

---

## Test Execution Flow for Our API

### Complete Test Scenario:

```gherkin
Feature: Complete Booking Lifecycle

Background:
  * url 'http://localhost:8000'
  * def randomEmail = 'test' + java.lang.System.currentTimeMillis() + '@example.com'

Scenario: User can search, book, and cancel flight
  
  # Step 1: Register
  Given path 'auth/register'
  And request { email: '#(randomEmail)', password: 'Test123!', full_name: 'Test User' }
  When method POST
  Then status 201
  And match response.email == randomEmail
  
  # Step 2: Login
  Given path 'auth/login'
  And form field username = randomEmail
  And form field password = 'Test123!'
  When method POST
  Then status 200
  And match response.access_token == '#present'
  * def authToken = response.access_token
  
  # Step 3: Search Flights
  Given path 'search/flights'
  And param origin = 'JFK'
  And param destination = 'LAX'
  When method GET
  Then status 200
  And match response == '#[]'
  And match each response contains { flight_id: '#string', price: '#number' }
  * def flightId = response[0].id
  
  # Step 4: Create Booking
  Given path 'bookings'
  And header Authorization = 'Bearer ' + authToken
  And request 
    """
    {
      flight_id: '#(flightId)',
      passengers: [
        {
          first_name: 'John',
          last_name: 'Doe',
          passport_number: 'AB123456',
          date_of_birth: '1990-01-01'
        }
      ]
    }
    """
  When method POST
  Then status 201
  And match response.status == 'PENDING'
  * def bookingId = response.id
  
  # Step 5: Get Booking
  Given path 'bookings', bookingId
  And header Authorization = 'Bearer ' + authToken
  When method GET
  Then status 200
  And match response.id == bookingId
  
  # Step 6: Cancel Booking
  Given path 'bookings', bookingId
  And header Authorization = 'Bearer ' + authToken
  When method DELETE
  Then status 200
  And match response.status == 'CANCELLED'
```

---

## Karate vs Our Current Tests

### Current Integration Test (Python)
```python
def test_complete_flow():
    # Register
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    
    # Login
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Search
    response = client.get("/search/flights?origin=JFK")
    # ... more code
```

### Equivalent Karate Test
```gherkin
Scenario: Complete flow
  * call read('auth.feature@register')
  * call read('auth.feature@login')
  * call read('search.feature@searchFlights')
  # More readable, reusable, no code
```

---

## Running Tests for Our API

### Step-by-Step Execution:

#### 1. Start the API Server
```bash
# Terminal 1: Start server
cd "C:\Users\HP\Desktop\SQE TravelBooking"
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

#### 2. Seed Test Data
```bash
# Terminal 2: Seed database
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
python src/seed_data.py
```

#### 3. Run Karate Tests
```bash
# Terminal 3: Run tests
cd tests/karate
mvn test
```

#### 4. View Reports
```
# Open in browser:
tests/karate/target/karate-reports/karate-summary.html
```

---

## Advanced Karate Features

### 1. **Data-Driven Testing**
```gherkin
Scenario Outline: Search flights from multiple origins
  Given path 'search/flights'
  And param origin = '<origin>'
  And param destination = '<destination>'
  When method GET
  Then status 200
  
  Examples:
    | origin | destination |
    | JFK    | LAX        |
    | ORD    | MIA        |
    | LAX    | DXB        |
```

### 2. **Conditional Logic**
```gherkin
Scenario: Conditional booking
  * def hasSeats = response.available_seats > 0
  * if (hasSeats) karate.call('create-booking.feature')
```

### 3. **Performance Testing**
```gherkin
Scenario: Load test flight search
  * configure performance = { time: 10000, throughput: 100 }
  Given path 'search/flights'
  When method GET
```

### 4. **Mock Data**
```gherkin
Scenario: Test with mock server
  * def mockResponse = read('mock-flight-data.json')
  Given path 'search/flights'
  When method GET
  Then match response == mockResponse
```

---

## Integration with CI/CD

### GitHub Actions Example:
```yaml
name: API Tests

on: [push, pull_request]

jobs:
  karate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Java
        uses: actions/setup-java@v2
        with:
          java-version: '11'
      
      - name: Start API
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          uvicorn src.main:app &
          sleep 10
      
      - name: Run Karate Tests
        run: |
          cd tests/karate
          mvn test
      
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: karate-reports
          path: tests/karate/target/karate-reports/
```

---

## Best Practices

### 1. **Organize Tests by Feature**
```
features/
├── smoke/          # Quick sanity tests
├── regression/     # Full test suite
└── performance/    # Load tests
```

### 2. **Use Tags**
```gherkin
@smoke @critical
Scenario: Login test

@regression @booking
Scenario: Complete booking flow
```

### 3. **Reusable Functions**
```javascript
// karate-config.js
function fn() {
  var config = {
    baseUrl: 'http://localhost:8000',
    adminToken: 'xyz123'
  };
  return config;
}
```

### 4. **Error Scenarios**
```gherkin
Scenario: Invalid booking should fail
  Given path 'bookings'
  And request { flight_id: 99999 }
  When method POST
  Then status 400
  And match response.detail contains 'not found'
```

---

## Comparison Summary

| Aspect | Karate | Python Integration Test | Postman |
|--------|--------|------------------------|---------|
| **Syntax** | Gherkin (BDD) | Python code | JSON/JavaScript |
| **Setup** | Maven/Java | Virtual env | Desktop app |
| **Learning** | Easy | Medium | Easy |
| **CI/CD** | Excellent | Excellent | Good |
| **Reports** | Built-in HTML | Custom | Cloud-based |
| **Debugging** | Good | Excellent | Good |
| **Best For** | API contracts, BDD | Unit + Integration | Manual testing |

---

## Getting Started Checklist

- [ ] Install Java 11+
- [ ] Install Maven
- [ ] Review `tests/karate/features/` directory
- [ ] Run `mvn test` in `tests/karate/`
- [ ] View HTML reports
- [ ] Modify tests for your scenarios
- [ ] Integrate with CI/CD

---

## Conclusion

**Karate is ideal for:**
- ✅ API contract testing
- ✅ BDD-style test documentation
- ✅ Quick test creation without coding
- ✅ Cross-team collaboration (QA + Dev + Business)

**Use our Python tests for:**
- ✅ Unit testing business logic
- ✅ Deep integration testing
- ✅ Database validation

**Use Postman for:**
- ✅ Manual exploratory testing
- ✅ Quick API debugging
- ✅ Sharing with non-technical team

**Best approach:** Use all three complementarily! 🎯
