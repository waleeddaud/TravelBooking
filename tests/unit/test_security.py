"""Unit tests for security utilities."""
import pytest
from src.auth.security import hash_password, verify_password


class TestSecurity:
    """Test suite for password hashing and verification."""
    
    def test_password_hash_generation(self):
        """Test that password hashing generates a hash."""
        # Act
        hashed = hash_password("TestPassword123!")
        
        # Assert
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != "TestPassword123!"
    
    def test_password_hash_uniqueness(self):
        """Test that same password generates different hashes (due to salt)."""
        # Act
        hash1 = hash_password("SamePassword123!")
        hash2 = hash_password("SamePassword123!")
        
        # Assert
        assert hash1 != hash2  # Different salts
    
    def test_verify_correct_password(self):
        """Test verifying correct password."""
        # Arrange
        password = "CorrectPassword123!"
        hashed = hash_password(password)
        
        # Act
        result = verify_password(password, hashed)
        
        # Assert
        assert result is True
    
    def test_verify_wrong_password(self):
        """Test verifying incorrect password."""
        # Arrange
        correct_password = "CorrectPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(correct_password)
        
        # Act
        result = verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False
    
    def test_verify_empty_password(self):
        """Test verifying empty password."""
        # Arrange
        hashed = hash_password("TestPassword123!")
        
        # Act
        result = verify_password("", hashed)
        
        # Assert
        assert result is False
    
    def test_long_password_handling(self):
        """Test that long passwords are handled correctly."""
        # Arrange
        long_password = "A" * 100  # 100 character password
        hashed = hash_password(long_password)
        
        # Act
        result = verify_password(long_password, hashed)
        
        # Assert
        assert result is True
    
    def test_special_characters_in_password(self):
        """Test passwords with special characters."""
        # Arrange
        special_password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(special_password)
        
        # Act
        result = verify_password(special_password, hashed)
        
        # Assert
        assert result is True
    
    def test_unicode_password(self):
        """Test passwords with unicode characters."""
        # Arrange
        unicode_password = "Pässwörd123!🔒"
        hashed = hash_password(unicode_password)
        
        # Act
        result = verify_password(unicode_password, hashed)
        
        # Assert
        assert result is True
