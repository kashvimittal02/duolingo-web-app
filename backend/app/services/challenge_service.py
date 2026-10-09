import json
import secrets
from datetime import datetime, timedelta
from typing import Any, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_utc_now
from app.models.course import Lesson
from app.models.exercise import Exercise
from app.models.user import User, UserStats
from app.models.challenge import ChallengeSession, ChallengeAnswer
from app.services.path_service import validate_lesson_access
from app.services.validator_service import build_safe_exercise_payload, grade_exercise_submission
from app.schemas.session import SafeExerciseDTO
from app.schemas.challenge import (
    ChallengeStartResponse,
    ChallengeStatusResponse,
    ChallengeAnswerResponse,
    ChallengeCompletionResponse,
)

DEFAULT_CHALLENGE_TIME_LIMIT = 90  # 90 seconds for 5 exercises

def start_challenge_session(
    db: Session,
    user_id: int,
    lesson_id: int,
    time_limit_seconds: int = DEFAULT_CHALLENGE_TIME_LIMIT,
) -> ChallengeStartResponse:
    """
    Starts an isolated Legendary Timed Challenge session.
    Calculates server-authoritative started_at and expires_at.
    Returns safe exercises stripped of all answers and grading keys.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson ID {lesson_id} not found")

    # Prerequisite validation: lesson must not be locked
    access = validate_lesson_access(db, user_id, lesson_id)
    if access.status == "locked":
        raise HTTPException(
            status_code=403,
            detail="Lesson is locked. Complete preceding lessons before attempting Legendary challenge."
        )

    # Cryptographically secure random token
    token = secrets.token_urlsafe(32)
    started_at = get_utc_now()
    expires_at = started_at + timedelta(seconds=time_limit_seconds)

    challenge = ChallengeSession(
        challenge_token=token,
        user_id=user_id,
        lesson_id=lesson_id,
        time_limit_seconds=time_limit_seconds,
        started_at=started_at,
        expires_at=expires_at,
        status="in_progress",
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    # Fetch ordered exercises
    exercises = (
        db.query(Exercise)
        .filter(Exercise.lesson_id == lesson_id)
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

    remaining_seconds = max(0, int((expires_at - get_utc_now()).total_seconds()))

    return ChallengeStartResponse(
        challenge_token=challenge.challenge_token,
        lesson_id=lesson.id,
        lesson_title=lesson.title,
        time_limit_seconds=time_limit_seconds,
        started_at=started_at,
        expires_at=expires_at,
        remaining_seconds=remaining_seconds,
        total_exercises=len(safe_exercises),
        exercises=safe_exercises,
    )

def get_challenge_session(
    db: Session,
    challenge_token: str,
    user_id: int,
) -> ChallengeStatusResponse:
    """
    Fetches the current authoritative status of an ongoing or finished challenge session.
    Enforces server-side expiry checks even on passive queries.
    """
    challenge = (
        db.query(ChallengeSession)
        .filter(ChallengeSession.challenge_token == challenge_token)
        .first()
    )
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge session not found")

    if challenge.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this challenge session")

    now = get_utc_now()
    is_expired = now > challenge.expires_at

    # Auto-expire if time has elapsed
    if is_expired and challenge.status == "in_progress":
        challenge.status = "timed_out"
        challenge.finished_at = challenge.expires_at
        db.commit()
        db.refresh(challenge)

    remaining_seconds = max(0, int((challenge.expires_at - now).total_seconds()))

    exercises = (
        db.query(Exercise)
        .filter(Exercise.lesson_id == challenge.lesson_id)
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

    completed_exercises = (
        db.query(ChallengeAnswer)
        .filter(ChallengeAnswer.challenge_id == challenge.id)
        .count()
    )

    return ChallengeStatusResponse(
        challenge_token=challenge.challenge_token,
        lesson_id=challenge.lesson_id,
        lesson_title=challenge.lesson.title,
        status=challenge.status,
        time_limit_seconds=challenge.time_limit_seconds,
        remaining_seconds=remaining_seconds,
        is_expired=is_expired,
        completed_exercises=completed_exercises,
        total_exercises=len(safe_exercises),
        current_exercise_index=min(completed_exercises, len(safe_exercises) - 1),
        exercises=safe_exercises,
    )

def submit_challenge_answer(
    db: Session,
    challenge_token: str,
    user_id: int,
    exercise_id: int,
    answer_payload: Any,
) -> ChallengeAnswerResponse:
    """
    Validates deadline before grading.
    Rejects submissions made after server-authoritative expires_at.
    """
    challenge = (
        db.query(ChallengeSession)
        .filter(ChallengeSession.challenge_token == challenge_token)
        .first()
    )
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge session not found")

    if challenge.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this challenge session")

    now = get_utc_now()

    # Server-authoritative deadline check
    if now > challenge.expires_at:
        if challenge.status == "in_progress":
            challenge.status = "timed_out"
            challenge.finished_at = challenge.expires_at
            db.commit()
        raise HTTPException(
            status_code=400,
            detail="Challenge time limit has expired. Answers can no longer be submitted."
        )

    if challenge.status == "timed_out":
        raise HTTPException(status_code=400, detail="Challenge has timed out")

    if challenge.status == "completed":
        raise HTTPException(status_code=400, detail="Challenge is already completed")

    if challenge.status != "in_progress":
        raise HTTPException(status_code=400, detail=f"Challenge status is '{challenge.status}'")

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.lesson_id == challenge.lesson_id,
    ).first()
    if not exercise:
        raise HTTPException(status_code=400, detail="Exercise does not belong to this challenge")

    total_exercises = db.query(Exercise).filter(Exercise.lesson_id == challenge.lesson_id).count()

    # Fast-path check for existing answer
    existing_answer = (
        db.query(ChallengeAnswer)
        .filter(
            ChallengeAnswer.challenge_id == challenge.id,
            ChallengeAnswer.exercise_id == exercise_id,
        )
        .first()
    )
    remaining_seconds = max(0, int((challenge.expires_at - now).total_seconds()))

    if existing_answer:
        completed = db.query(ChallengeAnswer).filter(ChallengeAnswer.challenge_id == challenge.id).count()
        return ChallengeAnswerResponse(
            is_correct=existing_answer.is_correct,
            feedback_title="Nicely done!" if existing_answer.is_correct else "Incorrect",
            correct_solution=exercise.canonical_answer,
            challenge_status=challenge.status,
            remaining_seconds=remaining_seconds,
            is_expired=False,
            is_duplicate=True,
            completed_exercises=completed,
            total_exercises=total_exercises,
        )

    # Authoritative grading
    is_correct, canonical_solution = grade_exercise_submission(exercise, answer_payload)

    try:
        with db.begin_nested():
            record = ChallengeAnswer(
                challenge_id=challenge.id,
                exercise_id=exercise_id,
                submitted_answer=json.dumps(answer_payload),
                is_correct=is_correct,
                answered_at=now,
            )
            db.add(record)
            db.flush()
    except IntegrityError:
        db.rollback()
        existing_answer = (
            db.query(ChallengeAnswer)
            .filter(
                ChallengeAnswer.challenge_id == challenge.id,
                ChallengeAnswer.exercise_id == exercise_id,
            )
            .first()
        )
        completed = db.query(ChallengeAnswer).filter(ChallengeAnswer.challenge_id == challenge.id).count()
        return ChallengeAnswerResponse(
            is_correct=existing_answer.is_correct if existing_answer else is_correct,
            feedback_title="Nicely done!" if (existing_answer and existing_answer.is_correct) else "Incorrect",
            correct_solution=canonical_solution,
            challenge_status=challenge.status,
            remaining_seconds=remaining_seconds,
            is_expired=False,
            is_duplicate=True,
            completed_exercises=completed,
            total_exercises=total_exercises,
        )

    db.commit()
    completed = db.query(ChallengeAnswer).filter(ChallengeAnswer.challenge_id == challenge.id).count()

    return ChallengeAnswerResponse(
        is_correct=is_correct,
        feedback_title="Nicely done!" if is_correct else "Incorrect",
        correct_solution=canonical_solution,
        challenge_status=challenge.status,
        remaining_seconds=remaining_seconds,
        is_expired=False,
        is_duplicate=False,
        completed_exercises=completed,
        total_exercises=total_exercises,
    )

def complete_challenge_session(
    db: Session,
    challenge_token: str,
    user_id: int,
) -> ChallengeCompletionResponse:
    """
    Completes a Legendary Timed Challenge.
    Enforces that submission occurs prior to server deadline.
    Grants a one-time 20 XP Legendary Bonus on first completion (0 XP on repeats to prevent XP farming).
    Guarantees idempotent repeat calls.
    """
    challenge = (
        db.query(ChallengeSession)
        .filter(ChallengeSession.challenge_token == challenge_token)
        .first()
    )
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge session not found")

    if challenge.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this challenge session")

    user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()

    # Idempotent response if already completed
    if challenge.status == "completed":
        time_taken = (
            int((challenge.finished_at - challenge.started_at).total_seconds())
            if challenge.finished_at
            else challenge.time_limit_seconds
        )
        return ChallengeCompletionResponse(
            status="completed",
            challenge_token=challenge.challenge_token,
            lesson_id=challenge.lesson_id,
            xp_awarded=challenge.xp_awarded,
            total_xp=user_stats.xp if user_stats else 0,
            time_taken_seconds=time_taken,
            is_first_completion=challenge.is_first_completion,
            is_idempotent=True,
        )

    now = get_utc_now()

    # Deadline validation
    if now > challenge.expires_at:
        challenge.status = "timed_out"
        challenge.finished_at = challenge.expires_at
        db.commit()
        raise HTTPException(
            status_code=400,
            detail="Cannot complete challenge: time limit has expired."
        )

    total_exercises = db.query(Exercise).filter(Exercise.lesson_id == challenge.lesson_id).count()
    answered_exercises = (
        db.query(ChallengeAnswer)
        .filter(ChallengeAnswer.challenge_id == challenge.id)
        .count()
    )

    if answered_exercises < total_exercises:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete challenge: only {answered_exercises} of {total_exercises} exercises answered."
        )

    # Check for prior completed Legendary challenge for this lesson
    prior_completion = (
        db.query(ChallengeSession)
        .filter(
            ChallengeSession.user_id == user_id,
            ChallengeSession.lesson_id == challenge.lesson_id,
            ChallengeSession.status == "completed",
            ChallengeSession.id != challenge.id,
        )
        .first()
    )

    is_first_completion = prior_completion is None
    xp_awarded = 20 if is_first_completion else 0  # 20 XP bonus on first Legendary completion, 0 XP on repeats

    challenge.status = "completed"
    challenge.finished_at = now
    challenge.xp_awarded = xp_awarded
    challenge.is_first_completion = is_first_completion

    if xp_awarded > 0 and user_stats:
        user_stats.xp += xp_awarded

    db.commit()
    db.refresh(challenge)
    if user_stats:
        db.refresh(user_stats)

    time_taken = max(1, int((now - challenge.started_at).total_seconds()))

    return ChallengeCompletionResponse(
        status="completed",
        challenge_token=challenge.challenge_token,
        lesson_id=challenge.lesson_id,
        xp_awarded=xp_awarded,
        total_xp=user_stats.xp if user_stats else 0,
        time_taken_seconds=time_taken,
        is_first_completion=is_first_completion,
        is_idempotent=False,
    )
