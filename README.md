# Travel Booking API

A production-ready Travel Booking API built with FastAPI, featuring authentication, flight/hotel search, and booking management.

## Architecture

- **Framework:** FastAPI with async support
- **Authentication:** JWT-based OAuth2 Password Flow
- **Configuration:** Environment variables via `pydantic-settings`
- **Testing:** Karate DSL for E2E + Postman for manual testing
- **Storage:** In-memory (migration-ready for SQL databases)

## Project Structure

```
travel_api/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── auth/                # JWT + password security
│   ├── schemas/             # Pydantic request/response models
│   ├── routes/              # API endpoints
│   └── services/            # Business logic
├── tests/karate/            # E2E automated tests
├── postman/                 # Manual test collections
└── openapi.yaml             # API specification
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and set your secret key:

```bash
copy .env.example .env
```

Edit `.env` and update `SECRET_KEY` with a secure random string.

### 3. Run the API

```bash
uvicorn src.main:app --reload
```

API will be available at: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Search
- `GET /search/flights` - Search flights by origin/destination
- `GET /search/hotels` - Search hotels by city

### Bookings
- `POST /bookings` - Create new booking (requires auth)
- `GET /bookings/{booking_id}` - Get booking details (requires auth)
- `PATCH /bookings/{booking_id}/cancel` - Cancel booking (requires auth)

### User Profile
- `GET /users/me` - Get current user profile (requires auth)
- `GET /users/me/bookings` - Get user's booking history (requires auth)

## Testing

### Manual Testing with Postman
Import `postman/travel-collection.json` into Postman and set the `base_url` environment variable.

### Automated Testing with Karate
```bash
cd tests/karate
mvn test
```

## Development Guidelines

- **Never hardcode secrets** - Always use environment variables
- **Type hints required** - All functions must have type annotations
- **Pydantic models** - Use schemas for all API inputs/outputs
- **Dependency injection** - Use `Depends()` for services and authentication
- **Error handling** - Wrap business logic in try/except blocks

## Security

- Passwords hashed with bcrypt
- JWT tokens with configurable expiration
- Protected routes require valid access token
- CORS enabled for frontend integration

## License

MIT
