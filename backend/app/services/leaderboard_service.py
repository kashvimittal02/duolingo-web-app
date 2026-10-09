from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.gamification import LeaderboardUser
from app.models.user import User
from app.models.progress import UserLessonCompletion
from app.models.challenge import ChallengeSession
from app.schemas.leaderboard import LeaderboardResponse, LeaderboardEntry
from app.services.learner_service import get_app_timezone

def get_current_week_start_utc() -> datetime:
    """
    Computes the start of the current weekly league (Monday at 00:00:00 IST)
    converted to a naive UTC datetime matching database storage.
    """
    tz = get_app_timezone()
    now_ist = datetime.now(tz)
    start_of_week_ist = (now_ist - timedelta(days=now_ist.weekday())).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start_of_week_utc = start_of_week_ist.astimezone(timezone.utc).replace(tzinfo=None)
    return start_of_week_utc

def get_weekly_leaderboard(db: Session, current_user_id: int) -> LeaderboardResponse:
    """
    Combines seeded competitors with the current learner's live weekly XP
    (derived from UserLessonCompletion and ChallengeSession records completed in the current calendar week),
    sorts descending, and assigns 1-based ranking.
    """
    current_user = db.query(User).filter(User.id == current_user_id).first()
    if not current_user or not current_user.stats:
        raise HTTPException(status_code=404, detail="Current learner not found")

    # Calculate current learner's weekly XP strictly from lesson and challenge completions in current week
    week_start_utc = get_current_week_start_utc()
    lesson_weekly_xp = db.query(
        func.coalesce(func.sum(UserLessonCompletion.xp_earned), 0)
    ).filter(
        UserLessonCompletion.user_id == current_user.id,
        UserLessonCompletion.completed_at >= week_start_utc
    ).scalar() or 0

    challenge_weekly_xp = db.query(
        func.coalesce(func.sum(ChallengeSession.xp_awarded), 0)
    ).filter(
        ChallengeSession.user_id == current_user.id,
        ChallengeSession.status == "completed",
        ChallengeSession.finished_at >= week_start_utc
    ).scalar() or 0

    learner_weekly_xp = int(lesson_weekly_xp) + int(challenge_weekly_xp)

    seeded_competitors = db.query(LeaderboardUser).all()

    # Build pool of competitors
    pool = []
    for comp in seeded_competitors:
        pool.append({
            "username": comp.username,
            "display_name": comp.display_name,
            "avatar_url": comp.avatar_url,
            "xp": comp.weekly_xp,
            "is_current_user": False
        })

    # Add active learner with weekly XP
    pool.append({
        "username": current_user.username,
        "display_name": current_user.display_name,
        "avatar_url": current_user.avatar_url or "/mascots/learner_avatar.svg",
        "xp": int(learner_weekly_xp),
        "is_current_user": True
    })

    # Sort descending by weekly XP
    pool.sort(key=lambda x: x["xp"], reverse=True)

    # Assign 1-based ranks
    rankings = []
    for rank_idx, item in enumerate(pool, start=1):
        rankings.append(LeaderboardEntry(
            rank=rank_idx,
            username=item["username"],
            display_name=item["display_name"],
            avatar_url=item["avatar_url"],
            xp=item["xp"],
            is_current_user=item["is_current_user"]
        ))

    return LeaderboardResponse(
        league_name="Bronze League",
        days_remaining=3,
        rankings=rankings
    )
