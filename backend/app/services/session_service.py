import json
import secrets
from datetime import datetime
from typing import Any, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import get_utc_now
from app.models.course import Lesson, Skill
from app.models.exercise import Exercise
from app.models.user import User, UserStats
from app.models.session import LessonSession, SessionAnswer
from app.models.progress import UserLessonCompletion, UserSkillProgress
from app.models.gamification import Achievement, UserAchievement
from app.services.learner_service import sync_hearts_on_mutation, update_streak_for_user
from app.services.path_service import validate_lesson_access
from app.services.validator_service import build_safe_exercise_payload, grade_exercise_submission
from app.schemas.session import (
    SafeExerciseDTO,
    LessonStartResponse,
    AnswerFeedbackResponse,
    LessonCompletionResponse,
)

def start_lesson_session(db: Session, user_id: int, lesson_id: int) -> LessonStartResponse:
    """
    Validates learner eligibility, synchronizes passive regeneration,
    generates a secure session token, and creates a LessonSession.
    Returns safe exercises with canonical answers and grading keys stripped.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.stats:
        raise HTTPException(status_code=404, detail="Learner not found")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson ID {lesson_id} not found")

    # Synchronize passive heart regeneration before checking access
    sync_hearts_on_mutation(user.stats)
    db.commit()
    db.refresh(user.stats)

    # Validate lesson access prerequisites
    access = validate_lesson_access(db, user_id, lesson_id)
    if not access.can_start:
        if access.status == "locked":
            raise HTTPException(
                status_code=403,
                detail=access.rejection_reason or "Lesson is locked. Complete preceding lessons to unlock."
            )
        elif user.stats.hearts <= 0:
            raise HTTPException(
                status_code=403,
                detail=access.rejection_reason or "You have 0 hearts. Practice or refill hearts to play."
            )
        else:
            raise HTTPException(
                status_code=403,
                detail=access.rejection_reason or "Cannot start lesson."
            )

    # Generate a cryptographically random, unguessable session token
    token = secrets.token_urlsafe(32)

    new_session = LessonSession(
        session_token=token,
        user_id=user_id,
        lesson_id=lesson_id,
        initial_hearts=user.stats.hearts,
        current_hearts=user.stats.hearts,
        status="in_progress",
        started_at=get_utc_now(),
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Fetch ordered exercises for the lesson
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

    return LessonStartResponse(
        session_token=new_session.session_token,
        lesson_id=lesson.id,
        lesson_title=lesson.title,
        total_exercises=len(safe_exercises),
        initial_hearts=new_session.initial_hearts,
        current_hearts=new_session.current_hearts,
        exercises=safe_exercises,
    )

def submit_session_answer(
    db: Session,
    session_token: str,
    user_id: int,
    exercise_id: int,
    answer_payload: Any,
) -> AnswerFeedbackResponse:
    """
    Grades an exercise submission, handles heart deductions and session failure,
    and guarantees idempotent handling of duplicate submissions.
    """
    session = db.query(LessonSession).filter(LessonSession.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Lesson session not found")

    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this lesson session")

    if session.status == "failed":
        raise HTTPException(status_code=400, detail="Cannot submit answer: this session has failed")

    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Cannot submit answer: this session is already completed")

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail=f"Cannot submit answer: session status is '{session.status}'")

    exercise = db.query(Exercise).filter(
        Exercise.id == exercise_id,
        Exercise.lesson_id == session.lesson_id,
    ).first()
    if not exercise:
        raise HTTPException(status_code=400, detail="Exercise does not belong to this lesson session")

    total_exercises = db.query(Exercise).filter(Exercise.lesson_id == session.lesson_id).count()

    # Fast-path check for existing answer
    existing_answer = db.query(SessionAnswer).filter(
        SessionAnswer.session_id == session.id,
        SessionAnswer.exercise_id == exercise_id,
    ).first()

    if existing_answer is not None:
        completed_exercises = db.query(SessionAnswer).filter(SessionAnswer.session_id == session.id).count()
        return AnswerFeedbackResponse(
            is_correct=existing_answer.is_correct,
            feedback_title="Nicely done!" if existing_answer.is_correct else "Incorrect",
            correct_solution=exercise.canonical_answer,
            remaining_hearts=session.current_hearts,
            session_status=session.status,
            is_duplicate=True,
            completed_exercises=completed_exercises,
            total_exercises=total_exercises,
        )

    # Authoritative grading
    is_correct, canonical_solution = grade_exercise_submission(exercise, answer_payload)

    # Concurrency-safe insert using savepoint
    try:
        with db.begin_nested():
            answer_record = SessionAnswer(
                session_id=session.id,
                exercise_id=exercise_id,
                submitted_answer=json.dumps(answer_payload),
                is_correct=is_correct,
                answered_at=get_utc_now(),
            )
            db.add(answer_record)
            db.flush()
    except IntegrityError:
        # Concurrent duplicate won the race; roll back savepoint and return existing
        db.rollback()
        existing_answer = db.query(SessionAnswer).filter(
            SessionAnswer.session_id == session.id,
            SessionAnswer.exercise_id == exercise_id,
        ).first()
        completed_exercises = db.query(SessionAnswer).filter(SessionAnswer.session_id == session.id).count()
        db.refresh(session)
        user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        current_hearts = user_stats.hearts if user_stats else session.current_hearts
        return AnswerFeedbackResponse(
            is_correct=existing_answer.is_correct if existing_answer else is_correct,
            feedback_title="Nicely done!" if (existing_answer and existing_answer.is_correct) else "Incorrect",
            correct_solution=canonical_solution,
            remaining_hearts=current_hearts,
            session_status=session.status,
            is_duplicate=True,
            completed_exercises=completed_exercises,
            total_exercises=total_exercises,
        )

    # Authoritative state mutation:
    user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if user_stats:
        # 1. Synchronize passive heart regeneration before mutating state
        sync_hearts_on_mutation(user_stats)

        # 2. If incorrect, deduct exactly one heart
        if not is_correct:
            user_stats.hearts = max(0, user_stats.hearts - 1)
            if user_stats.last_heart_loss_at is None:
                user_stats.last_heart_loss_at = get_utc_now()

        # 3. Synchronize session snapshot to authoritative user_stats.hearts
        session.current_hearts = user_stats.hearts

        # 4. If resulting hearts reach 0, mark session as failed
        if session.current_hearts == 0:
            session.status = "failed"
            session.finished_at = get_utc_now()

    db.commit()
    db.refresh(session)
    if user_stats:
        db.refresh(user_stats)

    completed_exercises = db.query(SessionAnswer).filter(SessionAnswer.session_id == session.id).count()

    return AnswerFeedbackResponse(
        is_correct=is_correct,
        feedback_title="Nicely done!" if is_correct else "Incorrect",
        correct_solution=canonical_solution,
        remaining_hearts=session.current_hearts,
        session_status=session.status,
        is_duplicate=False,
        completed_exercises=completed_exercises,
        total_exercises=total_exercises,
    )

def complete_lesson_session(
    db: Session,
    session_token: str,
    user_id: int,
) -> LessonCompletionResponse:
    """
    Atomically transitions a completed session, validates that all exercises were answered,
    records completion, awards XP, advances daily streak and crowns, checks achievements,
    and guarantees idempotent repeat calls.
    """
    session = db.query(LessonSession).filter(LessonSession.session_token == session_token).first()
    if not session:
        raise HTTPException(status_code=404, detail="Lesson session not found")

    if session.user_id != user_id:
        raise HTTPException(status_code=403, detail="You do not have access to this lesson session")

    if session.status == "failed":
        raise HTTPException(status_code=400, detail="Cannot complete a failed session")

    # Idempotent return for already-completed session
    if session.status == "completed":
        completion = db.query(UserLessonCompletion).filter(UserLessonCompletion.session_id == session.id).first()
        user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        lesson = db.query(Lesson).filter(Lesson.id == session.lesson_id).first()
        skill_prog = db.query(UserSkillProgress).filter(
            UserSkillProgress.user_id == user_id,
            UserSkillProgress.skill_id == lesson.skill_id,
        ).first()
        total_completions = db.query(UserLessonCompletion).filter(
            UserLessonCompletion.user_id == user_id,
            UserLessonCompletion.lesson_id == session.lesson_id,
        ).count()
        is_replay = total_completions > 1
        return LessonCompletionResponse(
            status="completed",
            session_token=session.session_token,
            lesson_id=session.lesson_id,
            xp_awarded=completion.xp_earned if completion else settings.BASE_LESSON_XP,
            total_xp=user_stats.xp if user_stats else 0,
            streak=user_stats.streak if user_stats else 1,
            is_replay=is_replay,
            crowns=skill_prog.crowns if skill_prog else 0,
            achievements_unlocked=[],
            is_idempotent=True,
        )

    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail=f"Cannot complete session with status '{session.status}'")

    # Validate that all exercises have been answered
    total_exercises = db.query(Exercise).filter(Exercise.lesson_id == session.lesson_id).count()
    answered_exercises = db.query(SessionAnswer).filter(SessionAnswer.session_id == session.id).count()
    if answered_exercises < total_exercises:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete lesson: only {answered_exercises} of {total_exercises} exercises answered.",
        )

    # Atomic conditional update for SQLite concurrency
    now_dt = get_utc_now()
    result = db.execute(
        text(
            "UPDATE lesson_sessions SET status = 'completed', finished_at = :finished_at "
            "WHERE id = :session_id AND status = 'in_progress'"
        ),
        {"finished_at": now_dt, "session_id": session.id},
    )

    if result.rowcount == 0:
        # Another concurrent request already transitioned the session
        db.refresh(session)
        if session.status == "completed":
            return complete_lesson_session(db, session_token, user_id)
        raise HTTPException(status_code=400, detail="Session state transition failed")

    # Check if first-time completion or replay
    prior_completion = db.query(UserLessonCompletion).filter(
        UserLessonCompletion.user_id == user_id,
        UserLessonCompletion.lesson_id == session.lesson_id,
    ).first()
    is_replay = prior_completion is not None
    xp_awarded = settings.REPLAY_LESSON_XP if is_replay else settings.BASE_LESSON_XP

    # Record UserLessonCompletion
    completion_record = UserLessonCompletion(
        session_id=session.id,
        user_id=user_id,
        lesson_id=session.lesson_id,
        xp_earned=xp_awarded,
        completed_at=now_dt,
    )
    db.add(completion_record)

    # Update UserStats
    user_stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    user_stats.xp += xp_awarded
    update_streak_for_user(user_stats)

    # Update Skill Progress & Crowns
    lesson = db.query(Lesson).filter(Lesson.id == session.lesson_id).first()
    skill = lesson.skill
    skill_prog = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill.id,
    ).first()
    if not skill_prog:
        skill_prog = UserSkillProgress(
            user_id=user_id,
            skill_id=skill.id,
            crowns=0,
            current_lesson_index=0,
            is_completed=False,
        )
        db.add(skill_prog)

    skill_lessons = (
        db.query(Lesson)
        .filter(Lesson.skill_id == skill.id)
        .order_by(Lesson.order_index)
        .all()
    )
    completed_skill_lesson_ids = {
        row[0]
        for row in db.query(UserLessonCompletion.lesson_id)
        .join(Lesson, UserLessonCompletion.lesson_id == Lesson.id)
        .filter(UserLessonCompletion.user_id == user_id, Lesson.skill_id == skill.id)
        .all()
    }
    completed_skill_lesson_ids.add(session.lesson_id)

    all_lessons_in_skill_done = all(l.id in completed_skill_lesson_ids for l in skill_lessons)

    # Advance crowns if all lessons in skill are completed and not a replay
    if not is_replay and all_lessons_in_skill_done:
        if skill_prog.crowns < skill.total_crown_levels:
            skill_prog.crowns += 1
        if skill_prog.crowns >= skill.total_crown_levels:
            skill_prog.is_completed = True

    # Update current_lesson_index
    uncompleted_indices = [
        idx for idx, l in enumerate(skill_lessons) if l.id not in completed_skill_lesson_ids
    ]
    skill_prog.current_lesson_index = uncompleted_indices[0] if uncompleted_indices else len(skill_lessons)

    # Evaluate achievements
    unlocked_achievement_titles: List[str] = []

    # 1. first_lesson: First Steps
    first_ach = db.query(Achievement).filter(Achievement.code == "first_lesson").first()
    if first_ach:
        existing_ua = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == first_ach.id,
        ).first()
        if not existing_ua:
            db.add(UserAchievement(user_id=user_id, achievement_id=first_ach.id, unlocked_at=now_dt))
            unlocked_achievement_titles.append(first_ach.title)

    # 2. streak_3: Wildfire
    if user_stats.streak >= 3:
        streak_ach = db.query(Achievement).filter(Achievement.code == "streak_3").first()
        if streak_ach:
            existing_ua = db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == streak_ach.id,
            ).first()
            if not existing_ua:
                db.add(UserAchievement(user_id=user_id, achievement_id=streak_ach.id, unlocked_at=now_dt))
                unlocked_achievement_titles.append(streak_ach.title)

    # 3. xp_100: Centurion
    if user_stats.xp >= 100:
        xp_ach = db.query(Achievement).filter(Achievement.code == "xp_100").first()
        if xp_ach:
            existing_ua = db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == xp_ach.id,
            ).first()
            if not existing_ua:
                db.add(UserAchievement(user_id=user_id, achievement_id=xp_ach.id, unlocked_at=now_dt))
                unlocked_achievement_titles.append(xp_ach.title)

    # 4. perfect_lesson: Flawless Victory
    if session.current_hearts == session.initial_hearts:
        perf_ach = db.query(Achievement).filter(Achievement.code == "perfect_lesson").first()
        if perf_ach:
            existing_ua = db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == perf_ach.id,
            ).first()
            if not existing_ua:
                db.add(UserAchievement(user_id=user_id, achievement_id=perf_ach.id, unlocked_at=now_dt))
                unlocked_achievement_titles.append(perf_ach.title)

    db.commit()
    db.refresh(session)
    db.refresh(user_stats)
    db.refresh(skill_prog)

    return LessonCompletionResponse(
        status="completed",
        session_token=session.session_token,
        lesson_id=session.lesson_id,
        xp_awarded=xp_awarded,
        total_xp=user_stats.xp,
        streak=user_stats.streak,
        is_replay=is_replay,
        crowns=skill_prog.crowns,
        achievements_unlocked=unlocked_achievement_titles,
        is_idempotent=False,
    )
