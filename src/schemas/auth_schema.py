"""
Authentication request and response schemas.
"""

from typing import Optional
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
    email: Optional[str] = None


class User(BaseModel):
    """User profile response schema."""
    id: int
    email: EmailStr
    full_name: str
    is_active: bool = True

    class Config:
        from_attributes = True


class UserInDB(User):
    """User model with hashed password for database storage."""
    hashed_password: str
