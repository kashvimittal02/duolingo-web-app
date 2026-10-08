from typing import Optional, List
from pydantic import BaseModel, Field

class LessonNodeDTO(BaseModel):
    id: int
    order_index: int
    title: str
    xp_reward: int
    status: str = Field(..., description="Lesson state: completed | available | locked")
    is_completed: bool
    completion_count: int

class SkillNodeDTO(BaseModel):
    id: int
    unit_id: int
    order_index: int
    title: str
    icon_name: str
    status: str = Field(..., description="Skill state: completed | available | locked")
    crowns: int
    total_crown_levels: int
    current_lesson_index: int
    lessons: List[LessonNodeDTO]

class UnitNodeDTO(BaseModel):
    id: int
    course_id: int
    order_index: int
    title: str
    description: str
    hex_color: str
    skills: List[SkillNodeDTO]

class CourseTreeResponse(BaseModel):
    course_id: int
    code: str
    title: str
    target_lang: str
    units: List[UnitNodeDTO]

class LessonStatusResponse(BaseModel):
    lesson_id: int
    skill_id: int
    skill_title: str
    status: str
    can_start: bool
    rejection_reason: Optional[str] = None
