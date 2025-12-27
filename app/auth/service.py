
from sqlalchemy.orm import Session

from app.users.models import User
from app.core.security import verify_password
from app.auth.security import create_access_token


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> tuple[str, User] | None:
\
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    # Return JWT access token and user object
    access_token = create_access_token(subject=str(user.id))
    return (access_token, user)
