from datetime import datetime, date, time, timedelta, timezone
from typing import Tuple, Optional
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config import settings
from app.database import get_utc_now
from app.models.user import User, UserStats
from app.models.progress import UserSkillProgress, UserLessonCompletion
from app.models.gamification import Achievement, UserAchievement
from app.models.challenge import ChallengeSession
from app.schemas.learner import (
    LearnerProfileResponse,
    LearnerStatsDTO,
    AchievementDTO,
    RefillHeartsResponse,
    PracticeHeartResponse,
)

def get_app_timezone():
    """Returns Asia/Kolkata timezone with cross-platform fallback."""
    if ZoneInfo is not None:
        try:
            return ZoneInfo(settings.DEFAULT_TIMEZONE)
        except Exception:
            pass
    return timezone(timedelta(hours=5, minutes=30), name="Asia/Kolkata")


def calculate_passive_hearts(stats: UserStats, now: Optional[datetime] = None) -> Tuple[int, Optional[int]]:
    """
    Computes effective hearts and time to next heart without mutating the database.
    Returns: (effective_hearts, next_heart_in_seconds)
    """
    if stats.hearts >= stats.max_hearts:
        return stats.max_hearts, None

    current_time = now or get_utc_now()
    last_loss = stats.last_heart_loss_at or current_time
    elapsed = max(0.0, (current_time - last_loss).total_seconds())

    regen_interval = float(settings.HEART_REGEN_SECONDS)
    recovered = int(elapsed // regen_interval)
    effective_hearts = min(stats.max_hearts, stats.hearts + recovered)

    if effective_hearts >= stats.max_hearts:
        return stats.max_hearts, None

    next_in_seconds = int(regen_interval - (elapsed % regen_interval))
    return effective_hearts, next_in_seconds

def sync_hearts_on_mutation(stats: UserStats, now: Optional[datetime] = None) -> None:
    """
    Persists passive heart regeneration to the database during mutating actions.
    Adjusts stats.hearts and advances stats.last_heart_loss_at.
    """
    if stats.hearts >= stats.max_hearts:
        stats.last_heart_loss_at = None
        return

    current_time = now or get_utc_now()
    last_loss = stats.last_heart_loss_at or current_time
    elapsed = max(0.0, (current_time - last_loss).total_seconds())
    regen_interval = float(settings.HEART_REGEN_SECONDS)
    recovered = int(elapsed // regen_interval)

    if recovered > 0:
        stats.hearts = min(stats.max_hearts, stats.hearts + recovered)
        if stats.hearts >= stats.max_hearts:
            stats.last_heart_loss_at = None
        else:
            # Advance last_heart_loss_at by the exact number of intervals consumed
            stats.last_heart_loss_at = last_loss + timedelta(seconds=recovered * regen_interval)

def update_streak_for_user(stats: UserStats, target_date_ist: Optional[date] = None) -> int:
    """
    Calculates and updates daily streak in Asia/Kolkata timezone.
    Returns the new streak value.
    """
    tz = get_app_timezone()
    today_ist = target_date_ist or datetime.now(tz).date()
    last_date = stats.last_streak_date

    if last_date is None:
        stats.streak = 1
    elif last_date == today_ist:
        # Already practiced today; maintain streak
        pass
    elif last_date == today_ist - timedelta(days=1):
        # Practiced yesterday; consecutive streak + 1
        stats.streak += 1
    else:
        # Missed at least one calendar day; streak reset
        stats.streak = 1

    stats.last_streak_date = today_ist
    return stats.streak

def calculate_effective_streak(stats: UserStats, target_date_ist: Optional[date] = None) -> int:
    """
    Computes current active streak in Asia/Kolkata timezone.
    If the user has not practiced today or yesterday, the streak is stale and evaluates to 0.
    """
    tz = get_app_timezone()
    today_ist = target_date_ist or datetime.now(tz).date()
    last_date = stats.last_streak_date

    if last_date is None:
        return 0
    if last_date == today_ist or last_date == today_ist - timedelta(days=1):
        return stats.streak
    return 0

def get_learner_profile(db: Session, user_id: int) -> LearnerProfileResponse:
    """
    Retrieves full learner profile and passively calculated gamification stats.
    Read-only: does NOT mutate database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Learner not found")

    stats = user.stats
    if not stats:
        raise HTTPException(status_code=404, detail="Learner stats not found")

    effective_hearts, next_heart_in_sec = calculate_passive_hearts(stats)

    tz = get_app_timezone()
    today_ist = datetime.now(tz).date()
    has_practiced = stats.last_streak_date == today_ist
    effective_streak = calculate_effective_streak(stats, today_ist)

    total_crowns = db.query(func.coalesce(func.sum(UserSkillProgress.crowns), 0)).filter(
        UserSkillProgress.user_id == user.id
    ).scalar()

    # Compute today's XP in Asia/Kolkata (both normal lesson completions and Legendary challenges)
    today_start_ist = datetime.combine(today_ist, time.min).replace(tzinfo=tz)
    today_start_utc = today_start_ist.astimezone(timezone.utc).replace(tzinfo=None)

    daily_lesson_xp = db.query(func.coalesce(func.sum(UserLessonCompletion.xp_earned), 0)).filter(
        UserLessonCompletion.user_id == user.id,
        UserLessonCompletion.completed_at >= today_start_utc
    ).scalar() or 0

    daily_challenge_xp = db.query(func.coalesce(func.sum(ChallengeSession.xp_awarded), 0)).filter(
        ChallengeSession.user_id == user.id,
        ChallengeSession.status == "completed",
        ChallengeSession.finished_at >= today_start_utc
    ).scalar() or 0

    daily_xp = int(daily_lesson_xp) + int(daily_challenge_xp)

    stats_dto = LearnerStatsDTO(
        xp=stats.xp,
        hearts=effective_hearts,
        max_hearts=stats.max_hearts,
        gems=stats.gems,
        streak=effective_streak,
        has_practiced_today=has_practiced,
        next_heart_in_seconds=next_heart_in_sec,
        daily_xp=daily_xp,
        daily_xp_goal=50,
    )

    # Fetch all achievements with unlocked status
    all_achievements = db.query(Achievement).order_by(Achievement.id).all()
    user_ach_map = {ua.achievement_id: ua.unlocked_at for ua in user.achievements}
    achievements_dto = [
        AchievementDTO(
            id=ach.id,
            code=ach.code,
            title=ach.title,
            description=ach.description,
            icon_name=ach.icon_name,
            is_unlocked=(ach.id in user_ach_map),
            unlocked_at=user_ach_map.get(ach.id),
        )
        for ach in all_achievements
    ]

    return LearnerProfileResponse(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        created_at=user.created_at,
        stats=stats_dto,
        total_crowns=total_crowns,
        achievements=achievements_dto,
    )

def refill_hearts_with_gems(db: Session, user_id: int, refill_type: str = "full_refill") -> RefillHeartsResponse:
    """
    Purchases a full heart refill using mock gems.
    Mutates database and deducts gem cost.
    """
    if refill_type != "full_refill":
        raise HTTPException(status_code=400, detail=f"Invalid refill_type '{refill_type}'. Only 'full_refill' is supported.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.stats:
        raise HTTPException(status_code=404, detail="Learner not found")

    stats = user.stats
    # Sync passive hearts before evaluating refill need
    sync_hearts_on_mutation(stats)

    if stats.hearts >= stats.max_hearts:
        raise HTTPException(status_code=400, detail="Hearts are already full!")

    cost = settings.GEM_REFILL_COST
    if stats.gems < cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient gems. Need {cost} gems, but you have {stats.gems}."
        )

    stats.gems -= cost
    stats.hearts = stats.max_hearts
    stats.last_heart_loss_at = None
    db.commit()
    db.refresh(stats)

    return RefillHeartsResponse(
        hearts=stats.hearts,
        gems=stats.gems,
        message="Hearts fully restored to 5!"
    )

def practice_earn_heart(db: Session, user_id: int, session_token: Optional[str] = None) -> PracticeHeartResponse:
    """
    Awards 1 heart only if a valid, completed practice session token is provided.
    Rejects blind requests without a completed practice session.
    """
    if not session_token:
        raise HTTPException(
            status_code=400,
            detail="Practice session token required. You must complete a practice session to earn a heart."
        )

    from app.services.practice_service import complete_practice_session
    comp = complete_practice_session(db, session_token, user_id)
    return PracticeHeartResponse(
        hearts=comp.hearts,
        xp_awarded=0,
        message=comp.message
    )
