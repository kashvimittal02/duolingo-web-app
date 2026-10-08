from typing import Optional
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import settings

def get_current_user(
    x_user_id: Optional[int] = Header(None, alias="X-User-Id"),
    db: Session = Depends(get_db)
) -> User:
    """
    Returns the active authenticated learner.
    Default behavior resolves to the seeded 'duo_learner'.
    X-User-Id is accepted ONLY when settings.ALLOW_DEV_USER_OVERRIDE is True.
    In normal/production configuration, attempting to override via X-User-Id returns 403 Forbidden.
    """
    if x_user_id is not None:
        if not settings.ALLOW_DEV_USER_OVERRIDE:
            raise HTTPException(
                status_code=403,
                detail="User override via X-User-Id is disabled in this environment."
            )
        user = db.query(User).filter(User.id == x_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User ID {x_user_id} not found")
        return user

    user = db.query(User).filter(User.username == "duo_learner").first()
    if not user:
        # Fallback to first user in database if custom seeded
        user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="Default learner not found. Please seed the database.")
    return user
