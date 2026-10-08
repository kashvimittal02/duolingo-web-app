from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from app.schemas.session import SafeExerciseDTO

class ChallengeStartResponse(BaseModel):
    challenge_token: str
    lesson_id: int
    lesson_title: str
    time_limit_seconds: int
    started_at: datetime
    expires_at: datetime
    remaining_seconds: int
    total_exercises: int
    exercises: List[SafeExerciseDTO]

class ChallengeStatusResponse(BaseModel):
    challenge_token: str
    lesson_id: int
    lesson_title: str
    status: str
    time_limit_seconds: int
    remaining_seconds: int
    is_expired: bool
    completed_exercises: int
    total_exercises: int
    current_exercise_index: int
    exercises: List[SafeExerciseDTO]

class ChallengeAnswerRequest(BaseModel):
    exercise_id: int
    answer: Any = Field(..., description="Answer payload: string, token list, or pair mappings")

class ChallengeAnswerResponse(BaseModel):
    is_correct: bool
    feedback_title: str
    correct_solution: str
    challenge_status: str
    remaining_seconds: int
    is_expired: bool
    is_duplicate: bool
    completed_exercises: int
    total_exercises: int

class ChallengeCompletionResponse(BaseModel):
    status: str
    challenge_token: str
    lesson_id: int
    xp_awarded: int
    total_xp: int
    time_taken_seconds: int
    is_first_completion: bool
    is_idempotent: bool = False
