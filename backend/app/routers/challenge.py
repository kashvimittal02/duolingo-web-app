from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.challenge import (
    ChallengeStartResponse,
    ChallengeStatusResponse,
    ChallengeAnswerRequest,
    ChallengeAnswerResponse,
    ChallengeCompletionResponse,
)
from app.services.challenge_service import (
    start_challenge_session,
    get_challenge_session,
    submit_challenge_answer,
    complete_challenge_session,
)

router = APIRouter(prefix="/challenges", tags=["Legendary Challenges"])

@router.post("/{lesson_id}/start", response_model=ChallengeStartResponse)
def start_challenge(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Starts an isolated Legendary Timed Challenge for a lesson.
    Computes server-authoritative start and deadline timestamps.
    """
    return start_challenge_session(db, current_user.id, lesson_id)

@router.get("/sessions/{challenge_token}", response_model=ChallengeStatusResponse)
def get_challenge_status(
    challenge_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Authoritative query of ongoing challenge progress and remaining time.
    """
    return get_challenge_session(db, challenge_token=challenge_token, user_id=current_user.id)

@router.post("/sessions/{challenge_token}/answer", response_model=ChallengeAnswerResponse)
def submit_answer(
    challenge_token: str,
    payload: ChallengeAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submits an answer within the challenge session.
    Validates deadline server-side; rejects submissions made after expiry.
    """
    return submit_challenge_answer(
        db,
        challenge_token=challenge_token,
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        answer_payload=payload.answer,
    )

@router.post("/sessions/{challenge_token}/complete", response_model=ChallengeCompletionResponse)
def complete_challenge(
    challenge_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Completes a Legendary Challenge if finished before the deadline.
    Grants a one-time 20 XP bonus on first completion (0 XP on repeats to prevent XP farming).
    Guarantees idempotency.
    """
    return complete_challenge_session(
        db,
        challenge_token=challenge_token,
        user_id=current_user.id,
    )
