from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

class AchievementDTO(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon_name: str
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LearnerStatsDTO(BaseModel):
    xp: int = Field(..., ge=0, description="Total accumulated XP")
    hearts: int = Field(..., ge=0, le=5, description="Current effective hearts (passively calculated)")
    max_hearts: int = Field(5, description="Maximum hearts capacity")
    gems: int = Field(..., ge=0, description="Mock gem currency balance")
    streak: int = Field(..., ge=0, description="Current active daily streak")
    has_practiced_today: bool = Field(..., description="Whether learner practiced today in Asia/Kolkata")
    next_heart_in_seconds: Optional[int] = Field(None, description="Seconds until next passive heart regeneration")
    daily_xp: int = Field(0, description="XP earned today in Asia/Kolkata")
    daily_xp_goal: int = Field(50, description="Daily XP goal target")

class LearnerProfileResponse(BaseModel):
    id: int
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    created_at: datetime
    stats: LearnerStatsDTO
    total_crowns: int = Field(..., ge=0, description="Sum of crowns earned across all skills")
    achievements: list[AchievementDTO] = Field(default_factory=list, description="All achievements with unlock status")

    model_config = ConfigDict(from_attributes=True)

class RefillHeartsRequest(BaseModel):
    refill_type: Literal["full_refill"] = Field(
        "full_refill",
        description="Type of heart refill. Only 'full_refill' is supported."
    )

class RefillHeartsResponse(BaseModel):
    hearts: int
    gems: int
    message: str

class PracticeHeartResponse(BaseModel):
    hearts: int
    xp_awarded: int = Field(0, description="XP awarded for practice (0 to prevent heart-farming)")
    message: str
