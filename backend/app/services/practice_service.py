import json
import secrets
from typing import Optional, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database import get_utc_now
from app.models.course import Lesson
from app.models.exercise import Exercise
from app.models.user import User, UserStats
from app.models.progress import UserLessonCompletion
from app.models.practice import PracticeSession, PracticeAnswer
from app.services.learner_service import sync_hearts_on_mutation, update_streak_for_user
from app.services.validator_service import build_safe_exercise_payload, grade_exercise_submission
from app.schemas.session import SafeExerciseDTO
from app.schemas.practice import (
    PracticeStartResponse,
    PracticeAnswerResponse,
    PracticeCompletionResponse,
)

def start_practice_session(
    db: Session,
    user_id: int,
    lesson_id: Optional[int] = None,
) -> PracticeStartResponse:
    """
    Starts a genuine practice session to earn 1 heart.
    Enforces that hearts must not already be full (5/5).
    Selects an eligible lesson to practice and returns sanitized exercises.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.stats:
        raise HTTPException(status_code=404, detail="Learner not found")

    # Synchronize passive heart regeneration
    sync_hearts_on_mutation(user.stats)
    db.commit()
    db.refresh(user.stats)

    # Enforce five-heart maximum on start
    if user.stats.hearts >= user.stats.max_hearts:
        raise HTTPException(
            status_code=400,
            detail=f"Hearts are already full! You have {user.stats.hearts}/{user.stats.max_hearts} hearts."
        )

    # Determine lesson to practice
    target_lesson: Optional[Lesson] = None
    if lesson_id is not None:
        target_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not target_lesson:
            raise HTTPException(status_code=404, detail=f"Lesson ID {lesson_id} not found")
    else:
        # Prefer a lesson the user has already completed for practice review
        last_completion = (
            db.query(UserLessonCompletion)
            .filter(UserLessonCompletion.user_id == user_id)
            .order_by(UserLessonCompletion.completed_at.desc())
            .first()
        )
        if last_completion:
            target_lesson = db.query(Lesson).filter(Lesson.id == last_completion.lesson_id).first()

        # Fallback to the first lesson in the curriculum
        if not target_lesson:
            target_lesson = db.query(Lesson).order_by(Lesson.id).first()

    if not target_lesson:
        raise HTTPException(status_code=404, detail="No lesson available for practice")

    # Cryptographically secure random session token
    token = secrets.token_urlsafe(32)

    new_session = PracticeSession(
        session_token=token,
        user_id=user_id,
        lesson_id=target_lesson.id,
        status="in_progress",
        heart_awarded=False,
        started_at=get_utc_now(),
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Fetch and sanitize exercises
    exercises = (
        db.query(Exercise)
        .filter(Exercise.lesson_id == target_lesson.id)
        .order_by(Exercise.order_index)
        .all()
    )

    safe_exercises = [
        SafeExerciseDTO(
            id=ex.id,
            order_index=ex.order_index,
            exercise_type=ex.exercise_type,
            prompt=ex.prompt,
            prompt_translation=ex.prompt_translation,
            payload=build_safe_exercise_payload(ex),
        )
        for ex in exercises
    ]

    return PracticeStartResponse(
        session_token=new_session.session_token,
        lesson_id=target_lesson.id,
        lesson_title=target_lesson.title,
        total_exercises=len(safe_exercises),
        exercises=safe_exercises,
        current_hearts=user.stats.hearts,
        max_hearts=user.stats.max_hearts,
    )

def submit_practice_answer(
    db: Session,
    session_token: str,
    user_id: int,
    exercise_id: int,
    answer_payload: Any,
) -> PracticeAnswerResponse:
    """
    Evaluates an answer within a practice session.
    Records answer for completion verification.
    Does NOT deduct hearts on incorrect answers.
    """
    session = (
        db.query(PracticeSession)
        .filter(PracticeSession.session_token == session_token)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Practice session does not belong to user")

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail=f"Cannot submit answer: session status is '{session.status}'")

    exercise = (
        db.query(Exercise)
        .filter(Exercise.id == exercise_id, Exercise.lesson_id == session.lesson_id)
        .first()
    )
    if not exercise:
        raise HTTPException(status_code=400, detail=f"Exercise ID {exercise_id} does not belong to this lesson")

    # Idempotency / Duplicate Check
    existing_answer = (
        db.query(PracticeAnswer)
        .filter(
            PracticeAnswer.session_id == session.id,
            PracticeAnswer.exercise_id == exercise_id,
        )
        .first()
    )
    user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    hearts_remaining = user_stats.hearts if user_stats else 0

    if existing_answer:
        return PracticeAnswerResponse(
            is_correct=existing_answer.is_correct,
            solution=None if existing_answer.is_correct else exercise.canonical_answer,
            hearts_remaining=hearts_remaining,
            session_failed=False,
            is_duplicate=True,
        )

    # Authoritative grading
    is_correct, canonical_solution = grade_exercise_submission(exercise, answer_payload)

    try:
        with db.begin_nested():
            new_answer = PracticeAnswer(
                session_id=session.id,
                exercise_id=exercise_id,
                submitted_answer=json.dumps(answer_payload),
                is_correct=is_correct,
                answered_at=get_utc_now(),
            )
            db.add(new_answer)
            db.flush()
        db.commit()
    except IntegrityError:
        db.rollback()
        existing_answer = (
            db.query(PracticeAnswer)
            .filter(
                PracticeAnswer.session_id == session.id,
                PracticeAnswer.exercise_id == exercise_id,
            )
            .first()
        )
        return PracticeAnswerResponse(
            is_correct=existing_answer.is_correct if existing_answer else is_correct,
            solution=None if (existing_answer and existing_answer.is_correct) else canonical_solution,
            hearts_remaining=hearts_remaining,
            session_failed=False,
            is_duplicate=True,
        )

    return PracticeAnswerResponse(
        is_correct=is_correct,
        solution=None if is_correct else canonical_solution,
        hearts_remaining=hearts_remaining,
        session_failed=False,
        is_duplicate=False,
    )

def complete_practice_session(
    db: Session,
    session_token: str,
    user_id: int,
) -> PracticeCompletionResponse:
    """
    Completes a practice session and awards exactly 1 heart.
    Validates:
    - Session belongs to user
    - All exercises in the lesson were answered
    - Enforces max 5 hearts
    - Idempotent against duplicate requests/replays
    """
    session = (
        db.query(PracticeSession)
        .filter(PracticeSession.session_token == session_token)
        .first()
    )
    if not session:
        raise HTTPException(status_code=404, detail="Practice session not found")

    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Practice session does not belong to user")

    user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not user_stats:
        raise HTTPException(status_code=404, detail="Learner stats not found")

    # Idempotent response if already completed
    if session.status == "completed":
        return PracticeCompletionResponse(
            status="completed",
            session_token=session.session_token,
            hearts=user_stats.hearts,
            heart_awarded=False,
            message="Practice session already completed.",
            is_idempotent=True,
        )

    if session.status != "in_progress":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete practice session with status '{session.status}'"
        )

    # Verification: Validate that ALL exercises in lesson have been answered
    total_exercises = (
        db.query(Exercise)
        .filter(Exercise.lesson_id == session.lesson_id)
        .count()
    )
    answered_exercises = (
        db.query(PracticeAnswer)
        .filter(PracticeAnswer.session_id == session.id)
        .count()
    )

    if answered_exercises < total_exercises:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete practice: only {answered_exercises} of {total_exercises} exercises answered."
        )

    # Concurrency safe state transition
    now_dt = get_utc_now()
    result = db.execute(
        text(
            "UPDATE practice_sessions SET status = 'completed', completed_at = :completed_at "
            "WHERE id = :session_id AND status = 'in_progress'"
        ),
        {"completed_at": now_dt, "session_id": session.id},
    )

    if result.rowcount == 0:
        db.refresh(session)
        if session.status == "completed":
            return PracticeCompletionResponse(
                status="completed",
                session_token=session.session_token,
                hearts=user_stats.hearts,
                heart_awarded=False,
                message="Practice session already completed.",
                is_idempotent=True,
            )
        raise HTTPException(status_code=400, detail="Practice session state transition failed")

    # Sync passive hearts before award
    sync_hearts_on_mutation(user_stats)

    heart_awarded = False
    if user_stats.hearts < user_stats.max_hearts:
        user_stats.hearts += 1
        session.heart_awarded = True
        heart_awarded = True
        if user_stats.hearts >= user_stats.max_hearts:
            user_stats.last_heart_loss_at = None

    # Maintain practice streak
    update_streak_for_user(user_stats)

    db.commit()
    db.refresh(user_stats)

    return PracticeCompletionResponse(
        status="completed",
        session_token=session.session_token,
        hearts=user_stats.hearts,
        heart_awarded=heart_awarded,
        message="Practice completed! Recovered 1 Heart." if heart_awarded else "Practice completed! Hearts are already full.",
        is_idempotent=False,
    )
