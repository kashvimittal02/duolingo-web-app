import pytest
import json
from sqlalchemy.exc import IntegrityError
from app.models.user import User, UserStats
from app.models.course import Course, Unit, Skill, Lesson
from app.models.exercise import Exercise
from app.models.session import LessonSession, SessionAnswer
from app.models.progress import UserLessonCompletion, UserSkillProgress
from app.models.gamification import Achievement, UserAchievement, LeaderboardUser
from app.seeds.seeder import seed_database

def test_seeder_curriculum_integrity(seeded_db):
    """Verify that curriculum hierarchy is accurately created and seeded."""
    courses = seeded_db.query(Course).all()
    assert len(courses) == 1
    course = courses[0]
    assert course.code == "es-en"
    assert course.target_lang == "Spanish"

    units = seeded_db.query(Unit).filter(Unit.course_id == course.id).order_by(Unit.order_index).all()
    assert len(units) == 8
    assert units[0].title == "Unit 1: First Words"
    assert units[1].title == "Unit 2: Everyday Words"
    assert units[5].is_checkpoint is True
    assert units[6].section_index == 2

    skills = seeded_db.query(Skill).all()
    assert len(skills) == 8

    lessons = seeded_db.query(Lesson).all()
    assert len(lessons) == 36

    exercises = seeded_db.query(Exercise).all()
    assert len(exercises) == 180  # 36 lessons * 5 exercises

def test_all_five_exercise_types_present(seeded_db):
    """Verify that every lesson contains all 5 required exercise types."""
    lessons = seeded_db.query(Lesson).all()
    expected_types = {"multiple_choice", "word_bank", "match_pairs", "fill_blank", "type_answer"}

    for lesson in lessons:
        lesson_exercises = seeded_db.query(Exercise).filter(Exercise.lesson_id == lesson.id).all()
        assert len(lesson_exercises) == 5
        types_in_lesson = {ex.exercise_type for ex in lesson_exercises}
        assert types_in_lesson == expected_types, f"Lesson {lesson.id} missing expected exercise types"

        # Verify JSON payloads are valid JSON
        for ex in lesson_exercises:
            parsed = json.loads(ex.payload_json)
            assert isinstance(parsed, dict)
            assert len(ex.canonical_answer) > 0

def test_seeder_learner_integrity(seeded_db):
    """Verify that default learner has correct persistent stats, crowns, and past completions."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    assert learner is not None
    assert learner.display_name == "Alex Developer"

    stats = learner.stats
    assert stats.xp == 340
    assert stats.hearts == 5
    assert stats.max_hearts == 5
    assert stats.gems == 450
    assert stats.streak == 4

    # Verify skill progress
    progress_records = seeded_db.query(UserSkillProgress).filter(UserSkillProgress.user_id == learner.id).all()
    assert len(progress_records) == 8

    # Skill 1 (Greetings) has 5 crowns and is completed
    skill1_progress = [p for p in progress_records if p.crowns == 5]
    assert len(skill1_progress) == 1
    assert skill1_progress[0].is_completed is True

    # Completed lessons audit
    completions = seeded_db.query(UserLessonCompletion).filter(UserLessonCompletion.user_id == learner.id).all()
    assert len(completions) >= 3
    for c in completions:
        assert c.session_id is not None
        assert c.session.status == "completed"

    # User achievements
    user_achs = seeded_db.query(UserAchievement).filter(UserAchievement.user_id == learner.id).all()
    assert len(user_achs) == 3

def test_leaderboard_seeded(seeded_db):
    """Verify seeded competitors exist with staggered weekly XP."""
    competitors = seeded_db.query(LeaderboardUser).order_by(LeaderboardUser.weekly_xp.desc()).all()
    assert len(competitors) == 9
    assert competitors[0].weekly_xp == 620
    assert competitors[-1].weekly_xp == 110

def test_unique_session_completion_constraint(seeded_db):
    """Verify database constraint: each lesson_session can have at most one UserLessonCompletion."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    existing_completion = seeded_db.query(UserLessonCompletion).first()
    assert existing_completion is not None

    # Attempt to insert a second completion referencing the same session_id
    duplicate_completion = UserLessonCompletion(
        session_id=existing_completion.session_id,
        user_id=learner.id,
        lesson_id=existing_completion.lesson_id,
        xp_earned=15
    )
    seeded_db.add(duplicate_completion)
    with pytest.raises(IntegrityError):
        seeded_db.flush()
    seeded_db.rollback()

def test_unique_user_achievement_constraint(seeded_db):
    """Verify database constraint: each achievement can be awarded at most once per user."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    existing_ua = seeded_db.query(UserAchievement).first()
    assert existing_ua is not None

    duplicate_ua = UserAchievement(
        user_id=learner.id,
        achievement_id=existing_ua.achievement_id
    )
    seeded_db.add(duplicate_ua)
    with pytest.raises(IntegrityError):
        seeded_db.flush()
    seeded_db.rollback()

def test_unique_session_exercise_answer_constraint(seeded_db):
    """Verify database constraint: UNIQUE(session_id, exercise_id) on session_answers."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    lesson = seeded_db.query(Lesson).first()
    exercise = lesson.exercises[0]

    session = LessonSession(
        session_token="test_tok_uq_answers",
        user_id=learner.id,
        lesson_id=lesson.id,
        initial_hearts=5,
        current_hearts=5,
        status="in_progress"
    )
    seeded_db.add(session)
    seeded_db.flush()

    ans1 = SessionAnswer(
        session_id=session.id,
        exercise_id=exercise.id,
        submitted_answer="Hola",
        is_correct=True
    )
    seeded_db.add(ans1)
    seeded_db.flush()

    ans2 = SessionAnswer(
        session_id=session.id,
        exercise_id=exercise.id,
        submitted_answer="Hola again",
        is_correct=True
    )
    seeded_db.add(ans2)
    with pytest.raises(IntegrityError):
        seeded_db.flush()
    seeded_db.rollback()

def test_seeder_idempotency(seeded_db):
    """Verify seeder can be executed repeatedly without errors or duplicate rows."""
    count_courses_before = seeded_db.query(Course).count()
    count_exercises_before = seeded_db.query(Exercise).count()
    count_users_before = seeded_db.query(User).count()

    # Re-run seeder without reset
    seed_database(seeded_db, reset=False)

    assert seeded_db.query(Course).count() == count_courses_before
    assert seeded_db.query(Exercise).count() == count_exercises_before
    assert seeded_db.query(User).count() == count_users_before
