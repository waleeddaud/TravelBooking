Here is the comprehensive, refined **`copilot-instructions.md`**.

This version integrates **PostgreSQL** (via SQLAlchemy & Alembic), strictly enforces **Environment Configuration**, mandates **Thorough Testing** (happy path + edge cases), and expands the API surface to cover a complete travel booking lifecycle.

***

# Copilot Instructions — Travel Booking API (FastAPI + PostgreSQL)

This document serves as the **Master Rulebook** for GitHub Copilot. It defines the architecture, folder structure, coding standards, and testing strategies for the **Travel Booking API**.

**Tech Stack:**
*   **Backend:** FastAPI (Python 3.10+)
*   **Database:** PostgreSQL (SQLAlchemy 2.0 + Alembic for migrations)
*   **Testing:** Karate DSL (E2E), Pytest (Unit), Postman (Manual)
*   **Config:** Pydantic Settings (`.env`)

---

# 1. High-Level Architecture

## 1.1 Core Philosophy
*   **OpenAPI-First:** The `openapi.yaml` is the source of truth.
*   **12-Factor App:** Configuration must be strictly separated from code using environment variables.
*   **Repository Pattern:**
    *   **Routes:** Handle HTTP requests/responses only.
    *   **Services:** Handle business logic (validations, calculations).
    *   **Repositories:** Handle direct Database CRUD operations.
*   **Stateless Auth:** JWT (JSON Web Tokens) with `OAuth2PasswordBearer`.

## 1.2 Database Strategy (PostgreSQL)
*   Use **SQLAlchemy 2.0** (ORM).
*   Use **Alembic** for all schema migrations.
*   **Never** create tables using `Base.metadata.create_all()` in production code; always use migrations.
*   Dates must be stored as UTC `DateTime`.
*   Currency must be stored as `Decimal(10, 2)`.

---

# 2. Folder Structure

Copilot must rigorously follow this structure to keep the project maintainable.

```text
travel_api/
│
├── alembic/                   # Database migrations
│   └── versions/
├── alembic.ini
│
├── .env                       # Local secrets (GIT IGNORED)
├── .env.example               # Config template (COMMITTED)
├── .gitignore
├── openapi.yaml
├── README.md
├── requirements.txt
│
├── src/
│   ├── main.py                # App entry point
│   ├── config.py              # Pydantic BaseSettings
│   ├── database.py            # DB Session setup (Engine)
│   ├── dependencies.py        # Common dependencies (get_db, get_current_user)
│   │
│   ├── auth/
│   │   ├── jwt_handler.py
│   │   ├── security.py        # Hashing logic
│   │
│   ├── models/                # SQLAlchemy Models (DB Tables)
│   │   ├── user_model.py
│   │   ├── booking_model.py
│   │   ├── flight_model.py
│   │
│   ├── schemas/               # Pydantic Schemas (Request/Response)
│   │   ├── auth_schema.py
│   │   ├── booking_schema.py
│   │   ├── search_schema.py
│   │
│   ├── repositories/          # CRUD Operations
│   │   ├── user_repo.py
│   │   ├── booking_repo.py
│   │
│   ├── services/              # Business Logic
│   │   ├── auth_service.py
│   │   ├── booking_service.py
│   │
│   └── routes/                # API Endpoints
│       ├── auth.py
│       ├── search.py
│       ├── bookings.py
│       └── users.py
│
├── tests/
│   ├── karate/
│   │   ├── karate-config.js
│   │   ├── features/          # .feature files
│   │   └── mocks/
│   └── unit/                  # Pytest unit tests
│
└── postman/
    └── travel-collection.json
```

---

# 3. Best Practices & Configuration

## 3.1 Environment Variables
Copilot must use `pydantic-settings`. Secrets **never** go into code.

**`src/config.py` Pattern:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "TravelAPI"
    DATABASE_URL: str  # postgresql://user:pass@localhost:5432/travel_db
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 3.2 Output Requirements for Config Files
When generating project scaffolding, Copilot must produce:

**`.env` (Local Development - Do not commit)**
```ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/travel_db
SECRET_KEY=dev_secret_key_change_me
DEBUG=True
```

**`.env.example` (Committed Template)**
```ini
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=
DEBUG=False
```

## 3.3 Coding Standards
1.  **Type Hinting:** Mandatory for all arguments and returns.
    *   *Bad:* `def get_user(id):`
    *   *Good:* `def get_user(user_id: int, db: Session) -> UserResponse:`
2.  **Dependency Injection:** Inject `Session` and `Settings`.
    *   `def create_booking(req: BookingRequest, db: Session = Depends(get_db)):`
3.  **Error Handling:**
    *   Use `HTTPException` in Routes/Services.
    *   Catch `SQLAlchemyError` in Repositories and wrap them in custom exceptions if needed.
4.  **Transaction Management:**
    *   Services should handle `db.commit()` and `db.rollback()`.

---

# 4. API Functionality & Coverage

Copilot must ensure the API covers the full "Search → Book → Pay → Manage" lifecycle.

## 4.1 Auth Module (`/auth`)
*   `POST /auth/register`: Create account. Params: email, password, full_name, phone.
*   `POST /auth/login`: Authenticate. Returns `access_token` (Bearer).
*   `POST /auth/refresh`: Refresh expired token.

## 4.2 User Module (`/users`)
*   `GET /users/me`: Profile details.
*   `PUT /users/me`: Update profile (phone, address).
*   `GET /users/me/bookings`: Booking history with pagination.

## 4.3 Search Module (`/search`)
*   `GET /search/flights`:
    *   Filters: `origin`, `destination`, `date`, `min_price`, `max_price`, `airline`.
*   `GET /search/hotels`:
    *   Filters: `city`, `check_in`, `check_out`, `stars`, `guests`.
*   *Note:* For MVP, search can query the DB, but structure it so it can eventually point to an external provider (Amadeus/Sabre).

## 4.4 Booking Module (`/bookings`)
*   `POST /bookings`: **Initiate** a booking.
    *   Status: `PENDING`.
    *   Body: `flight_id` OR `hotel_id`, list of `passengers` (names, passport info).
*   `GET /bookings/{id}`: View details.
*   `POST /bookings/{id}/payment`: **Confirm** booking.
    *   Body: `payment_token`, `amount`.
    *   Logic: Update status `PENDING` → `CONFIRMED`.
*   `DELETE /bookings/{id}`: **Cancel** booking.
    *   Logic: Only allowed if status is not already cancelled. Triggers refund logic (mock).

---

# 5. Testing Strategy (Thorough)

Copilot must generate tests that go beyond the "happy path."

## 5.1 Karate DSL Rules
1.  **Integration Flow:**
    *   Scenario: Register -> Login -> Search Flight -> Create Booking -> Pay -> Verify Status is 'CONFIRMED'.
2.  **Negative Testing (Mandatory):**
    *   **Auth:** Access protected route without token (Expect 401).
    *   **Validation:** Book flight with past date (Expect 400).
    *   **Logic:** Pay for a booking that is already Cancelled (Expect 400).
    *   **Resource:** Get non-existent booking ID (Expect 404).
3.  **Data Setup:**
    *   Use `callonce` in Karate to create seed data (e.g., insert available flights into DB before testing search).

## 5.2 Postman
*   Update collection with negative test cases (e.g., "Invalid Login").
*   Use "Pre-request Script" to hash passwords if sending raw JSON (optional, better to use environment vars).

---

# 6. Database Implementation Details for Copilot

When asked to implement the database layer:

1.  **Define Models (`src/models/`)**:
    ```python
    class Booking(Base):
        __tablename__ = "bookings"
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        status = Column(Enum("PENDING", "CONFIRMED", "CANCELLED"), default="PENDING")
        total_price = Column(Numeric(10, 2))
        # relationships...
    ```
2.  **Define Repository (`src/repositories/`)**:
    ```python
    def create_booking(db: Session, booking: BookingCreate, user_id: int):
        db_booking = Booking(**booking.dict(), user_id=user_id)
        db.add(db_booking)
        db.flush() # distinct from commit, handled by service
        return db_booking
    ```
3.  **Migrations**:
    *   Copilot should suggest running: `alembic revision --autogenerate -m "create bookings table"`

---

# 7. Final Checklist for Copilot Generation

Before generating code, Copilot must verify:
1.  **Security**: Are passwords hashed? Are routes protected?
2.  **Config**: Is `DATABASE_URL` loaded from `.env`?
3.  **Completeness**: Does the booking flow handle the `payment` step?
4.  **Testing**: Did I generate a negative test case?

**Use these instructions to scaffold, refactor, and extend the Travel Booking API.**