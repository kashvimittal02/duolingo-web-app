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
    assert data["total_crowns"] == 7  # 5 in Greetings + 2 in Food & Drinks

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
    - Awards 0 XP to eliminate API-level XP farming
    - Prevents XP inflation on repeated calls
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 3
    learner.stats.xp = 340
    learner.stats.last_heart_loss_at = datetime.utcnow()
    seeded_db.commit()

    # First call: hearts 3 -> 4
    response = client.post("/api/v1/learner/practice-heart")
    assert response.status_code == 200
    data = response.json()
    assert data["hearts"] == 4
    assert data["xp_awarded"] == 0

    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 4
    assert learner.stats.xp == 340  # XP unchanged!

    # Second call: hearts 4 -> 5
    response2 = client.post("/api/v1/learner/practice-heart")
    assert response2.status_code == 200
    assert response2.json()["hearts"] == 5
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 5
    assert learner.stats.xp == 340

    # Third call: already full -> rejected with 400!
    response3 = client.post("/api/v1/learner/practice-heart")
    assert response3.status_code == 400
    assert "already full" in response3.json()["detail"].lower()
    seeded_db.refresh(learner.stats)
    assert learner.stats.xp == 340  # Zero XP farmed!

# --- PROGRESSION & TREE TESTS ---

def test_course_tree_structure_and_states(client, seeded_db):
    """
    Verify GET /api/v1/courses/active/tree:
    - Computes full tree with locked, available, and completed states.
    - Skill 1 (Greetings): completed (5 crowns).
    - Skill 2 (Food & Drinks): available (2 crowns).
    - Skill 3 (Basic Phrases): available (0 crowns).
    - Skill 4 (Travel): locked (0 crowns).
    """
    response = client.get("/api/v1/courses/active/tree")
    assert response.status_code == 200
    tree = response.json()

    assert tree["code"] == "es-en"
    assert len(tree["units"]) == 2

    unit1 = tree["units"][0]
    unit2 = tree["units"][1]

    # Skill 1 (Greetings)
    skill1 = unit1["skills"][0]
    assert skill1["title"] == "Greetings"
    assert skill1["status"] == "completed"
    assert skill1["crowns"] == 5
    assert all(lesson["status"] == "completed" for lesson in skill1["lessons"])

    # Skill 2 (Food & Drinks)
    skill2 = unit1["skills"][1]
    assert skill2["title"] == "Food & Drinks"
    assert skill2["status"] == "available"
    assert skill2["crowns"] == 2
    # Lesson 1 completed, Lesson 2 available
    assert skill2["lessons"][0]["status"] == "completed"
    assert skill2["lessons"][1]["status"] == "available"

    # Skill 3 (Basic Phrases in Unit 2) - unlocked because prior skills progress
    skill3 = unit2["skills"][0]
    assert skill3["title"] == "Basic Phrases"
    assert skill3["status"] == "available"
    assert skill3["lessons"][0]["status"] == "available"
    assert skill3["lessons"][1]["status"] == "locked"

    # Skill 4 (Travel in Unit 2) - locked because Skill 3 has 0 crowns
    skill4 = unit2["skills"][1]
    assert skill4["title"] == "Travel"
    assert skill4["status"] == "locked"
    assert all(lesson["status"] == "locked" for lesson in skill4["lessons"])

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

    # Skill 4 Lesson 1 (Locked)
    skill4 = seeded_db.query(Skill).filter(Skill.title == "Travel").first()
    s4_l1 = skill4.lessons[0]
    res_locked = client.get(f"/api/v1/lessons/{s4_l1.id}/status")
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

    # Skill 2 Lesson 2 is available on path
    skill2 = seeded_db.query(Skill).filter(Skill.title == "Food & Drinks").first()
    s2_l2 = skill2.lessons[1]

    response = client.get(f"/api/v1/lessons/{s2_l2.id}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["can_start"] is False
    assert "0 hearts" in data["rejection_reason"].lower()

def test_invalid_lesson_id_404(client, seeded_db):
    """Verify querying status of non-existent lesson returns 404 Not Found."""
    response = client.get("/api/v1/lessons/9999/status")
    assert response.status_code == 404

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
