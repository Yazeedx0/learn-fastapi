from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status

from jose import jwt, JWTError
 
from app.core.config import get_settings

settings = get_settings()

def create_access_token(
        
        subject: str, 
        expires_delta: Optional[timedelta] = None,
) -> str: 
    
    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access"
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> dict:

    try: 
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    
        # Validate token type 
        if payload.get("type") != "access": 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        return payload 
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


    