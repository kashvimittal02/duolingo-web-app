from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal, get_utc_now
from app.models.user import User, UserStats
from app.models.course import Course, Unit, Skill, Lesson
from app.models.exercise import Exercise
from app.models.progress import UserSkillProgress, UserLessonCompletion
from app.models.gamification import Achievement, UserAchievement, LeaderboardUser
from app.models.session import LessonSession
from app.seeds.seed_data import (
    COURSE_DATA,
    ACHIEVEMENTS_DATA,
    LEADERBOARD_USERS_DATA,
    DEFAULT_LEARNER_DATA,
)

def init_db():
    """Create all tables in the SQLite database."""
    Base.metadata.create_all(bind=engine)

def seed_database(db: Session, reset: bool = False):
    """
    Seeds the SQLite database with curriculum, default learner, leaderboard, and achievements.
    Idempotent: skips seeding if already populated unless reset=True.
    """
    if reset:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    else:
        init_db()

    # 1. Seed Achievements
    for ach in ACHIEVEMENTS_DATA:
        existing = db.query(Achievement).filter(Achievement.code == ach["code"]).first()
        if not existing:
            db.add(Achievement(
                code=ach["code"],
                title=ach["title"],
                description=ach["description"],
                icon_name=ach["icon_name"]
            ))
    db.commit()

    # 2. Seed Leaderboard Users
    for lb_user in LEADERBOARD_USERS_DATA:
        existing = db.query(LeaderboardUser).filter(LeaderboardUser.username == lb_user["username"]).first()
        if not existing:
            db.add(LeaderboardUser(
                username=lb_user["username"],
                display_name=lb_user["display_name"],
                avatar_url=lb_user["avatar_url"],
                weekly_xp=lb_user["weekly_xp"]
            ))
    db.commit()

    # 3. Seed Course Curriculum
    course = db.query(Course).filter(Course.code == COURSE_DATA["code"]).first()
    if not course:
        course = Course(
            code=COURSE_DATA["code"],
            title=COURSE_DATA["title"],
            target_lang=COURSE_DATA["target_lang"]
        )
        db.add(course)
        db.flush()

        for unit_data in COURSE_DATA["units"]:
            unit = Unit(
                course_id=course.id,
                order_index=unit_data["order_index"],
                title=unit_data["title"],
                description=unit_data["description"],
                hex_color=unit_data["hex_color"]
            )
            db.add(unit)
            db.flush()

            for skill_data in unit_data["skills"]:
                skill = Skill(
                    unit_id=unit.id,
                    order_index=skill_data["order_index"],
                    title=skill_data["title"],
                    icon_name=skill_data["icon_name"],
                    total_crown_levels=skill_data["total_crown_levels"]
                )
                db.add(skill)
                db.flush()

                for lesson_data in skill_data["lessons"]:
                    lesson = Lesson(
                        skill_id=skill.id,
                        order_index=lesson_data["order_index"],
                        title=lesson_data["title"],
                        xp_reward=lesson_data["xp_reward"]
                    )
                    db.add(lesson)
                    db.flush()

                    for ex_data in lesson_data["exercises"]:
                        exercise = Exercise(
                            lesson_id=lesson.id,
                            order_index=ex_data["order_index"],
                            exercise_type=ex_data["exercise_type"],
                            prompt=ex_data["prompt"],
                            prompt_translation=ex_data["prompt_translation"],
                            canonical_answer=ex_data["canonical_answer"],
                            payload_json=ex_data["payload_json"]
                        )
                        db.add(exercise)
        db.commit()

    # 4. Seed Default Learner & Progress
    learner = db.query(User).filter(User.username == DEFAULT_LEARNER_DATA["username"]).first()
    if not learner:
        learner = User(
            username=DEFAULT_LEARNER_DATA["username"],
            display_name=DEFAULT_LEARNER_DATA["display_name"],
            avatar_url=DEFAULT_LEARNER_DATA["avatar_url"],
            created_at=get_utc_now() - timedelta(days=14)
        )
        db.add(learner)
        db.flush()

        # Yesterday's date for streak continuity
        yesterday_date = date.today() - timedelta(days=1)

        user_stats = UserStats(
            user_id=learner.id,
            xp=DEFAULT_LEARNER_DATA["stats"]["xp"],
            hearts=DEFAULT_LEARNER_DATA["stats"]["hearts"],
            max_hearts=DEFAULT_LEARNER_DATA["stats"]["max_hearts"],
            gems=DEFAULT_LEARNER_DATA["stats"]["gems"],
            streak=DEFAULT_LEARNER_DATA["stats"]["streak"],
            last_streak_date=yesterday_date,
            last_heart_loss_at=None
        )
        db.add(user_stats)
        db.flush()

        # Retrieve skills for initial progress
        all_skills = db.query(Skill).order_by(Skill.id).all()
        if len(all_skills) >= 4:
            s1, s2, s3, s4 = all_skills[0], all_skills[1], all_skills[2], all_skills[3]

            # Skill 1 (Greetings): Completed with 5 crowns
            db.add(UserSkillProgress(
                user_id=learner.id,
                skill_id=s1.id,
                crowns=5,
                current_lesson_index=2,
                is_completed=True
            ))

            # Skill 2 (Food & Drinks): In progress with 2 crowns, 1 lesson done
            db.add(UserSkillProgress(
                user_id=learner.id,
                skill_id=s2.id,
                crowns=2,
                current_lesson_index=1,
                is_completed=False
            ))

            # Skill 3 (Basic Phrases): Unlocked (0 crowns)
            db.add(UserSkillProgress(
                user_id=learner.id,
                skill_id=s3.id,
                crowns=0,
                current_lesson_index=0,
                is_completed=False
            ))

            # Skill 4 (Travel): Locked (0 crowns)
            db.add(UserSkillProgress(
                user_id=learner.id,
                skill_id=s4.id,
                crowns=0,
                current_lesson_index=0,
                is_completed=False
            ))
            db.flush()

            # Record completions for past lessons with associated sessions for strict auditability
            completed_lessons = []
            s1_lessons = db.query(Lesson).filter(Lesson.skill_id == s1.id).order_by(Lesson.order_index).all()
            completed_lessons.extend(s1_lessons)
            s2_lesson1 = db.query(Lesson).filter(Lesson.skill_id == s2.id, Lesson.order_index == 1).first()
            if s2_lesson1:
                completed_lessons.append(s2_lesson1)

            from app.services.leaderboard_service import get_current_week_start_utc
            week_start = get_current_week_start_utc()

            for idx, c_lesson in enumerate(completed_lessons, start=1):
                # Create historical completed session for each completion within current week
                finish_time = week_start + timedelta(hours=idx * 2)
                start_time = finish_time - timedelta(minutes=10)
                hist_session = LessonSession(
                    session_token=f"seed_sess_{learner.id}_{c_lesson.id}_{idx}",
                    user_id=learner.id,
                    lesson_id=c_lesson.id,
                    initial_hearts=5,
                    current_hearts=5,
                    status="completed",
                    started_at=start_time,
                    finished_at=finish_time
                )
                db.add(hist_session)
                db.flush()

                db.add(UserLessonCompletion(
                    session_id=hist_session.id,
                    user_id=learner.id,
                    lesson_id=c_lesson.id,
                    xp_earned=15,
                    completed_at=hist_session.finished_at
                ))

        # Award default achievements
        ach_first = db.query(Achievement).filter(Achievement.code == "first_lesson").first()
        ach_streak = db.query(Achievement).filter(Achievement.code == "streak_3").first()
        ach_xp = db.query(Achievement).filter(Achievement.code == "xp_100").first()

        for ach in [ach_first, ach_streak, ach_xp]:
            if ach:
                db.add(UserAchievement(
                    user_id=learner.id,
                    achievement_id=ach.id,
                    unlocked_at=get_utc_now() - timedelta(days=2)
                ))

        db.commit()

if __name__ == "__main__":
    import sys
    db = SessionLocal()
    try:
        reset_flag = "--reset" in sys.argv
        print(f"[*] Running database seeder (reset={reset_flag})...")
        seed_database(db, reset=reset_flag)
        print("[+] Database seeding completed successfully!")
    finally:
        db.close()
