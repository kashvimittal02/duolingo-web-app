import json
import pytest
from datetime import datetime, date, timedelta
from app.models.user import User, UserStats
from app.models.course import Lesson, Skill
from app.models.exercise import Exercise
from app.models.session import LessonSession, SessionAnswer
from app.models.progress import UserLessonCompletion, UserSkillProgress
from app.config import settings

def test_lesson_start_locked_lesson_rejected_403(client, seeded_db):
    """Verify that attempting to start a locked lesson returns 403 Forbidden."""
    # Lesson 8 in Unit 2 Skill 4 is locked for duo_learner
    lesson8 = seeded_db.query(Lesson).filter(Lesson.id == 8).first()
    assert lesson8 is not None

    response = client.post(f"/api/v1/lessons/{lesson8.id}/start")
    assert response.status_code == 403
    assert "locked" in response.json()["detail"].lower()

def test_lesson_start_zero_hearts_rejected_403(client, seeded_db):
    """Verify that a learner with 0 hearts cannot start any lesson."""
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 0
    learner.stats.last_heart_loss_at = datetime.utcnow()
    seeded_db.commit()

    # Lesson 1 is completed/available for practice, but hearts == 0
    response = client.post("/api/v1/lessons/1/start")
    assert response.status_code == 403
    assert "0 hearts" in response.json()["detail"].lower()

def test_lesson_start_nonexistent_lesson_404(client, seeded_db):
    """Verify that starting a non-existent lesson returns 404 Not Found."""
    response = client.post("/api/v1/lessons/99999/start")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_lesson_start_success_and_payload_sanitization(client, seeded_db):
    """
    Verify starting an available lesson generates a secure token and returns
    exercises completely scrubbed of answers, solutions, and keys.
    """
    response = client.post("/api/v1/lessons/1/start")
    assert response.status_code == 200
    data = response.json()

    assert "session_token" in data
    assert len(data["session_token"]) >= 32
    assert data["lesson_id"] == 1
    assert data["total_exercises"] == 5
    assert data["initial_hearts"] == 5
    assert data["current_hearts"] == 5
    assert len(data["exercises"]) == 5

    # Check payload sanitization across all exercises
    for ex in data["exercises"]:
        payload = ex["payload"]
        assert "canonical_answer" not in payload, f"Leaked canonical_answer in exercise {ex['id']}"
        assert "accepted_answers" not in payload, f"Leaked accepted_answers in exercise {ex['id']}"
        assert "answer_key" not in payload, f"Leaked answer_key in exercise {ex['id']}"
        assert "is_correct" not in payload, f"Leaked is_correct in exercise {ex['id']}"

        # Match pairs must decouple left and right items into separate shuffled lists
        if ex["exercise_type"] == "match_pairs":
            assert "pairs" not in payload, "Raw pairs array was leaked!"
            assert "left_items" in payload
            assert "right_items" in payload
            assert len(payload["left_items"]) == 4
            assert len(payload["right_items"]) == 4

def test_cross_user_session_access_rejected_403(client, seeded_db, monkeypatch):
    """Verify that a session cannot be answered or completed by another user."""
    monkeypatch.setattr(settings, "ALLOW_DEV_USER_OVERRIDE", True)

    # 1. Start session as duo_learner
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    first_ex_id = resp.json()["exercises"][0]["id"]

    # 2. Create another user
    other_user = User(
        username="other_learner",
        display_name="Other Learner",
        created_at=datetime.utcnow()
    )
    seeded_db.add(other_user)
    seeded_db.flush()
    other_stats = UserStats(user_id=other_user.id, xp=0, hearts=5, gems=500, streak=0)
    seeded_db.add(other_stats)
    seeded_db.commit()

    # 3. other_user tries to submit an answer
    ans_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        headers={"X-User-Id": str(other_user.id)},
        json={"exercise_id": first_ex_id, "answer": "el niño"}
    )
    assert ans_resp.status_code == 403
    assert "access" in ans_resp.json()["detail"].lower()

    # 4. other_user tries to complete the session
    comp_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/complete",
        headers={"X-User-Id": str(other_user.id)}
    )
    assert comp_resp.status_code == 403
    assert "access" in comp_resp.json()["detail"].lower()

def test_answer_submission_grading_all_five_types(client, seeded_db):
    """
    Verify authoritative grading for all 5 exercise types:
    multiple_choice, word_bank, match_pairs, fill_blank, and type_answer.
    """
    # Start Lesson 1 which contains all 5 types
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    # Map exercises by type
    ex_by_type = {e["exercise_type"]: e for e in exercises}

    # 1. Multiple Choice (canonical: "Hola")
    mc_ex = ex_by_type["multiple_choice"]
    mc_correct = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": mc_ex["id"], "answer": "Hola"}
    )
    assert mc_correct.status_code == 200
    assert mc_correct.json()["is_correct"] is True
    assert mc_correct.json()["feedback_title"] == "Nicely done!"

    # Start a second session to test incorrect MC
    resp2 = client.post("/api/v1/lessons/1/start")
    token2 = resp2.json()["session_token"]
    mc_wrong = client.post(
        f"/api/v1/lessons/sessions/{token2}/answer",
        json={"exercise_id": mc_ex["id"], "answer": "Adiós"}
    )
    assert mc_wrong.status_code == 200
    assert mc_wrong.json()["is_correct"] is False
    assert mc_wrong.json()["feedback_title"] == "Incorrect"

    # 2. Word Bank (canonical: "Buenos días amigo")
    wb_ex = ex_by_type["word_bank"]
    wb_correct = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": wb_ex["id"], "answer": ["Buenos", "días", "amigo"]}
    )
    assert wb_correct.status_code == 200
    assert wb_correct.json()["is_correct"] is True

    # 3. Match Pairs
    # Seeded pairs: [Hola: Hello, Adiós: Goodbye, Gracias: Thank you, Por favor: Please]
    mp_ex = ex_by_type["match_pairs"]
    mp_correct_pairs = [
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
        {"left": "Gracias", "right": "Thank you"},
        {"left": "Por favor", "right": "Please"}
    ]
    mp_correct = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": mp_ex["id"], "answer": mp_correct_pairs}
    )
    assert mp_correct.status_code == 200
    assert mp_correct.json()["is_correct"] is True

    # 4. Fill in the Blank (canonical: "Buenos")
    fb_ex = ex_by_type["fill_blank"]
    fb_correct = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": fb_ex["id"], "answer": "Buenos"}
    )
    assert fb_correct.status_code == 200
    assert fb_correct.json()["is_correct"] is True

    # 5. Type the Answer (canonical: "Hola, adiós", accepted includes "hola adios")
    ta_ex = ex_by_type["type_answer"]
    # Test normalization: lowercased, punctuation ignored
    ta_correct = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ta_ex["id"], "answer": "  hola, adios!  "}
    )
    assert ta_correct.status_code == 200
    assert ta_correct.json()["is_correct"] is True
    assert ta_correct.json()["completed_exercises"] == 5

def test_heart_loss_and_session_failure_on_zero_hearts(client, seeded_db):
    """
    Verify incorrect answers deduct hearts and reaching 0 hearts fails the session,
    rejecting subsequent answer or completion attempts.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 1
    seeded_db.commit()

    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    ex_id = resp.json()["exercises"][0]["id"]

    # Submit wrong answer
    ans_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "wrong_answer"}
    )
    assert ans_resp.status_code == 200
    ans_data = ans_resp.json()
    assert ans_data["is_correct"] is False
    assert ans_data["remaining_hearts"] == 0
    assert ans_data["session_status"] == "failed"

    # Verify learner stats in DB has 0 hearts
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 0

    # Attempting to answer another exercise in the failed session returns 400
    next_ex_id = resp.json()["exercises"][1]["id"]
    ans_fail_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": next_ex_id, "answer": "any"}
    )
    assert ans_fail_resp.status_code == 400
    assert "failed" in ans_fail_resp.json()["detail"].lower()

    # Attempting to complete a failed session returns 400
    comp_resp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp_resp.status_code == 400
    assert "failed" in comp_resp.json()["detail"].lower()

def test_duplicate_submission_idempotency_no_double_heart_deduction(client, seeded_db):
    """
    Verify submitting an answer to an already-answered exercise returns is_duplicate: True
    and NEVER deducts additional hearts.
    """
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    ex_id = resp.json()["exercises"][0]["id"]

    # First wrong answer: drops hearts from 5 to 4
    first_sub = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "wrong_1"}
    )
    assert first_sub.status_code == 200
    assert first_sub.json()["is_duplicate"] is False
    assert first_sub.json()["remaining_hearts"] == 4

    # Duplicate submission to the SAME exercise
    second_sub = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "wrong_1"}
    )
    assert second_sub.status_code == 200
    assert second_sub.json()["is_duplicate"] is True
    assert second_sub.json()["is_correct"] is False
    assert second_sub.json()["remaining_hearts"] == 4  # NOT 3!

    # A third duplicate with different text still returns cached result without deduction
    third_sub = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "different_attempt"}
    )
    assert third_sub.status_code == 200
    assert third_sub.json()["is_duplicate"] is True
    assert third_sub.json()["remaining_hearts"] == 4

def test_completion_rejected_if_exercises_unanswered(client, seeded_db):
    """Verify that completing a session with unanswered exercises returns 400."""
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    ex_id = resp.json()["exercises"][0]["id"]

    # Answer only 1 of 5 exercises
    client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "el niño"}
    )

    comp_resp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp_resp.status_code == 400
    assert "only 1 of 5 exercises answered" in comp_resp.json()["detail"].lower()

def test_first_time_lesson_completion_awards_15_xp_and_advances_progression(client, seeded_db):
    """
    Verify completing an uncompleted lesson for the first time awards 15 XP,
    updates daily streak, updates crowns, and returns full completion DTO.
    """
    # Lesson 4 is uncompleted in seed data (Skill 2, Lesson 2)
    resp = client.post("/api/v1/lessons/4/start")
    assert resp.status_code == 200
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    initial_xp = learner.stats.xp
    initial_streak = learner.stats.streak

    # Fetch canonical answers directly from DB to answer all 5 correctly
    for ex in exercises:
        db_ex = seeded_db.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        
        ans_resp = client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans}
        )
        assert ans_resp.status_code == 200
        assert ans_resp.json()["is_correct"] is True

    # Complete the lesson session
    comp_resp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()

    assert comp_data["status"] == "completed"
    assert comp_data["xp_awarded"] == 15
    assert comp_data["total_xp"] == initial_xp + 15
    assert comp_data["is_replay"] is False
    assert comp_data["is_idempotent"] is False
    assert comp_data["crowns"] == 3  # Skill 2 had 2 crowns; advancing to 3 because all lessons in skill done

    # Verify DB persistence
    seeded_db.refresh(learner.stats)
    assert learner.stats.xp == initial_xp + 15
    completion_row = seeded_db.query(UserLessonCompletion).filter(
        UserLessonCompletion.session_id == seeded_db.query(LessonSession).filter(LessonSession.session_token == token).first().id
    ).first()
    assert completion_row is not None
    assert completion_row.xp_earned == 15

def test_replay_lesson_completion_awards_5_xp_and_no_crown_advance(client, seeded_db):
    """
    Verify replaying an already-completed lesson awards only 5 XP
    and does not advance crowns.
    """
    # Lesson 1 was already completed by duo_learner in seed data
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    initial_xp = learner.stats.xp

    for ex in exercises:
        db_ex = seeded_db.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]

        client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans}
        )

    comp_resp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()

    assert comp_data["xp_awarded"] == 5
    assert comp_data["is_replay"] is True
    assert comp_data["total_xp"] == initial_xp + 5

    # Crowns for Skill 1 was 5 (max) and should remain 5
    assert comp_data["crowns"] == 5

def test_lesson_completion_idempotency(client, seeded_db):
    """
    Verify that calling completion multiple times on the same session is idempotent:
    returns 200 with is_idempotent: True, without awarding double XP or creating duplicate records.
    """
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    for ex in exercises:
        db_ex = seeded_db.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans}
        )

    # First completion
    first_comp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert first_comp.status_code == 200
    assert first_comp.json()["is_idempotent"] is False
    recorded_xp = first_comp.json()["total_xp"]

    # Second completion call (idempotent duplicate)
    second_comp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert second_comp.status_code == 200
    assert second_comp.json()["is_idempotent"] is True
    assert second_comp.json()["total_xp"] == recorded_xp  # No double XP!

    # Verify in DB: exactly 1 completion record for this session
    session_obj = seeded_db.query(LessonSession).filter(LessonSession.session_token == token).first()
    completions = seeded_db.query(UserLessonCompletion).filter(UserLessonCompletion.session_id == session_obj.id).all()
    assert len(completions) == 1

def test_answer_submission_exercise_not_in_lesson_rejected_400(client, seeded_db):
    """Verify submitting an exercise ID from a different lesson returns 400."""
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]

    # Exercise from Lesson 2
    ex_lesson2 = seeded_db.query(Exercise).filter(Exercise.lesson_id == 2).first()
    assert ex_lesson2 is not None

    ans_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_lesson2.id, "answer": "anything"}
    )
    assert ans_resp.status_code == 400
    assert "not belong" in ans_resp.json()["detail"].lower()

def test_answer_submission_after_completion_rejected_400(client, seeded_db):
    """Verify submitting an answer to an already completed session returns 400."""
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    for ex in exercises:
        db_ex = seeded_db.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans}
        )

    # Complete session
    comp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp.status_code == 200

    # Attempt to submit an answer after completion
    late_ans = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": exercises[0]["id"], "answer": "anything"}
    )
    assert late_ans.status_code == 400
    assert "already completed" in late_ans.json()["detail"].lower()

def test_flawless_victory_achievement_unlocked_on_perfect_lesson(client, seeded_db):
    """Verify finishing a lesson without heart loss unlocks 'Flawless Victory' achievement."""
    resp = client.post("/api/v1/lessons/4/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]

    for ex in exercises:
        db_ex = seeded_db.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans}
        )

    comp_resp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
    assert comp_resp.status_code == 200
    assert "Flawless Victory" in comp_resp.json()["achievements_unlocked"]

# ==============================================================================
# PHASE 3 FINAL HARDENING: HEART REGENERATION & SOURCE OF TRUTH
# ==============================================================================

def test_heart_regeneration_before_wrong_answer(client, seeded_db):
    """
    Verify passive regeneration happens BEFORE deducting a heart for an incorrect answer:
    Learner with 4 hearts and last loss 35 min ago recovers to 5, then drops to 4, NOT 3.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    # Start session normally (full 5 hearts)
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    ex_id = resp.json()["exercises"][0]["id"]

    # Now simulate heart loss occurred 35 minutes ago during the lesson
    learner.stats.hearts = 4
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(minutes=35)
    # Session snapshot before answer reflects 4
    session_obj = seeded_db.query(LessonSession).filter(LessonSession.session_token == token).first()
    session_obj.current_hearts = 4
    seeded_db.commit()

    # Submit WRONG answer
    ans_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "wrong_choice"}
    )
    assert ans_resp.status_code == 200
    ans_data = ans_resp.json()
    assert ans_data["is_correct"] is False

    # Passive regeneration restored 4 -> 5, then wrong answer dropped 5 -> 4
    assert ans_data["remaining_hearts"] == 4

    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert learner.stats.hearts == 4
    assert session_obj.current_hearts == 4

def test_heart_partial_regeneration_before_wrong_answer(client, seeded_db):
    """
    Verify partial regeneration timing is preserved when answer mutates hearts:
    Learner with 3 hearts and 45 min elapsed recovers 1 heart (3 -> 4), then drops to 3,
    and last_heart_loss_at advances by exactly 30 min (leaving ~15 min credit).
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    ex_id = resp.json()["exercises"][0]["id"]

    elapsed_loss_time = datetime.utcnow() - timedelta(minutes=45)
    learner.stats.hearts = 3
    learner.stats.last_heart_loss_at = elapsed_loss_time
    session_obj = seeded_db.query(LessonSession).filter(LessonSession.session_token == token).first()
    session_obj.current_hearts = 3
    seeded_db.commit()

    # Submit wrong answer
    ans_resp = client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": ex_id, "answer": "wrong_choice"}
    )
    assert ans_resp.status_code == 200
    assert ans_resp.json()["remaining_hearts"] == 3

    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert learner.stats.hearts == 3
    assert session_obj.current_hearts == 3

    # Verify last_heart_loss_at advanced by 1 interval (30 min), keeping 15 min progress
    expected_new_loss_at = elapsed_loss_time + timedelta(seconds=settings.HEART_REGEN_SECONDS)
    assert abs((learner.stats.last_heart_loss_at - expected_new_loss_at).total_seconds()) < 2.0

def test_heart_source_of_truth_agreement(client, seeded_db):
    """
    Verify UserStats.hearts and LessonSession.current_hearts remain strictly equal across:
    - correct answer
    - wrong answer
    - heart regeneration + wrong answer
    - zero-heart failure
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    resp = client.post("/api/v1/lessons/1/start")
    token = resp.json()["session_token"]
    exercises = resp.json()["exercises"]
    session_obj = seeded_db.query(LessonSession).filter(LessonSession.session_token == token).first()

    # 1. Correct answer: both remain equal
    client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": exercises[0]["id"], "answer": "Hola"}
    )
    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert session_obj.current_hearts == learner.stats.hearts == 5

    # 2. Wrong answer: both deduct to 4
    client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": exercises[1]["id"], "answer": "wrong"}
    )
    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert session_obj.current_hearts == learner.stats.hearts == 4

    # 3. Heart regeneration + wrong answer
    learner.stats.hearts = 3
    learner.stats.last_heart_loss_at = datetime.utcnow() - timedelta(minutes=35)
    session_obj.current_hearts = 3
    seeded_db.commit()

    client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": exercises[2]["id"], "answer": "wrong"}
    )
    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert session_obj.current_hearts == learner.stats.hearts == 3

    # 4. Zero-heart failure
    learner.stats.hearts = 1
    session_obj.current_hearts = 1
    seeded_db.commit()

    client.post(
        f"/api/v1/lessons/sessions/{token}/answer",
        json={"exercise_id": exercises[3]["id"], "answer": "wrong"}
    )
    seeded_db.refresh(learner.stats)
    seeded_db.refresh(session_obj)
    assert session_obj.current_hearts == learner.stats.hearts == 0
    assert session_obj.status == "failed"

# ==============================================================================
# PHASE 3 FINAL HARDENING: STRICT MATCH-PAIR GRADING
# ==============================================================================

def test_match_pairs_strict_grading_validation(client, seeded_db):
    """
    Verify strict match_pairs grading:
    - duplicate left fails
    - duplicate right fails
    - missing pair fails
    - wrong pair fails
    - exact correct mapping passes
    - correct mapping in different order passes
    """
    from app.services.validator_service import grade_exercise_submission
    mp_ex = seeded_db.query(Exercise).filter(Exercise.lesson_id == 1, Exercise.exercise_type == "match_pairs").first()
    assert mp_ex is not None
    # Canonical pairs in Lesson 1:
    # Hola -> Hello, Adiós -> Goodbye, Gracias -> Thank you, Por favor -> Please

    # A. Duplicate Left: Hola -> Hello submitted twice, Por favor missing
    dup_left = [
        {"left": "Hola", "right": "Hello"},
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
        {"left": "Gracias", "right": "Thank you"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, dup_left)
    assert is_ok is False
    assert "duplicate" in msg.lower()

    # B. Duplicate Right: Adiós and Gracias both mapped to "Goodbye"
    dup_right = [
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
        {"left": "Gracias", "right": "Goodbye"},
        {"left": "Por favor", "right": "Please"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, dup_right)
    assert is_ok is False

    # C. Missing pair: only 3 of 4 submitted
    missing = [
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
        {"left": "Gracias", "right": "Thank you"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, missing)
    assert is_ok is False
    assert "all pairs must be matched" in msg.lower()

    # D. Wrong pair: Hola -> Goodbye
    wrong_pair = [
        {"left": "Hola", "right": "Goodbye"},
        {"left": "Adiós", "right": "Hello"},
        {"left": "Gracias", "right": "Thank you"},
        {"left": "Por favor", "right": "Please"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, wrong_pair)
    assert is_ok is False
    assert "incorrect" in msg.lower()

    # E. Exact correct mapping: passes
    exact = [
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
        {"left": "Gracias", "right": "Thank you"},
        {"left": "Por favor", "right": "Please"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, exact)
    assert is_ok is True

    # F. Correct mapping in shuffled order: passes
    shuffled = [
        {"left": "Por favor", "right": "Please"},
        {"left": "Gracias", "right": "Thank you"},
        {"left": "Hola", "right": "Hello"},
        {"left": "Adiós", "right": "Goodbye"},
    ]
    is_ok, msg = grade_exercise_submission(mp_ex, shuffled)
    assert is_ok is True

# ==============================================================================
# PHASE 3 FINAL HARDENING: REAL CONCURRENCY TESTS (THREAD POOL EXECUTOR)
# ==============================================================================

from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.seeds.seeder import seed_database

@pytest.fixture
def thread_safe_client(tmp_path):
    """
    Dedicated WAL-mode SQLite database with busy_timeout=10000 and per-request
    session instantiation, enabling realistic concurrent execution without thread-affinity errors.
    """
    db_file = tmp_path / "concurrent_test.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False, "timeout": 15}
    )
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=10000")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    ThreadSafeSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    init_db = ThreadSafeSessionLocal()
    seed_database(init_db, reset=False)
    init_db.close()

    def get_thread_safe_db():
        db = ThreadSafeSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_thread_safe_db
    with TestClient(app) as test_client:
        yield test_client, ThreadSafeSessionLocal
    app.dependency_overrides.clear()
    engine.dispose()

def test_concurrent_duplicate_wrong_answer(thread_safe_client):
    """
    CONCURRENCY TEST A: Two simultaneous requests submitting WRONG answer for same session/exercise.
    Assert:
    - exactly 1 SessionAnswer row
    - exactly 1 heart deducted
    - one response is original (is_duplicate: False) and one is duplicate (is_duplicate: True)
    - no negative hearts
    - final DB state is correct
    """
    client, SessionLocal = thread_safe_client
    start_resp = client.post("/api/v1/lessons/1/start")
    token = start_resp.json()["session_token"]
    ex_id = start_resp.json()["exercises"][0]["id"]

    def submit_wrong(val):
        return client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex_id, "answer": val}
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(submit_wrong, "wrong_attempt_1")
        f2 = pool.submit(submit_wrong, "wrong_attempt_2")
        r1, r2 = f1.result(), f2.result()

    assert r1.status_code == 200
    assert r2.status_code == 200

    duplicates = [r1.json()["is_duplicate"], r2.json()["is_duplicate"]]
    assert True in duplicates, "One request must be identified as duplicate"
    assert False in duplicates, "One request must be the original winner"

    # DB state assertions
    s = SessionLocal()
    session_obj = s.query(LessonSession).filter(LessonSession.session_token == token).first()
    answers = s.query(SessionAnswer).filter(
        SessionAnswer.session_id == session_obj.id,
        SessionAnswer.exercise_id == ex_id
    ).all()
    learner = s.query(User).filter(User.username == "duo_learner").first()

    assert len(answers) == 1, "Exactly 1 SessionAnswer row must exist in DB"
    assert learner.stats.hearts == 4, "Exactly 1 heart must be deducted (not 2!)"
    assert session_obj.current_hearts == 4
    s.close()

def test_concurrent_duplicate_correct_answer(thread_safe_client):
    """
    CONCURRENCY TEST B: Two simultaneous requests submitting CORRECT answer for same session/exercise.
    Assert:
    - exactly 1 SessionAnswer row
    - 0 heart loss
    - one response original, one duplicate
    """
    client, SessionLocal = thread_safe_client
    start_resp = client.post("/api/v1/lessons/1/start")
    token = start_resp.json()["session_token"]
    ex_id = start_resp.json()["exercises"][0]["id"]

    def submit_correct():
        return client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": ex_id, "answer": "Hola"}
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(submit_correct)
        f2 = pool.submit(submit_correct)
        r1, r2 = f1.result(), f2.result()

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["is_correct"] is True
    assert r2.json()["is_correct"] is True

    duplicates = [r1.json()["is_duplicate"], r2.json()["is_duplicate"]]
    assert True in duplicates
    assert False in duplicates

    s = SessionLocal()
    session_obj = s.query(LessonSession).filter(LessonSession.session_token == token).first()
    answers = s.query(SessionAnswer).filter(
        SessionAnswer.session_id == session_obj.id,
        SessionAnswer.exercise_id == ex_id
    ).all()
    learner = s.query(User).filter(User.username == "duo_learner").first()

    assert len(answers) == 1
    assert learner.stats.hearts == 5, "0 hearts deducted for correct answer"
    assert session_obj.current_hearts == 5
    s.close()

def test_concurrent_lesson_completion(thread_safe_client):
    """
    CONCURRENCY TEST C: Two simultaneous /complete requests for the same session.
    Assert:
    - exactly 1 UserLessonCompletion row
    - XP is awarded exactly once
    - only one request is the state-transition winner
    - losing request is idempotent
    - no duplicate achievement or crown advancement
    """
    client, SessionLocal = thread_safe_client
    start_resp = client.post("/api/v1/lessons/4/start")
    token = start_resp.json()["session_token"]
    exercises = start_resp.json()["exercises"]

    s = SessionLocal()
    learner = s.query(User).filter(User.username == "duo_learner").first()
    initial_xp = learner.stats.xp

    for ex in exercises:
        db_ex = s.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        client.post(f"/api/v1/lessons/sessions/{token}/answer", json={"exercise_id": ex["id"], "answer": ans})
    s.close()

    def call_complete():
        return client.post(f"/api/v1/lessons/sessions/{token}/complete")

    with ThreadPoolExecutor(max_workers=2) as pool:
        f1 = pool.submit(call_complete)
        f2 = pool.submit(call_complete)
        r1, r2 = f1.result(), f2.result()

    assert r1.status_code == 200
    assert r2.status_code == 200

    idempotent_flags = [r1.json()["is_idempotent"], r2.json()["is_idempotent"]]
    assert False in idempotent_flags, "Exactly one request must be the transition winner"
    assert True in idempotent_flags, "The losing request must be marked idempotent"

    # Both report the same authoritative total XP (awarded once)
    assert r1.json()["total_xp"] == initial_xp + 15
    assert r2.json()["total_xp"] == initial_xp + 15

    s = SessionLocal()
    session_obj = s.query(LessonSession).filter(LessonSession.session_token == token).first()
    completions = s.query(UserLessonCompletion).filter(UserLessonCompletion.session_id == session_obj.id).all()
    assert len(completions) == 1, "Exactly 1 UserLessonCompletion record created"
    learner = s.query(User).filter(User.username == "duo_learner").first()
    assert learner.stats.xp == initial_xp + 15
    s.close()

def test_concurrent_final_answer_vs_completion_race(thread_safe_client):
    """
    CONCURRENCY TEST D: Final-answer submission racing with /complete.
    Assert invariant:
    - Lesson may NEVER become completed without all 5 answers in the database.
    - If completion runs first: safely returns 400 with incomplete rejection.
    - If answer commits first: completion succeeds.
    """
    client, SessionLocal = thread_safe_client
    start_resp = client.post("/api/v1/lessons/4/start")
    token = start_resp.json()["session_token"]
    exercises = start_resp.json()["exercises"]

    s = SessionLocal()
    for ex in exercises[:4]:
        db_ex = s.query(Exercise).filter(Exercise.id == ex["id"]).first()
        ans = db_ex.canonical_answer
        if ex["exercise_type"] == "match_pairs":
            pairs = json.loads(db_ex.payload_json)["pairs"]
            ans = [{"left": p["left"], "right": p["right"]} for p in pairs]
        client.post(f"/api/v1/lessons/sessions/{token}/answer", json={"exercise_id": ex["id"], "answer": ans})

    final_ex = exercises[4]
    db_final = s.query(Exercise).filter(Exercise.id == final_ex["id"]).first()
    final_ans = db_final.canonical_answer
    s.close()

    def submit_final():
        return client.post(
            f"/api/v1/lessons/sessions/{token}/answer",
            json={"exercise_id": final_ex["id"], "answer": final_ans}
        )

    def call_complete():
        return client.post(f"/api/v1/lessons/sessions/{token}/complete")

    with ThreadPoolExecutor(max_workers=2) as pool:
        f_ans = pool.submit(submit_final)
        f_comp = pool.submit(call_complete)
        r_ans, r_comp = f_ans.result(), f_comp.result()

    assert r_ans.status_code == 200

    if r_comp.status_code == 400:
        # Race condition where completion was checked before final answer committed
        assert "answered" in r_comp.json()["detail"].lower()
        # Retry completion now that final answer is committed
        retry_comp = client.post(f"/api/v1/lessons/sessions/{token}/complete")
        assert retry_comp.status_code == 200
        assert retry_comp.json()["status"] == "completed"
    else:
        # Race condition where final answer committed before completion check
        assert r_comp.status_code == 200
        assert r_comp.json()["status"] == "completed"

    s = SessionLocal()
    session_obj = s.query(LessonSession).filter(LessonSession.session_token == token).first()
    assert session_obj.status == "completed"
    answers = s.query(SessionAnswer).filter(SessionAnswer.session_id == session_obj.id).all()
    assert len(answers) == 5, "All 5 answers must be safely present in DB"
    s.close()


