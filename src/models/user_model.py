"""
User database model.

SQLAlchemy model for users table.
"""

from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base


class User(Base):
    """User model for database storage."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
