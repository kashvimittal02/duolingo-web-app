from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.session import (
    LessonStartResponse,
    SubmitAnswerRequest,
    AnswerFeedbackResponse,
    LessonCompletionResponse,
)
from app.services.session_service import (
    start_lesson_session,
    submit_session_answer,
    complete_lesson_session,
)

router = APIRouter(prefix="/lessons", tags=["Lessons & Sessions"])

@router.post("/{lesson_id}/start", response_model=LessonStartResponse)
def start_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Starts a new lesson session.
    Validates prerequisite unlock status and available hearts.
    Returns safe exercises with canonical answers stripped.
    """
    return start_lesson_session(db, current_user.id, lesson_id)

@router.post("/sessions/{session_token}/answer", response_model=AnswerFeedbackResponse)
def submit_answer(
    session_token: str,
    payload: SubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Submits an answer for authoritative server grading.
    Deducts hearts on error, handles session failure, and guarantees idempotent duplicate responses.
    """
    return submit_session_answer(
        db,
        session_token=session_token,
        user_id=current_user.id,
        exercise_id=payload.exercise_id,
        answer_payload=payload.answer,
    )

@router.post("/sessions/{session_token}/complete", response_model=LessonCompletionResponse)
def complete_lesson(
    session_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Completes a lesson session atomically.
    Awards XP, updates streak, advances skill progression/crowns, and unlocks eligible achievements.
    """
    return complete_lesson_session(db, session_token=session_token, user_id=current_user.id)
