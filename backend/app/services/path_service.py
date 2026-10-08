from typing import Tuple, Optional, Dict, Set
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.course import Course, Unit, Skill, Lesson
from app.models.progress import UserSkillProgress, UserLessonCompletion
from app.models.user import User
from app.services.learner_service import calculate_passive_hearts
from app.schemas.tree import (
    CourseTreeResponse,
    UnitNodeDTO,
    SkillNodeDTO,
    LessonNodeDTO,
    LessonStatusResponse,
)

def get_course_tree_for_learner(db: Session, user_id: int, course_code: str = "es-en") -> CourseTreeResponse:
    """
    Computes the full curriculum tree for the active learner, dynamically calculating
    locked, available, and completed status across units, skills, and lessons.
    """
    course = db.query(Course).filter(Course.code == course_code).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course '{course_code}' not found")

    # Fetch learner's skill progress map
    progress_records = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id
    ).all()
    progress_map: Dict[int, UserSkillProgress] = {p.skill_id: p for p in progress_records}

    # Fetch set of completed lesson IDs for learner
    completions = db.query(UserLessonCompletion.lesson_id).filter(
        UserLessonCompletion.user_id == user_id
    ).all()
    completed_lesson_ids: Set[int] = {c[0] for c in completions}

    # Count of completions per lesson
    completion_counts: Dict[int, int] = {}
    for c in completions:
        completion_counts[c[0]] = completion_counts.get(c[0], 0) + 1

    # Fetch all skills in ordered sequence across all units
    ordered_skills = (
        db.query(Skill)
        .join(Unit, Skill.unit_id == Unit.id)
        .filter(Unit.course_id == course.id)
        .order_by(Unit.order_index, Skill.order_index)
        .all()
    )

    # Determine unlocked status for each skill in sequence
    skill_status_map: Dict[int, str] = {}
    prior_skill_has_crown = True  # First skill is always unlocked

    for idx, skill in enumerate(ordered_skills):
        skill_prog = progress_map.get(skill.id)
        crowns = skill_prog.crowns if skill_prog else 0
        is_completed = skill_prog.is_completed if skill_prog else False

        if not prior_skill_has_crown:
            skill_status_map[skill.id] = "locked"
        else:
            if is_completed or crowns >= skill.total_crown_levels:
                skill_status_map[skill.id] = "completed"
            elif crowns > 0:
                skill_status_map[skill.id] = "available"
            else:
                skill_status_map[skill.id] = "available"

        # Rule: Next skill unlocks if current skill has >= 1 crown or is completed
        prior_skill_has_crown = (crowns >= 1) or is_completed

    # Construct the DTO hierarchy
    units_dto = []
    for unit in course.units:
        skills_dto = []
        for skill in unit.skills:
            skill_status = skill_status_map.get(skill.id, "locked")
            skill_prog = progress_map.get(skill.id)
            crowns = skill_prog.crowns if skill_prog else 0
            curr_lesson_idx = skill_prog.current_lesson_index if skill_prog else 0

            lessons_dto = []
            prior_lesson_completed = True

            for lesson in skill.lessons:
                is_lesson_done = lesson.id in completed_lesson_ids
                count_done = completion_counts.get(lesson.id, 0)

                if skill_status == "locked":
                    lesson_status = "locked"
                else:
                    if is_lesson_done:
                        lesson_status = "completed"
                    elif prior_lesson_completed:
                        lesson_status = "available"
                    else:
                        lesson_status = "locked"

                lessons_dto.append(LessonNodeDTO(
                    id=lesson.id,
                    order_index=lesson.order_index,
                    title=lesson.title,
                    xp_reward=lesson.xp_reward,
                    status=lesson_status,
                    is_completed=is_lesson_done,
                    completion_count=count_done
                ))

                prior_lesson_completed = is_lesson_done

            skills_dto.append(SkillNodeDTO(
                id=skill.id,
                unit_id=skill.unit_id,
                order_index=skill.order_index,
                title=skill.title,
                icon_name=skill.icon_name,
                status=skill_status,
                crowns=crowns,
                total_crown_levels=skill.total_crown_levels,
                current_lesson_index=curr_lesson_idx,
                lessons=lessons_dto
            ))

        units_dto.append(UnitNodeDTO(
            id=unit.id,
            course_id=unit.course_id,
            order_index=unit.order_index,
            title=unit.title,
            description=unit.description,
            hex_color=unit.hex_color,
            skills=skills_dto
        ))

    return CourseTreeResponse(
        course_id=course.id,
        code=course.code,
        title=course.title,
        target_lang=course.target_lang,
        units=units_dto
    )

def validate_lesson_access(db: Session, user_id: int, lesson_id: int) -> LessonStatusResponse:
    """
    Validates whether a learner has eligibility to start a lesson.
    Checks skill lock state, lesson lock state, and hearts > 0.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.stats:
        raise HTTPException(status_code=404, detail="Learner not found")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail=f"Lesson ID {lesson_id} not found")

    # Inspect tree status for this lesson
    tree = get_course_tree_for_learner(db, user_id)
    target_lesson_node: Optional[LessonNodeDTO] = None
    target_skill_title = ""

    for u in tree.units:
        for s in u.skills:
            for l in s.lessons:
                if l.id == lesson_id:
                    target_lesson_node = l
                    target_skill_title = s.title
                    break

    if not target_lesson_node:
        raise HTTPException(status_code=404, detail="Lesson not found in active course tree")

    status = target_lesson_node.status

    if status == "locked":
        return LessonStatusResponse(
            lesson_id=lesson.id,
            skill_id=lesson.skill_id,
            skill_title=target_skill_title,
            status="locked",
            can_start=False,
            rejection_reason="Lesson is locked. Complete preceding lessons to unlock."
        )

    # Check hearts
    effective_hearts, _ = calculate_passive_hearts(user.stats)
    if effective_hearts <= 0:
        return LessonStatusResponse(
            lesson_id=lesson.id,
            skill_id=lesson.skill_id,
            skill_title=target_skill_title,
            status=status,
            can_start=False,
            rejection_reason="You have 0 hearts. Practice or refill hearts to play."
        )

    return LessonStatusResponse(
        lesson_id=lesson.id,
        skill_id=lesson.skill_id,
        skill_title=target_skill_title,
        status=status,
        can_start=True,
        rejection_reason=None
    )
