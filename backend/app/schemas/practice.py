from typing import List, Optional, Any
from pydantic import BaseModel, Field
from app.schemas.session import SafeExerciseDTO

class PracticeStartRequest(BaseModel):
    lesson_id: Optional[int] = Field(None, description="Optional specific lesson ID to practice; if omitted, defaults to an eligible completed lesson")

class PracticeStartResponse(BaseModel):
    session_token: str = Field(..., description="Unique practice session token")
    lesson_id: int
    lesson_title: str
    total_exercises: int
    exercises: List[SafeExerciseDTO]
    current_hearts: int
    max_hearts: int

class PracticeAnswerRequest(BaseModel):
    exercise_id: int
    answer: Any

class PracticeAnswerResponse(BaseModel):
    is_correct: bool
    solution: Optional[str] = None
    hearts_remaining: int
    session_failed: bool = False
    is_duplicate: bool = False

class PracticeCompletionResponse(BaseModel):
    status: str
    session_token: str
    hearts: int
    heart_awarded: bool
    message: str
    is_idempotent: bool = False
