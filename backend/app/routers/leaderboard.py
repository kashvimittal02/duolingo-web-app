from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.leaderboard import LeaderboardResponse
from app.services.leaderboard_service import get_weekly_leaderboard

router = APIRouter(tags=["Leaderboard"])

@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns weekly competitive league rankings blending seeded competitors
    with the authenticated learner's live XP.
    """
    return get_weekly_leaderboard(db, current_user.id)
