from typing import Optional, List
from pydantic import BaseModel, Field

class LeaderboardEntry(BaseModel):
    rank: int = Field(..., ge=1, description="1-based competitive leaderboard position")
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    xp: int = Field(..., ge=0, description="Weekly competitive XP")
    is_current_user: bool = Field(False, description="True if entry represents the authenticated learner")

class LeaderboardResponse(BaseModel):
    league_name: str = "Bronze League"
    days_remaining: int = 3
    rankings: List[LeaderboardEntry]
