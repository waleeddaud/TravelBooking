# Travel Booking API - Development Setup Guide

## Quick Start (Windows)

### Option 1: Using the Startup Script (Recommended)
```cmd
start.bat
```

The script will automatically:
- Create a virtual environment if it doesn't exist
- Install all dependencies
- Set up configuration files
- Start the server

### Option 2: Manual Setup
```cmd
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env and set a secure SECRET_KEY

# 5. Start the server
set PYTHONPATH=%CD%
python -m uvicorn src.main:app --reload
```

## Quick Start (Linux/Mac)

### Option 1: Using the Startup Script (Recommended)
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and set a secure SECRET_KEY

# 5. Start the server
export PYTHONPATH=$(pwd)
python -m uvicorn src.main:app --reload
```

## Accessing the API

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

## Testing the API

### Using Swagger UI (Browser)
1. Navigate to http://localhost:8000/docs
2. Try the endpoints interactively
3. Authentication flow:
   - Register a user at `/auth/register`
   - Login at `/auth/login` to get a token
   - Click "Authorize" button and enter: `Bearer YOUR_TOKEN`
   - Now you can access protected endpoints

### Using Postman
1. Import the collection: `postman/travel-collection.json`
2. Set environment variable `base_url` to `http://localhost:8000`
3. Follow the requests in order:
   - Register User
   - Login User (token auto-saved)
   - Search Flights/Hotels
   - Create Booking
   - View/Cancel Bookings

### Using Karate (Automated Tests)
```bash
cd tests/karate
mvn test
```

## API Workflow Example

### 1. Register a User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"
```

Response: `{"access_token": "YOUR_JWT_TOKEN", "token_type": "bearer"}`

### 3. Search Flights
```bash
curl "http://localhost:8000/search/flights?origin=LHE&destination=DXB"
```

### 4. Create Booking
```bash
curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_type": "flight",
    "item_id": "FL001",
    "passengers": 2,
    "special_requests": "Window seat"
  }'
```

### 5. View Booking History
```bash
curl http://localhost:8000/users/me/bookings \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Project Structure

```
travel_api/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── auth/                # Authentication & security
│   │   ├── jwt_handler.py   # JWT token operations
│   │   └── security.py      # Password hashing
│   ├── schemas/             # Pydantic models
│   │   ├── auth_schema.py
│   │   ├── booking_schema.py
│   │   └── search_schema.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Registration & login
│   │   ├── search.py        # Flight & hotel search
│   │   ├── bookings.py      # Booking management
│   │   └── users.py         # User profile
│   └── services/            # Business logic
│       ├── search_service.py
│       └── booking_service.py
├── tests/
│   └── karate/              # E2E automated tests
├── postman/                 # Manual test collection
├── .env                     # Environment variables (local)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── openapi.yaml             # API specification
```

## Configuration

### Environment Variables (.env)

```env
APP_NAME=TravelAPI
DEBUG=True                    # Set to False in production
SECRET_KEY=your_secret_key    # MUST be changed for security
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**⚠️ Security Note**: Always set a strong, unique `SECRET_KEY` before deploying!

Generate a secure key:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Development Guidelines

### Code Standards
- All functions have type hints
- Pydantic models for request/response validation
- JWT authentication for protected endpoints
- Error handling with try/except blocks
- Never hardcode secrets (use .env)

### Adding New Features
1. Define Pydantic schemas in `src/schemas/`
2. Implement business logic in `src/services/`
3. Create API routes in `src/routes/`
4. Register router in `src/main.py`
5. Update `openapi.yaml`
6. Add Karate tests in `tests/karate/features/`

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Module Not Found Error
Ensure PYTHONPATH is set:
```bash
# Windows
set PYTHONPATH=%CD%

# Linux/Mac
export PYTHONPATH=$(pwd)
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Production Deployment

### Before Deployment
1. Set `DEBUG=False` in `.env`
2. Generate strong `SECRET_KEY`
3. Configure allowed CORS origins in `src/main.py`
4. Set up proper database (replace in-memory storage)
5. Configure HTTPS/SSL
6. Set up monitoring and logging

### Running in Production
```bash
# Use production server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs
- **OpenAPI Spec**: `openapi.yaml`
- **Architecture Guide**: `.github/copilot-instructions.md`

## License
MIT License
