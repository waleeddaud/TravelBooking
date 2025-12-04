"""
Authentication request and response schemas.
"""

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """User registration request schema."""
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    """User login request schema."""
    username: str  # email
    password: str


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded token data schema."""
    email: str | None = None


class User(BaseModel):
    """User profile response schema."""
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserInDB(User):
    """User model with hashed password for database storage."""
    hashed_password: str
