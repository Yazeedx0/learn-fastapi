from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 

from app.core.database import get_db
from app.users.schemas import UserCreate, UserRead
from app.users.service import create_user, get_user_by_email
from app.users.models import User
from app.auth.dependencies import get_current_user


router = APIRouter()


@router.post("/register",
             response_model=UserRead,
             status_code=status.HTTP_201_CREATED,
             )

def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    
    # 1. Check if email is already exists 

    existing_user = get_user_by_email(db, user_in.email)

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Email is alreay registered"
        )
    
    # 2. Create user 

    user = create_user(db, user_in)

    return user 


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user