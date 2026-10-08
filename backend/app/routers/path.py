from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.tree import CourseTreeResponse, LessonStatusResponse
from app.services.path_service import get_course_tree_for_learner, validate_lesson_access

router = APIRouter(tags=["Curriculum & Path"])

@router.get("/courses/active/tree", response_model=CourseTreeResponse)
def get_active_course_tree(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the complete learning path for the active Spanish course,
    with dynamically evaluated locked, available, and completed states.
    """
    return get_course_tree_for_learner(db, current_user.id, course_code="es-en")

@router.get("/lessons/{lesson_id}/status", response_model=LessonStatusResponse)
def get_lesson_status(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Validates whether the current learner can start a specific lesson.
    Checks skill prerequisites, lesson ordering, and heart availability.
    """
    return validate_lesson_access(db, current_user.id, lesson_id)
