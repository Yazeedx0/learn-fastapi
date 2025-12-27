from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from uuid import UUID 


from app.core.database import get_db
from app.auth.security import decode_token
from app.users.models import User 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    
    try: 
        payload = decode_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise ValueError()
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.get(User, UUID(user_id))

    if not user or not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or invalid user"
        )
    
    return user 