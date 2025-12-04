"""Unit tests for JWT token handling."""
import pytest
from datetime import timedelta
from src.auth.jwt_handler import create_access_token, decode_access_token
from src.config import settings


class TestJWTHandler:
    """Test suite for JWT token operations."""
    
    def test_create_access_token(self):
        """Test creating a valid access token."""
        # Arrange
        data = {"sub": "test@example.com"}
        
        # Act
        token = create_access_token(data)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_token_with_custom_expiry(self):
        """Test creating token with custom expiration."""
        # Arrange
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=15)
        
        # Act
        token = create_access_token(data, expires_delta=expires_delta)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
    
    def test_verify_valid_token(self):
        """Test verifying a valid token."""
        # Arrange
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data)
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload.get("sub") == email
    
    def test_verify_invalid_token(self):
        """Test verifying an invalid token."""
        # Arrange
        invalid_token = "invalid.token.here"
        
        # Act
        payload = decode_access_token(invalid_token)
        
        # Assert
        assert payload is None
    
    def test_verify_malformed_token(self):
        """Test verifying a malformed token."""
        # Arrange
        malformed_token = "not-a-jwt-token"
        
        # Act
        payload = decode_access_token(malformed_token)
        
        # Assert
        assert payload is None
    
    def test_verify_empty_token(self):
        """Test verifying an empty token."""
        # Act
        payload = decode_access_token("")
        
        # Assert
        assert payload is None
    
    def test_token_contains_expiry(self):
        """Test that created token contains expiration claim."""
        # Arrange
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert "exp" in payload
        assert "sub" in payload
    
    def test_token_with_additional_claims(self):
        """Test creating token with additional claims."""
        # Arrange
        data = {
            "sub": "test@example.com",
            "user_id": 123,
            "role": "admin"
        }
        token = create_access_token(data)
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is not None
        assert payload.get("sub") == "test@example.com"
        assert payload.get("user_id") == 123
        assert payload.get("role") == "admin"
    
    def test_expired_token_handling(self):
        """Test handling of expired token."""
        # Arrange
        data = {"sub": "test@example.com"}
        # Create token that expires immediately
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        
        # Act
        payload = decode_access_token(token)
        
        # Assert
        assert payload is None  # Expired tokens should be invalid
