# Postman Collection - Travel Booking API

Complete Postman collection for manual and automated testing of the Travel Booking API.

## Collection Structure

### 1. Root & Health
- **Root - API Info**: Get API welcome message and version
- **Health Check**: Verify API health status

### 2. Authentication
- **Register User**: Create new user account
- **Login User**: Authenticate and receive JWT token

### 3. Search
- **Search Flights**: Find flights by origin and destination
- **Search Hotels**: Find hotels by city

### 4. Bookings
- **Create Flight Booking**: Book a flight (requires auth)
- **Create Hotel Booking**: Book a hotel (requires auth)
- **Get Booking by ID**: Retrieve booking details (requires auth)
- **Cancel Booking**: Cancel existing booking (requires auth)

### 5. Users
- **Get Current User Profile**: Retrieve authenticated user's profile
- **Get User Booking History**: Retrieve all user's bookings

## Collection Variables

The collection uses the following variables:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `base_url` | API base URL | `http://localhost:8000` |
| `access_token` | JWT authentication token | Auto-set on login |
| `user_email` | Registered user email | Auto-set on registration |
| `booking_id` | Created booking ID | Auto-set on booking creation |

## Quick Start

### 1. Import Collection
1. Open Postman
2. Click **Import**
3. Select `postman/travel-collection.json`
4. Collection will appear in your workspace

### 2. Set Environment
1. Click **Environments** (left sidebar)
2. Create new environment: "Travel API Local"
3. Add variable:
   - Key: `base_url`
   - Value: `http://localhost:8000`
4. Save and select the environment

### 3. Test Flow

**Step 1: Register User**
1. Open `Authentication > Register User`
2. Modify email if needed
3. Click **Send**
4. ✅ Status: 201 Created
5. Email automatically saved to `user_email` variable

**Step 2: Login**
1. Open `Authentication > Login User`
2. Ensure username matches registered email
3. Click **Send**
4. ✅ Status: 200 OK
5. Token automatically saved to `access_token` variable

**Step 3: Search Flights**
1. Open `Search > Search Flights`
2. Modify query params if needed (origin, destination)
3. Click **Send**
4. ✅ Status: 200 OK
5. Review available flights

**Step 4: Create Booking**
1. Open `Bookings > Create Flight Booking`
2. Copy `flight_id` from search results
3. Update `item_id` in request body
4. Click **Send**
5. ✅ Status: 201 Created
6. Booking ID automatically saved to `booking_id` variable

**Step 5: View Booking**
1. Open `Bookings > Get Booking by ID`
2. Click **Send** (uses saved `booking_id`)
3. ✅ Status: 200 OK

**Step 6: Cancel Booking**
1. Open `Bookings > Cancel Booking`
2. Click **Send**
3. ✅ Status: 200 OK
4. Verify status is "cancelled"

## Automated Scripts

The collection includes automated test scripts:

### Pre-request Scripts
Some requests modify data before sending (e.g., generating unique emails).

### Test Scripts
Automatically executed after each request to:
- Validate status codes
- Extract and save variables
- Assert response structure

#### Example: Login Test Script
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.collectionVariables.set('access_token', response.access_token);
}
```

## Request Details

### Authentication Requests

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

#### Login User
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john.doe@example.com
password=SecurePass123!
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Search Requests

#### Search Flights
```
GET /search/flights?origin=LHE&destination=DXB
```

**Response (200):**
```json
[
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
  }
]
```

#### Search Hotels
```
GET /search/hotels?city=Dubai
```

### Booking Requests

#### Create Booking
```
POST /bookings
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "booking_type": "flight",
  "item_id": "FL001",
  "passengers": 2,
  "special_requests": "Window seat preferred"
}
```

**Response (201):**
```json
{
  "booking_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_email": "john.doe@example.com",
  "booking_type": "flight",
  "item_id": "FL001",
  "status": "pending",
  "passengers": 2,
  "special_requests": "Window seat preferred",
  "total_price": 900.00,
  "currency": "USD",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

## Error Handling

### Common Error Codes

| Code | Description | Example Scenario |
|------|-------------|------------------|
| 400 | Bad Request | Invalid email format, booking item not found |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Booking ID doesn't exist |
| 422 | Validation Error | Missing required fields |
| 500 | Server Error | Internal server error |

### Example Error Response
```json
{
  "detail": "Email already registered"
}
```

## Testing Strategies

### Positive Testing
1. Test happy path scenarios
2. Verify successful responses
3. Check data persistence

### Negative Testing
1. Test with invalid data
2. Test unauthorized access
3. Test non-existent resources

### Boundary Testing
1. Maximum passengers
2. Long special requests
3. Edge case dates

## Collection Runner

### Run Entire Collection
1. Click collection name
2. Click **Run**
3. Select environment
4. Click **Run Travel Booking API**
5. Review test results

### Run Specific Folder
1. Right-click folder (e.g., "Authentication")
2. Click **Run folder**

### Export Results
1. After runner completes
2. Click **Export Results**
3. Save as JSON or CSV

## Integration with Newman (CLI)

Run collection from command line:

```bash
# Install Newman
npm install -g newman

# Run collection
newman run postman/travel-collection.json \
  --environment postman/local-environment.json \
  --reporters cli,html \
  --reporter-html-export newman-report.html
```

## Tips and Best Practices

1. **Use Environments**: Create separate environments for dev, staging, production
2. **Variable Management**: Let scripts auto-populate tokens and IDs
3. **Organize Tests**: Group related requests in folders
4. **Add Descriptions**: Document each request's purpose
5. **Version Control**: Commit collection to git for team collaboration
6. **Monitor**: Use Postman Monitors for continuous testing

## Troubleshooting

### Token Expired
- Re-run the Login request to get a fresh token

### Base URL Not Set
- Verify environment is selected
- Check `base_url` variable is set

### Variables Not Saving
- Check Test scripts are enabled
- Verify collection variables are used (not environment)

## Support

For issues or questions:
- Check API documentation: `http://localhost:8000/docs`
- Review [README.md](../../README.md)
- Test with Karate for automated verification
