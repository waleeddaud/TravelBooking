"""
User repository for database operations.

Handles CRUD operations for User model.
"""

from sqlalchemy.orm import Session
from typing import Optional

from src.models.user_model import User
from src.schemas.auth_schema import UserRegister


class UserRepository:
    """Repository for User database operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, user_data: UserRegister, hashed_password: str) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User registration data
            hashed_password: Hashed password
            
        Returns:
            Created user object
        """
        db_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User's database ID
            
        Returns:
            User object if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def exists_by_email(self, email: str) -> bool:
        """
        Check if user exists by email.
        
        Args:
            email: Email to check
            
        Returns:
            True if user exists, False otherwise
        """
        return self.db.query(User).filter(User.email == email).first() is not None
