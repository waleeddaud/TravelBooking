# Karate DSL Tests for Travel Booking API

Comprehensive end-to-end API tests using Karate DSL framework.

## Overview

This test suite provides complete E2E testing coverage including:
- Authentication flows (register, login)
- Search functionality (flights, hotels)
- Complete booking lifecycle (create, view, cancel)
- Authorization and error handling
- Negative test scenarios

## Prerequisites

- Java 11 or higher
- Maven 3.6+
- Running Travel Booking API (default: http://localhost:8000)

## Test Files

### Configuration
- `karate-config.js` - Global configuration and base URL setup
- `pom.xml` - Maven project configuration

### Feature Files

#### `auth.feature`
**Authentication Tests**
- ✅ User registration with unique email
- ✅ Duplicate email registration failure
- ✅ Successful user login with JWT token
- ✅ Invalid credentials login failure

**Scenarios:**
1. User Registration - Success
2. User Registration - Duplicate Email
3. User Login - Success
4. User Login - Invalid Credentials

#### `flight-search.feature`
**Search Tests**
- ✅ Flight search with valid routes
- ✅ Hotel search by city
- ✅ Empty search results handling

**Scenarios:**
1. Search Flights - Valid Route (LHE to DXB)
2. Search Flights - Valid Route (LHE to LHR)
3. Search Flights - No Results
4. Search Hotels - Valid City (Dubai)
5. Search Hotels - No Results

#### `booking-lifecycle.feature`
**Complete Booking Flow Tests**
- ✅ Full lifecycle: Register → Login → Search → Book → View → Cancel
- ✅ Authorization requirements
- ✅ Invalid booking attempts
- ✅ User profile retrieval

**Scenarios:**
1. Complete Booking Flow - Flight Booking (Full Integration)
2. Create Booking - Unauthorized (Negative Test)
3. Create Booking - Invalid Flight ID (Negative Test)
4. Get User Profile

### Mock Files

#### `payment-mock.feature`
**Payment Service Simulation**
- Mock payment processing
- Success and failure scenarios
- Transaction ID generation

## Running Tests

### Run All Tests
```bash
cd tests/karate
mvn test
```

### Run Specific Feature
```bash
mvn test -Dkarate.options="classpath:features/auth.feature"
```

### Run with Custom Base URL
```bash
mvn test -Dapi.baseUrl=http://staging.example.com:8000
```

### Run Specific Scenario
```bash
mvn test -Dkarate.options="--tags @smoke"
```

### Generate HTML Report
```bash
mvn test
# Report will be in target/karate-reports/karate-summary.html
```

## Test Data Strategy

### Dynamic Email Generation
Tests use `java.lang.System.currentTimeMillis()` to generate unique emails:
```javascript
* def uniqueEmail = 'testuser' + java.lang.System.currentTimeMillis() + '@example.com'
```

### Chaining Requests
Tests chain requests to simulate real user flows:
```gherkin
# Register → Login → Book → Cancel
Given path '/auth/register'
...
Given path '/auth/login'
...
And def authToken = response.access_token
...
Given path '/bookings'
And header Authorization = 'Bearer ' + authToken
```

## Test Coverage

### Positive Test Cases
- User registration and login
- Token-based authentication
- Flight and hotel search
- Booking creation with valid data
- Booking retrieval
- Booking cancellation
- User profile access

### Negative Test Cases
- Duplicate email registration
- Invalid login credentials
- Unauthorized access attempts
- Invalid flight/hotel IDs
- Missing authentication tokens

### Integration Scenarios
- Complete end-to-end booking flow
- Multi-step user journeys
- State management across requests

## Assertions

Tests validate:
- HTTP status codes (200, 201, 400, 401, 404)
- Response body structure
- Field types and values
- Array lengths
- Null checks
- String contains operations

Example:
```gherkin
Then status 201
And match response.email == uniqueEmail
And match response.access_token == '#notnull'
And match response contains { status: 'pending' }
```

## Configuration

### Base URL
Default: `http://localhost:8000`

Override via:
- System property: `-Dapi.baseUrl=...`
- Environment variable
- karate-config.js

### Timeouts
- Connection timeout: 10 seconds
- Read timeout: 10 seconds

Configured in `karate-config.js`:
```javascript
karate.configure('connectTimeout', 10000);
karate.configure('readTimeout', 10000);
```

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run Karate Tests
  run: |
    cd tests/karate
    mvn test
  env:
    API_BASE_URL: http://localhost:8000
```

### Jenkins Pipeline
```groovy
stage('E2E Tests') {
    steps {
        dir('tests/karate') {
            sh 'mvn clean test'
        }
    }
}
```

## Troubleshooting

### Tests Failing with Connection Refused
- Ensure API is running: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
- Check base URL in karate-config.js

### Authentication Failures
- Verify user database is cleared between test runs
- Check JWT token is correctly extracted and passed

### Flaky Tests
- Increase timeouts in karate-config.js
- Add explicit waits if needed
- Ensure test data isolation

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Data Cleanup**: Use unique identifiers to avoid conflicts
3. **Assertions**: Validate both positive and negative scenarios
4. **Documentation**: Keep feature files readable with clear descriptions
5. **Maintainability**: Use Background sections for common setup

## Further Reading

- [Karate Documentation](https://github.com/karatelabs/karate)
- [Karate Best Practices](https://github.com/karatelabs/karate/wiki/Best-Practices)
- [API Testing Guide](../README.md)
