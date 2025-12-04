"""
Authentication routes for user registration and login.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.schemas.auth_schema import UserRegister, Token, User, UserInDB
from src.auth.security import hash_password, verify_password
from src.auth.jwt_handler import create_access_token, decode_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

# In-memory user storage
users_db: dict[str, dict] = {}

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user(email: str) -> UserInDB | None:
    """Get user from database by email."""
    user_data = users_db.get(email)
    if user_data:
        return UserInDB(**user_data)
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = get_user(email)
    if user is None:
        raise credentials_exception
    
    return User(email=user.email, full_name=user.full_name, is_active=user.is_active)


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to ensure user is active.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Active user object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, password, full_name)
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already registered
    """
    try:
        # Check if user already exists
        if user_data.email in users_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and store user
        hashed_password = hash_password(user_data.password)
        user_dict = {
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True
        }
        
        users_db[user_data.email] = user_dict
        
        return User(
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and receive JWT access token.
    
    Args:
        form_data: OAuth2 password form (username=email, password)
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Get user by email (username field contains email)
        user = get_user(form_data.username)
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
