import pytest
from datetime import datetime, date, timedelta
from app.models.user import User, UserStats
from app.models.course import Skill, Lesson
from app.models.progress import UserLessonCompletion
from app.models.session import LessonSession
from app.services.learner_service import update_streak_for_user, calculate_effective_streak
from app.services.leaderboard_service import get_current_week_start_utc
from app.config import settings

def test_get_learner_me(client, seeded_db):
    """Verify GET /api/v1/learner/me returns complete learner profile and gamification stats."""
    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "duo_learner"
    assert data["display_name"] == "Alex Developer"
    assert data["total_crowns"] == 5  # 5 in Greetings

    stats = data["stats"]
    assert stats["xp"] == 340
    assert stats["hearts"] == 5
    assert stats["max_hearts"] == 5
    assert stats["gems"] == 450
    assert stats["streak"] == 4
    assert stats["next_heart_in_seconds"] is None

# --- AUTH & IMPERSONATION HARDENING TESTS ---

def test_auth_default_user_resolves_to_duo_learner(client, seeded_db):
    """Verify standard requests without override header resolve to duo_learner."""
    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    assert response.json()["username"] == "duo_learner"

def test_auth_user_override_rejected_when_disabled(client, seeded_db, monkeypatch):
    """Verify sending X-User-Id when ALLOW_DEV_USER_OVERRIDE is False returns 403 Forbidden."""
    monkeypatch.setattr(settings, "ALLOW_DEV_USER_OVERRIDE", False)
    response = client.get("/api/v1/learner/me", headers={"X-User-Id": "1"})
    assert response.status_code == 403
    assert "disabled" in response.json()["detail"].lower()

def test_auth_user_override_accepted_when_enabled(client, seeded_db, monkeypatch):
    """Verify sending X-User-Id when ALLOW_DEV_USER_OVERRIDE is True successfully resolves to target user."""
    monkeypatch.setattr(settings, "ALLOW_DEV_USER_OVERRIDE", True)
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    response = client.get("/api/v1/learner/me", headers={"X-User-Id": str(learner.id)})
    assert response.status_code == 200
    assert response.json()["id"] == learner.id

def test_auth_unknown_user_id_404_when_override_enabled(client, seeded_db, monkeypatch):
    """Verify sending non-existent user ID returns 404 when override is enabled."""
    monkeypatch.setattr(settings, "ALLOW_DEV_USER_OVERRIDE", True)
    response = client.get("/api/v1/learner/me", headers={"X-User-Id": "9999"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

# --- HEART REGENERATION TESTS ---

def test_passive_heart_regeneration_no_get_mutation(client, seeded_db):
    """
    Verify deterministic passive heart calculation:
    - 2 lost hearts with 3600 seconds elapsed restores exactly 2 hearts.
    - Database is NOT mutated on GET (remains 2 hearts in SQLite).
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 2
    # 3600 seconds = exactly 2 intervals of 1800s
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(seconds=3600)
    seeded_db.commit()

    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    data = response.json()

    # Passively calculated hearts: 2 + (3600 // 1800) = 4
    assert data["stats"]["hearts"] == 4
    assert 1790 <= data["stats"]["next_heart_in_seconds"] <= 1800

    # Verify zero database mutation on GET
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 2, "Database hearts must NOT mutate on GET requests!"

def test_passive_heart_regeneration_single_interval(client, seeded_db):
    """Verify exactly 1 lost heart is recovered after 1800s."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 4
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(seconds=1800)
    seeded_db.commit()

    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["hearts"] == 5
    assert data["stats"]["next_heart_in_seconds"] is None

def test_passive_heart_regeneration_partial_interval_preserved(client, seeded_db):
    """
    Verify partial intervals are preserved:
    - hearts = 3, elapsed = 2700s (1 interval of 1800s + 900s partial)
    - Effective hearts = 4
    - Time until next heart = ~900 seconds
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 3
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(seconds=2700)
    seeded_db.commit()

    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["hearts"] == 4
    assert 890 <= data["stats"]["next_heart_in_seconds"] <= 905

def test_passive_heart_regeneration_cap_at_max(client, seeded_db):
    """Verify passive regeneration never exceeds max_hearts (5)."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 1
    # 20 hours elapsed = 40 intervals
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(hours=20)
    seeded_db.commit()

    response = client.get("/api/v1/learner/me")
    assert response.status_code == 200
    data = response.json()

    assert data["stats"]["hearts"] == 5
    assert data["stats"]["next_heart_in_seconds"] is None

# --- REFILL & PRACTICE VALIDATION TESTS ---

def test_refill_hearts_gem_deduction_and_persistence(client, seeded_db):
    """
    Verify POST /api/v1/learner/refill-hearts:
    - Deducts 350 gems
    - Restores hearts to 5
    - Persists changes to SQLite database
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 2
    learner.stats.gems = 450
    learner.stats.last_heart_loss_at = datetime.utcnow()
    seeded_db.commit()

    response = client.post("/api/v1/learner/refill-hearts", json={"refill_type": "full_refill"})
    assert response.status_code == 200
    data = response.json()

    assert data["hearts"] == 5
    assert data["gems"] == 100  # 450 - 350

    # Verify database persistence
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 5
    assert learner.stats.gems == 100
    assert learner.stats.last_heart_loss_at is None

def test_refill_hearts_invalid_type_rejected(client, seeded_db):
    """Verify passing an invalid refill_type returns 422 Unprocessable Entity."""
    response = client.post("/api/v1/learner/refill-hearts", json={"refill_type": "partial_refill"})
    assert response.status_code == 422

def test_refill_hearts_already_full_rejected(client, seeded_db):
    """Verify attempting to refill when hearts are already 5 returns 400 Bad Request."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 5
    seeded_db.commit()

    response = client.post("/api/v1/learner/refill-hearts", json={"refill_type": "full_refill"})
    assert response.status_code == 400
    assert "already full" in response.json()["detail"].lower()

def test_refill_hearts_insufficient_gems_rejected(client, seeded_db):
    """Verify attempting to refill with < 350 gems returns 400 Bad Request."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 2
    learner.stats.gems = 150  # < 350
    learner.stats.last_heart_loss_at = datetime.utcnow()
    seeded_db.commit()

    response = client.post("/api/v1/learner/refill-hearts", json={"refill_type": "full_refill"})
    assert response.status_code == 400
    assert "insufficient gems" in response.json()["detail"].lower()

def test_practice_earn_heart_recovers_heart_and_prevents_xp_farming(client, seeded_db):
    """
    Verify POST /api/v1/learner/practice-heart:
    - Increments hearts by 1
    - Rejects blind POST without a completed practice session
    - Awards 1 heart only upon genuine practice completion
    - Awards 0 XP to eliminate API-level XP farming
    - Prevents XP inflation on repeated calls
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 3
    learner.stats.xp = 340
    learner.stats.last_heart_loss_at = datetime.utcnow()
    seeded_db.commit()

    # Blind call without session is rejected!
    blind_response = client.post("/api/v1/learner/practice-heart")
    assert blind_response.status_code == 400
    assert "practice session token required" in blind_response.json()["detail"].lower()

    # 1. Start practice session (hearts 3 -> 4 flow)
    start_resp = client.post("/api/v1/practice/start")
    assert start_resp.status_code == 200
    session_data = start_resp.json()
    token1 = session_data["session_token"]
    exercises = session_data["exercises"]
    assert len(exercises) > 0

    # Answer all exercises
    for ex in exercises:
        ans_resp = client.post(
            f"/api/v1/practice/sessions/{token1}/answer",
            json={"exercise_id": ex["id"], "answer": "Hola"}
        )
        assert ans_resp.status_code == 200

    # Complete practice session 1: hearts 3 -> 4
    comp_resp = client.post(f"/api/v1/practice/sessions/{token1}/complete")
    assert comp_resp.status_code == 200
    assert comp_resp.json()["hearts"] == 4
    assert comp_resp.json()["heart_awarded"] is True

    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 4
    assert learner.stats.xp == 340  # XP unchanged!

    # 2. Practice session 2: hearts 4 -> 5 flow
    start_resp2 = client.post("/api/v1/practice/start")
    assert start_resp2.status_code == 200
    token2 = start_resp2.json()["session_token"]
    for ex in start_resp2.json()["exercises"]:
        client.post(
            f"/api/v1/practice/sessions/{token2}/answer",
            json={"exercise_id": ex["id"], "answer": "Hola"}
        )
    comp_resp2 = client.post(f"/api/v1/practice/sessions/{token2}/complete")
    assert comp_resp2.status_code == 200
    assert comp_resp2.json()["hearts"] == 5

    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 5
    assert learner.stats.xp == 340

    # 3. Third attempt: already full -> start rejected with 400!
    start_resp3 = client.post("/api/v1/practice/start")
    assert start_resp3.status_code == 400
    assert "already full" in start_resp3.json()["detail"].lower()
    seeded_db.refresh(learner.stats)
    assert learner.stats.xp == 340  # Zero XP farmed!

# --- PROGRESSION & TREE TESTS ---

def test_course_tree_structure_and_states(client, seeded_db):
    """
    Verify GET /api/v1/courses/active/tree:
    - Computes full tree with locked, available, and completed states.
    - Unit 1: is_unlocked=True.
    - Unit 2: is_unlocked=False (prerequisite: Unit 1 incomplete).
    - Skill 1 (Greetings): completed (5 crowns).
    - Skill 2 (Food & Drinks): available (2 crowns).
    - Skill 3 (Basic Phrases): locked (0 crowns).
    - Skill 4 (Travel): locked (0 crowns).
    """
    response = client.get("/api/v1/courses/active/tree")
    assert response.status_code == 200
    tree = response.json()

    assert tree["code"] == "es-en"
    assert len(tree["units"]) == 8

    unit1 = tree["units"][0]
    unit2 = tree["units"][1]

    assert unit1["is_unlocked"] is True
    assert unit2["is_unlocked"] is False

    # Skill 1 (Greetings in Unit 1)
    skill1 = unit1["skills"][0]
    assert skill1["title"] == "Greetings"
    assert skill1["crowns"] == 5
    assert skill1["lessons"][0]["status"] == "completed"
    assert skill1["lessons"][1]["status"] == "completed"
    assert skill1["lessons"][2]["status"] == "completed"
    assert skill1["lessons"][3]["status"] == "available"
    assert skill1["lessons"][4]["status"] == "locked"

    # Skill in Unit 2 - locked because Unit 1 is not fully completed
    skill2 = unit2["skills"][0]
    assert skill2["title"] == "Food & Drinks"
    assert skill2["status"] == "locked"
    assert all(lesson["status"] == "locked" for lesson in skill2["lessons"])

    # Unit 6 Checkpoint & Unit 7 Section 2 - locked
    unit6 = tree["units"][5]
    assert unit6["is_checkpoint"] is True
    assert unit6["is_unlocked"] is False

    unit7 = tree["units"][6]
    assert unit7["section_index"] == 2
    assert unit7["is_unlocked"] is False

def test_lesson_status_validation(client, seeded_db):
    """
    Verify GET /api/v1/lessons/{id}/status:
    - Completed lesson can be started.
    - Available lesson can be started.
    - Locked lesson is rejected with can_start: false.
    """
    # Skill 1 Lesson 1 (Completed)
    s1_l1 = seeded_db.query(Lesson).filter(Lesson.order_index == 1).first()
    res_comp = client.get(f"/api/v1/lessons/{s1_l1.id}/status")
    assert res_comp.status_code == 200
    assert res_comp.json()["can_start"] is True
    assert res_comp.json()["status"] == "completed"

    # Locked Lesson in Unit 7 (Travel Basics)
    skill_locked = seeded_db.query(Skill).filter(Skill.title == "Travel Basics").first()
    s_locked_l1 = skill_locked.lessons[0]
    res_locked = client.get(f"/api/v1/lessons/{s_locked_l1.id}/status")
    assert res_locked.status_code == 200
    data_locked = res_locked.json()
    assert data_locked["can_start"] is False
    assert data_locked["status"] == "locked"
    assert "locked" in data_locked["rejection_reason"].lower()

def test_zero_hearts_lesson_rejection(client, seeded_db):
    """Verify that a learner with 0 hearts cannot start an otherwise available lesson."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 0
    learner.stats.last_heart_loss_at = datetime.utcnow()  # no time elapsed
    seeded_db.commit()

    # Skill 1 Lesson 4 is available on path
    s1 = seeded_db.query(Skill).filter(Skill.title == "Greetings").first()
    s1_l4 = s1.lessons[3]

    response = client.get(f"/api/v1/lessons/{s1_l4.id}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["can_start"] is False
    assert "0 hearts" in data["rejection_reason"].lower()

def test_invalid_lesson_id_404(client, seeded_db):
    """Verify querying status of non-existent lesson returns 404 Not Found."""
    response = client.get("/api/v1/lessons/9999/status")
    assert response.status_code == 404

def test_section_navigation_and_prerequisites(client, seeded_db):
    """
    Verify course curriculum section and unit navigation data integrity:
    - Section 1 (Unit 1): order_index=1, contains active playable lesson.
    - Section 2 (Unit 2): order_index=2, contains locked lesson prerequisites.
    - Status validation rejects starting locked lessons in subsequent section.
    """
    tree_resp = client.get("/api/v1/courses/active/tree")
    assert tree_resp.status_code == 200
    tree = tree_resp.json()

    units = tree["units"]
    assert len(units) >= 2

    # Section 1 verification
    section1 = units[0]
    assert section1["order_index"] == 1
    assert "Rookie Basics" in section1["section_title"] or "First Words" in section1["title"]
    s1_lessons = [l for skill in section1["skills"] for l in skill["lessons"]]
    s1_active = [l for l in s1_lessons if l["status"] == "available"]
    assert len(s1_active) > 0, "Section 1 must have an available active lesson to continue"

    # Unit 2 verification & prerequisite locking
    section2 = units[1]
    assert section2["order_index"] == 2
    s2_locked = [l for skill in section2["skills"] for l in skill["lessons"] if l["status"] == "locked"]
    assert len(s2_locked) > 0, "Unit 2 must preserve locked lesson prerequisites"

    # Verify locked lesson cannot be started
    locked_lesson = s2_locked[0]
    status_resp = client.get(f"/api/v1/lessons/{locked_lesson['id']}/status")
    assert status_resp.status_code == 200
    assert status_resp.json()["can_start"] is False

def test_section_2_locked_before_section_1_complete(client, seeded_db):
    """
    Regression Test: Unit 2 and subsequent units must remain locked while Unit 1 is incomplete.
    - Unit 1 has Lessons 4 and 5 incomplete in seed data.
    - Unit 2 is_unlocked is False.
    - Lesson 6 (first lesson in Unit 2: Café Essentials) is locked.
    - Attempting to start Lesson 6 returns 403 Forbidden.
    - Attempting to start a challenge on Lesson 6 returns 403 Forbidden.
    """
    tree_resp = client.get("/api/v1/courses/active/tree")
    assert tree_resp.status_code == 200
    tree = tree_resp.json()

    unit2 = tree["units"][1]
    assert unit2["order_index"] == 2
    assert unit2["is_unlocked"] is False

    for skill in unit2["skills"]:
        assert skill["status"] == "locked"
        for lesson in skill["lessons"]:
            assert lesson["status"] == "locked"

    # Status validation for Lesson 6 (first lesson in Unit 2)
    status_resp = client.get("/api/v1/lessons/6/status")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["can_start"] is False
    assert status_data["status"] == "locked"
    assert "locked" in status_data["rejection_reason"].lower()

    # Starting lesson 6 must be rejected with 403 Forbidden
    start_resp = client.post("/api/v1/lessons/6/start")
    assert start_resp.status_code == 403
    assert "locked" in start_resp.json()["detail"].lower()

    # Starting legendary challenge on lesson 6 must also be rejected with 403 Forbidden
    chal_resp = client.post("/api/v1/challenges/6/start")
    assert chal_resp.status_code == 403
    assert "locked" in chal_resp.json()["detail"].lower()

def test_unit_2_unlocks_after_unit_1_complete(client, seeded_db):
    """
    Regression Test: Unit 2 unlocks dynamically once all Unit 1 lessons (4 and 5) are completed.
    - Completes Lessons 4 and 5.
    - Verifies Unit 2 is_unlocked transitions to True.
    - Food & Drinks transitions to 'available'.
    - Lesson 6 transitions to 'available' with can_start: True.
    - Learner can successfully start Lesson 6 (200 OK).
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()

    for lid in [4, 5]:
        session = LessonSession(
            session_token=f"test-unlock-session-lesson-{lid}",
            user_id=learner.id,
            lesson_id=lid,
            initial_hearts=5,
            current_hearts=5,
            status="completed",
            finished_at=datetime.utcnow(),
        )
        seeded_db.add(session)
        seeded_db.flush()

        comp = UserLessonCompletion(
            session_id=session.id,
            user_id=learner.id,
            lesson_id=lid,
            xp_earned=15,
        )
        seeded_db.add(comp)
    seeded_db.commit()

    # Fetch updated tree
    tree_resp = client.get("/api/v1/courses/active/tree")
    assert tree_resp.status_code == 200
    tree = tree_resp.json()

    unit2 = tree["units"][1]
    assert unit2["order_index"] == 2
    assert unit2["is_unlocked"] is True

    # First skill in Unit 2 should now be available
    skill2 = unit2["skills"][0]
    assert skill2["title"] == "Food & Drinks"
    assert skill2["status"] == "available"

    # First lesson in Skill 2 (Lesson 6) should now be available
    lesson6 = skill2["lessons"][0]
    assert lesson6["id"] == 6
    assert lesson6["status"] == "available"

    # Lesson 6 status check
    status_resp = client.get("/api/v1/lessons/6/status")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    assert status_data["can_start"] is True
    assert status_data["status"] == "available"
    assert status_data["rejection_reason"] is None

    # Starting Lesson 6 succeeds
    start_resp = client.post("/api/v1/lessons/6/start")
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    assert "session_token" in start_data
    assert len(start_data["exercises"]) > 0

def test_section_2_unlocks_after_checkpoint_complete(client, seeded_db):
    """
    Regression Test: Section 2 unlocks dynamically ONLY after all Section 1 lessons (1-25)
    AND the Checkpoint Challenge (Lesson 26) are completed.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()

    # Complete all lessons from 4 to 26
    for lid in range(4, 27):
        session = LessonSession(
            session_token=f"test-unlock-checkpoint-{lid}",
            user_id=learner.id,
            lesson_id=lid,
            initial_hearts=5,
            current_hearts=5,
            status="completed",
            finished_at=datetime.utcnow(),
        )
        seeded_db.add(session)
        seeded_db.flush()

        comp = UserLessonCompletion(
            session_id=session.id,
            user_id=learner.id,
            lesson_id=lid,
            xp_earned=15 if lid < 26 else 50,
        )
        seeded_db.add(comp)
    seeded_db.commit()

    # Fetch updated tree
    tree_resp = client.get("/api/v1/courses/active/tree")
    assert tree_resp.status_code == 200
    tree = tree_resp.json()

    # Section 2 is Unit 7
    unit7 = tree["units"][6]
    assert unit7["section_index"] == 2
    assert unit7["is_unlocked"] is True

    # First skill in Section 2 (Travel Basics)
    skill_travel = unit7["skills"][0]
    assert skill_travel["status"] == "available"

    # First lesson in Section 2 (Lesson 27)
    lesson27 = skill_travel["lessons"][0]
    assert lesson27["id"] == 27
    assert lesson27["status"] == "available"

    # Can start lesson 27
    start_resp = client.post("/api/v1/lessons/27/start")
    assert start_resp.status_code == 200

# --- STREAK TESTS ---

def test_streak_continuation_and_break():
    """
    Unit test streak state machine with Asia/Kolkata date boundaries:
    - Same day: streak unchanged
    - Consecutive day (diff == 1): streak += 1
    - Missed day (diff > 1): streak resets to 1
    """
    stats = UserStats(streak=4, last_streak_date=date(2026, 10, 8))

    # Test 1: Practice on consecutive day (October 9) -> streak = 5
    new_streak = update_streak_for_user(stats, target_date_ist=date(2026, 10, 9))
    assert new_streak == 5
    assert stats.streak == 5
    assert stats.last_streak_date == date(2026, 10, 9)

    # Test 2: Practice again on same day (October 9) -> streak remains 5
    same_day_streak = update_streak_for_user(stats, target_date_ist=date(2026, 10, 9))
    assert same_day_streak == 5
    assert stats.streak == 5

    # Test 3: Next practice is October 11 (missed October 10) -> streak resets to 1
    broken_streak = update_streak_for_user(stats, target_date_ist=date(2026, 10, 11))
    assert broken_streak == 1
    assert stats.streak == 1
    assert stats.last_streak_date == date(2026, 10, 11)

def test_stale_streak_evaluates_to_zero():
    """
    Verify calculate_effective_streak:
    - If user practiced today: streak is active
    - If user practiced yesterday: streak is active
    - If user practiced 2+ days ago: streak is stale and evaluates to 0
    - If user has never practiced: evaluates to 0
    """
    today = date(2026, 10, 15)

    # 1. Practiced today -> active
    stats_today = UserStats(streak=5, last_streak_date=today)
    assert calculate_effective_streak(stats_today, target_date_ist=today) == 5

    # 2. Practiced yesterday -> active (eligible to continue today)
    stats_yesterday = UserStats(streak=5, last_streak_date=date(2026, 10, 14))
    assert calculate_effective_streak(stats_yesterday, target_date_ist=today) == 5

    # 3. Practiced 2 days ago (missed yesterday) -> stale, evaluates to 0
    stats_stale = UserStats(streak=5, last_streak_date=date(2026, 10, 13))
    assert calculate_effective_streak(stats_stale, target_date_ist=today) == 0

    # 4. Never practiced -> 0
    stats_none = UserStats(streak=0, last_streak_date=None)
    assert calculate_effective_streak(stats_none, target_date_ist=today) == 0

# --- LEADERBOARD WEEKLY XP TESTS ---

def test_leaderboard_uses_weekly_xp_not_lifetime_xp(client, seeded_db):
    """
    Verify GET /api/v1/leaderboard:
    - Current learner's leaderboard XP reflects weekly lesson completions (45 XP), NOT lifetime XP (340 XP).
    - Adding a lesson completion this week directly updates weekly XP on leaderboard.
    """
    response = client.get("/api/v1/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert 1 <= data["days_remaining"] <= 7

    rankings = data["rankings"]
    assert len(rankings) == 10

    # Learner starts with 3 seeded completions of 15 XP each = 45 weekly XP
    current_user_entry = next((e for e in rankings if e["is_current_user"] is True), None)
    assert current_user_entry is not None
    assert current_user_entry["xp"] == 45, f"Expected 45 weekly XP, got {current_user_entry['xp']}. Lifetime XP must NOT be used!"

    # Verify descending sort order across all entries
    for i in range(len(rankings) - 1):
        assert rankings[i]["xp"] >= rankings[i + 1]["xp"]
        assert rankings[i]["rank"] == i + 1

    # Simulate learner completing another lesson this week (+15 XP)
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    lesson = seeded_db.query(Lesson).first()
    week_start = get_current_week_start_utc()

    new_session = LessonSession(
        session_token="test_leaderboard_week_sess",
        user_id=learner.id,
        lesson_id=lesson.id,
        initial_hearts=5,
        current_hearts=5,
        status="completed"
    )
    seeded_db.add(new_session)
    seeded_db.flush()

    new_completion = UserLessonCompletion(
        session_id=new_session.id,
        user_id=learner.id,
        lesson_id=lesson.id,
        xp_earned=15,
        completed_at=week_start + timedelta(hours=8)
    )
    seeded_db.add(new_completion)
    seeded_db.commit()

    # Re-fetch leaderboard: weekly XP must now be 45 + 15 = 60!
    response2 = client.get("/api/v1/leaderboard")
    assert response2.status_code == 200
    rankings2 = response2.json()["rankings"]
    updated_entry = next((e for e in rankings2 if e["is_current_user"] is True), None)
    assert updated_entry["xp"] == 60
