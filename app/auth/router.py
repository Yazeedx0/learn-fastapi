from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from app.core.database import get_db
from app.auth.service import authenticate_user

router = APIRouter()



@router.post("/login")
def login(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    
    token = authenticate_user(
        db,
        email = from_data.username,
        password=from_data.password
    )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credntials"
        )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }