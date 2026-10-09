from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.practice import (
    PracticeStartRequest,
    PracticeStartResponse,
    PracticeAnswerRequest,
    PracticeAnswerResponse,
    PracticeCompletionResponse,
)
from app.services.practice_service import (
    start_practice_session,
    submit_practice_answer,
    complete_practice_session,
)

router = APIRouter(prefix="/practice", tags=["Practice & Heart Recovery"])

@router.post("/start", response_model=PracticeStartResponse)
def start_practice(
    payload: PracticeStartRequest = PracticeStartRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Starts a genuine practice session with real exercises.
    Enforces that learner does not already have 5/5 hearts.
    Returns sanitized exercises with canonical answers stripped.
    """
    return start_practice_session(
        db,
        user_id=current_user.id,
        lesson_id=payload.lesson_id,
    )

@router.post("/sessions/{session_token}/answer", response_model=PracticeAnswerResponse)
def submit_answer(
    session_token: str,
    payload: PracticeAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submits an exercise answer for authoritative grading during practice.
    Does NOT deduct hearts on incorrect answers.
    """
    return submit_practice_answer(
        db,
        session_token=session_token,
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        answer_payload=payload.answer,
    )

@router.post("/sessions/{session_token}/complete", response_model=PracticeCompletionResponse)
def complete_practice(
    session_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Completes a practice session and awards exactly 1 heart up to the 5-heart maximum.
    Validates that all exercises were answered.
    Guarantees idempotency against duplicate submissions.
    """
    return complete_practice_session(
        db,
        session_token=session_token,
        user_id=current_user.id,
    )
