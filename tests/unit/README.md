# Unit Tests for Travel Booking API

This directory contains comprehensive unit tests for the Travel Booking API.

## Test Structure

- `test_auth.py` - Authentication tests (registration, login, JWT)
- `test_search.py` - Search functionality tests (flights, hotels)
- `test_bookings.py` - Booking management tests (create, cancel, retrieve)
- `test_users.py` - User profile tests
- `conftest.py` - Pytest configuration and fixtures

## Running Tests

### Run all tests:
```bash
pytest tests/unit/
```

### Run with coverage:
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

### Run specific test file:
```bash
pytest tests/unit/test_auth.py
```

### Run specific test class:
```bash
pytest tests/unit/test_auth.py::TestUserRegistration
```

### Run specific test:
```bash
pytest tests/unit/test_auth.py::TestUserRegistration::test_register_user_success
```

### Run with verbose output:
```bash
pytest tests/unit/ -v
```

### Run tests matching a keyword:
```bash
pytest tests/unit/ -k "booking"
```

## Test Coverage

The unit tests cover:

- ✅ User registration (success, duplicate email, invalid email, missing fields)
- ✅ User login (success, wrong password, non-existent user)
- ✅ JWT authentication (valid, invalid, missing tokens)
- ✅ Flight search (with results, no results, case-insensitive)
- ✅ Hotel search (with results, no results, case-insensitive)
- ✅ Booking creation (flight, hotel, invalid IDs, auth required)
- ✅ Booking retrieval (by ID, user's bookings, non-existent)
- ✅ Booking cancellation (success, non-existent, auth required)
- ✅ Complete booking lifecycle workflows
- ✅ User profile retrieval

## Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov httpx
```
