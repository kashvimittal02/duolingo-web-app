from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

class SafeExerciseDTO(BaseModel):
    id: int
    order_index: int
    exercise_type: str = Field(..., description="multiple_choice | word_bank | match_pairs | fill_blank | type_answer")
    prompt: str
    prompt_translation: Optional[str] = None
    payload: Dict[str, Any] = Field(..., description="Exercise UI data stripped of all answers and grading keys")
    target_lang: Optional[str] = Field("es", description="Target language code e.g. es, fr, de")

class LessonStartResponse(BaseModel):
    session_token: str
    lesson_id: int
    lesson_title: str
    total_exercises: int
    initial_hearts: int
    current_hearts: int
    exercises: List[SafeExerciseDTO]

class SubmitAnswerRequest(BaseModel):
    exercise_id: int
    answer: Any = Field(..., description="Answer payload: string, token list, or pair mappings")

class AnswerFeedbackResponse(BaseModel):
    is_correct: bool
    feedback_title: str
    correct_solution: str
    remaining_hearts: int
    session_status: str = Field(..., description="in_progress | failed")
    is_duplicate: bool
    completed_exercises: int
    total_exercises: int

class LessonCompletionResponse(BaseModel):
    status: str = "completed"
    session_token: str
    lesson_id: int
    xp_awarded: int
    total_xp: int
    streak: int
    is_replay: bool
    crowns: int
    achievements_unlocked: List[str]
    is_idempotent: bool = False
