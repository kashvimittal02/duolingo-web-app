from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.learner import (
    LearnerProfileResponse,
    RefillHeartsRequest,
    RefillHeartsResponse,
    PracticeHeartRequest,
    PracticeHeartResponse,
)
from app.services.learner_service import (
    get_learner_profile,
    refill_hearts_with_gems,
    practice_earn_heart,
)

router = APIRouter(prefix="/learner", tags=["Learner"])

@router.get("/me", response_model=LearnerProfileResponse)
def read_current_learner(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the authenticated learner's profile and gamification stats.
    Pure read operation: computes passive heart regeneration without mutating the database.
    """
    return get_learner_profile(db, current_user.id)

@router.post("/refill-hearts", response_model=RefillHeartsResponse)
def refill_hearts(
    payload: RefillHeartsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refills hearts to 5 in exchange for 350 gems.
    Mutates the database. Fails if hearts are already full or gems are insufficient.
    """
    return refill_hearts_with_gems(db, current_user.id, payload.refill_type)

@router.post("/practice-heart", response_model=PracticeHeartResponse)
def practice_heart(
    payload: Optional[PracticeHeartRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Awards 1 heart only upon verification of a completed practice session.
    Fails if no session token is provided, if session is incomplete, or if hearts are full.
    """
    token = payload.session_token if payload else None
    return practice_earn_heart(db, current_user.id, session_token=token)
