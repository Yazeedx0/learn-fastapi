import logging
from sqlalchemy.orm import Session 
from app.users.models import User 
from app.users.schemas import UserCreate
from app.core.security import hash_password

logger = logging.getLogger(__name__)


def create_user(db: Session, user_in: UserCreate) -> User:
\
    try:
        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"User created successfully: {user.email}")
        return user
    
    except Exception as e:
        logger.error(f"Error creating user {user_in.email}: {e}")
        db.rollback()
        raise


def get_user_by_email(db: Session, email: str) -> User | None:

    return db.query(User).filter(User.email == email).first()

