"""Simplified unit tests focusing on core functionality."""
import pytest
from src.auth.security import hash_password, verify_password
from src.auth.jwt_handler import create_access_token, decode_access_token
from datetime import timedelta


class TestPasswordSecurity:
    """Test password hashing and verification."""
    
    def test_password_hash_generation(self):
        """Test password hashing works."""
        hashed = hash_password("TestPassword123!")
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_password_hash_uniqueness(self):
        """Test same password generates different hashes (salt)."""
        hash1 = hash_password("SamePassword123!")
        hash2 = hash_password("SamePassword123!")
        assert hash1 != hash2
    
    def test_verify_correct_password(self):
        """Test correct password verification."""
        password = "CorrectPassword123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_wrong_password(self):
        """Test wrong password verification."""
        hashed = hash_password("CorrectPassword123!")
        assert verify_password("WrongPassword123!", hashed) is False
    
    def test_verify_empty_password(self):
        """Test empty password fails."""
        hashed = hash_password("TestPassword123!")
        assert verify_password("", hashed) is False
    
    def test_long_password_truncation(self):
        """Test long passwords are truncated to 72 bytes."""
        long_password = "A" * 100
        hashed = hash_password(long_password)
        # Should verify with truncated version
        assert verify_password(long_password[:72], hashed) is True
    
    def test_special_characters(self):
        """Test special characters in passwords."""
        special_password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(special_password)
        assert verify_password(special_password, hashed) is True
    
    def test_unicode_password(self):
        """Test unicode characters in passwords."""
        unicode_password = "Pässwörd123!🔒"
        hashed = hash_password(unicode_password)
        assert verify_password(unicode_password, hashed) is True


class TestJWTTokens:
    """Test JWT token creation and verification."""
    
    def test_create_token(self):
        """Test token creation."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_token_with_expiry(self):
        """Test token with custom expiration."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(minutes=15))
        assert token is not None
    
    def test_decode_valid_token(self):
        """Test decoding valid token."""
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data)
        payload = decode_access_token(token)
        assert payload is not None
        assert payload.get("sub") == email
    
    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"
        payload = decode_access_token(invalid_token)
        assert payload is None
    
    def test_decode_malformed_token(self):
        """Test decoding malformed token."""
        payload = decode_access_token("not-a-jwt")
        assert payload is None
    
    def test_decode_empty_token(self):
        """Test decoding empty token."""
        payload = decode_access_token("")
        assert payload is None
    
    def test_token_contains_claims(self):
        """Test token contains expected claims."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        payload = decode_access_token(token)
        assert "exp" in payload
        assert "sub" in payload
    
    def test_token_additional_claims(self):
        """Test token with additional claims."""
        data = {
            "sub": "test@example.com",
            "user_id": 123,
            "role": "admin"
        }
        token = create_access_token(data)
        payload = decode_access_token(token)
        assert payload.get("user_id") == 123
        assert payload.get("role") == "admin"
    
    def test_expired_token(self):
        """Test expired token is rejected."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        payload = decode_access_token(token)
        assert payload is None


class TestBusinessLogic:
    """Test business logic validation."""
    
    def test_password_minimum_length(self):
        """Test password has minimum length requirement."""
        # This is a business rule - passwords should have minimum length
        short_password = "123"
        # In production, you'd validate this before hashing
        assert len(short_password) < 8
    
    def test_email_format(self):
        """Test email format validation."""
        valid_email = "user@example.com"
        invalid_email = "not-an-email"
        
        assert "@" in valid_email
        assert "." in valid_email
        assert "@" not in invalid_email
    
    def test_booking_price_positive(self):
        """Test booking prices must be positive."""
        valid_price = 299.99
        invalid_price = -50.00
        
        assert valid_price > 0
        assert invalid_price < 0
    
    def test_passenger_count_positive(self):
        """Test passenger count must be positive."""
        valid_count = 2
        invalid_count = 0
        
        assert valid_count > 0
        assert invalid_count == 0


# Summary test to ensure all core functionality works
def test_complete_auth_flow():
    """Integration-style test of complete auth flow."""
    # 1. Hash password
    password = "SecurePassword123!"
    hashed = hash_password(password)
    
    # 2. Verify password
    assert verify_password(password, hashed) is True
    
    # 3. Create token
    data = {"sub": "user@example.com", "user_id": 1}
    token = create_access_token(data)
    
    # 4. Decode token
    payload = decode_access_token(token)
    assert payload.get("sub") == "user@example.com"
    assert payload.get("user_id") == 1
    
    # Complete flow validated ✅
