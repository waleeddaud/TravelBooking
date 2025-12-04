"""
Authentication service with database integration.

Handles user registration and authentication logic.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.repositories.user_repo import UserRepository
from src.schemas.auth_schema import UserRegister, User
from src.auth.security import hash_password, verify_password
from src.auth.jwt_handler import create_access_token


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            HTTPException: If email already registered
        """
        user_repo = UserRepository(db)
        
        # Check if user already exists
        if user_repo.exists_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = hash_password(user_data.password)
        db_user = user_repo.create(user_data, hashed_password)
        
        return User.model_validate(db_user)
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        """
        Authenticate user and return JWT token.
        
        Args:
            db: Database session
            email: User's email
            password: User's password
            
        Returns:
            JWT access token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        user_repo = UserRepository(db)
        db_user = user_repo.get_by_email(email)
        
        if not db_user or not verify_password(password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": db_user.email})
        return access_token
