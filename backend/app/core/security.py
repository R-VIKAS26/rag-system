"""
Security configuration and utilities
Implements ADA protocol compliance, JWT authentication, and encryption
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(scheme_name="JWT")


class TokenData(BaseModel):
    """JWT token data"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    scopes: list = []


def setup_security(app: FastAPI) -> None:
    """
    Setup security features including ADA compliance
    """
    logger.info("Setting up security features")
    
    if settings.ENABLE_ADA_COMPLIANCE:
        logger.info("✅ ADA compliance enabled")
    
    if settings.ENCRYPTION_ENABLED:
        logger.info("✅ Encryption enabled")
    
    if settings.AUDIT_LOG_ENABLED:
        logger.info("✅ Audit logging enabled")


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Verify JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        token_data = TokenData(user_id=user_id)
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return token_data


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Get current authenticated user from JWT token
    """
    token = credentials.credentials
    return verify_token(token)


def encrypt_data(data: str) -> str:
    """
    Encrypt sensitive data (placeholder for Fernet encryption)
    """
    if not settings.ENCRYPTION_ENABLED:
        return data
    try:
        import base64
        import hashlib
        from cryptography.fernet import Fernet

        # Derive a 32-byte key from SECRET_KEY using SHA256 and base64-url encode
        raw_key = hashlib.sha256(settings.SECRET_KEY.get_secret_value().encode()).digest()
        fernet_key = base64.urlsafe_b64encode(raw_key)
        f = Fernet(fernet_key)
        token = f.encrypt(data.encode('utf-8'))
        return token.decode('utf-8')
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise


def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data (placeholder for Fernet decryption)
    """
    if not settings.ENCRYPTION_ENABLED:
        return encrypted_data
    try:
        import base64
        import hashlib
        from cryptography.fernet import Fernet

        raw_key = hashlib.sha256(settings.SECRET_KEY.get_secret_value().encode()).digest()
        fernet_key = base64.urlsafe_b64encode(raw_key)
        f = Fernet(fernet_key)
        plaintext = f.decrypt(encrypted_data.encode('utf-8'))
        return plaintext.decode('utf-8')
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise
