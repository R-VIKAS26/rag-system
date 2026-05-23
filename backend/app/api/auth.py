"""
Authentication endpoints
Implements JWT-based authentication with enterprise security
"""
import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    get_current_user,
    TokenData
)

logger = logging.getLogger(__name__)
router = APIRouter()


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response"""
    access_token: str
    token_type: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class UserResponse(BaseModel):
    """User response"""
    user_id: str
    email: str


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login"
)
async def login(request: LoginRequest) -> LoginResponse:
    """
    Login endpoint
    Returns JWT access token for authenticated user
    """
    logger.info(f"Login attempt for user: {request.email}")
    
    # TODO: Verify credentials against database
    # For now, accept any email/password combination
    
    access_token = create_access_token(
        data={"sub": request.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"Login successful for user: {request.email}")
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post(
    "/signup",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User Sign Up"
)
async def signup(request: LoginRequest) -> LoginResponse:
    """
    Sign up endpoint
    Creates new user and returns JWT access token
    """
    logger.info(f"Sign up attempt for user: {request.email}")
    
    # TODO: Create user in database with hashed password
    hashed_password = hash_password(request.password)
    
    access_token = create_access_token(
        data={"sub": request.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"Sign up successful for user: {request.email}")
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User"
)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user information
    """
    return UserResponse(
        user_id=current_user.user_id,
        email=current_user.user_id  # Assuming user_id is email for now
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User Logout"
)
async def logout(current_user: TokenData = Depends(get_current_user)):
    """
    Logout endpoint
    """
    logger.info(f"User logged out: {current_user.user_id}")
    return {"message": "Successfully logged out"}


@router.post(
    "/refresh",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token"
)
async def refresh_token(
    request: RefreshTokenRequest,
    current_user: TokenData = Depends(get_current_user)
) -> LoginResponse:
    """
    Refresh access token using refresh token
    """
    access_token = create_access_token(
        data={"sub": current_user.user_id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
