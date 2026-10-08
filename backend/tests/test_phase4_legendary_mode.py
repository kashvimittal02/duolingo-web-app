import pytest
from datetime import datetime, timedelta
from app.models.challenge import ChallengeSession, ChallengeAnswer
from app.models.user import User
from app.models.course import Lesson

def test_challenge_start_success(client):
    """Verify that an unlocked lesson can start a Legendary challenge with a 90s server deadline."""
    res = client.post("/api/v1/challenges/1/start")
    assert res.status_code == 200, res.text
    data = res.json()
    assert "challenge_token" in data
    assert data["lesson_id"] == 1
    assert data["time_limit_seconds"] == 90
    assert data["remaining_seconds"] <= 90 and data["remaining_seconds"] >= 88
    assert data["total_exercises"] == 5
    assert len(data["exercises"]) == 5

    # Verify answers are stripped from exercises
    for ex in data["exercises"]:
        assert "canonical_answer" not in ex
        assert "canonical_answer" not in ex["payload"]
        assert "correct_index" not in ex["payload"]

def test_challenge_start_locked_lesson_rejected_403(client):
    """Verify that a locked lesson cannot start a Legendary challenge."""
    # Lesson 8 is locked for default learner
    res = client.post("/api/v1/challenges/8/start")
    assert res.status_code == 403
    assert "locked" in res.json()["detail"].lower()

def test_challenge_get_status_active_and_expired(client, seeded_db):
    """Verify GET status returns server-authoritative remaining time and auto-expires."""
    res = client.post("/api/v1/challenges/1/start")
    assert res.status_code == 200
    token = res.json()["challenge_token"]

    status_res = client.get(f"/api/v1/challenges/sessions/{token}")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert status_data["status"] == "in_progress"
    assert status_data["remaining_seconds"] > 0
    assert status_data["is_expired"] is False

    # Simulate deadline expiry on server
    challenge = seeded_db.query(ChallengeSession).filter(ChallengeSession.challenge_token == token).first()
    challenge.expires_at = datetime.utcnow() - timedelta(seconds=5)
    seeded_db.commit()

    # Query status again - should auto-expire
    expired_res = client.get(f"/api/v1/challenges/sessions/{token}")
    assert expired_res.status_code == 200
    expired_data = expired_res.json()
    assert expired_data["status"] == "timed_out"
    assert expired_data["remaining_seconds"] == 0
    assert expired_data["is_expired"] is True

def test_challenge_answer_submission_and_expiry_enforcement(client, seeded_db):
    """Verify that answers are accepted within time limit and strictly rejected after expiry."""
    res = client.post("/api/v1/challenges/1/start")
    assert res.status_code == 200
    data = res.json()
    token = data["challenge_token"]
    ex1 = data["exercises"][0]

    # Valid submission before expiry
    ans_res = client.post(
        f"/api/v1/challenges/sessions/{token}/answer",
        json={"exercise_id": ex1["id"], "answer": "Hola"},
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["is_correct"] is True
    assert ans_data["completed_exercises"] == 1
    assert ans_data["is_duplicate"] is False

    # Duplicate submission is idempotent
    dup_res = client.post(
        f"/api/v1/challenges/sessions/{token}/answer",
        json={"exercise_id": ex1["id"], "answer": "Hola"},
    )
    assert dup_res.status_code == 200
    assert dup_res.json()["is_duplicate"] is True

    # Now expire the challenge on server
    challenge = seeded_db.query(ChallengeSession).filter(ChallengeSession.challenge_token == token).first()
    challenge.expires_at = datetime.utcnow() - timedelta(seconds=1)
    seeded_db.commit()

    # Next exercise submission must be rejected
    ex2 = data["exercises"][1]
    late_res = client.post(
        f"/api/v1/challenges/sessions/{token}/answer",
        json={"exercise_id": ex2["id"], "answer": ["Buenos", "días", "amigo"]},
    )
    assert late_res.status_code == 400
    assert "expired" in late_res.json()["detail"].lower()

def test_challenge_completion_awards_first_time_bonus_and_prevents_farming(client, seeded_db):
    """Verify that completing Legendary challenge awards +20 XP once, and 0 XP on replay."""
    user = seeded_db.query(User).filter(User.username == "duo_learner").first()
    initial_xp = user.stats.xp

    # 1. Start Challenge 1
    start_res = client.post("/api/v1/challenges/1/start")
    assert start_res.status_code == 200
    token1 = start_res.json()["challenge_token"]
    exercises = start_res.json()["exercises"]

    # Submit all 5 answers
    answers = [
        "Hola",
        ["Buenos", "días", "amigo"],
        [{"left": "Hola", "right": "Hello"}, {"left": "Adiós", "right": "Goodbye"}, {"left": "Por favor", "right": "Please"}, {"left": "Gracias", "right": "Thank you"}],
        "Buenos",
        "Hola, adiós",
    ]
    for ex, ans in zip(exercises, answers):
        a_res = client.post(
            f"/api/v1/challenges/sessions/{token1}/answer",
            json={"exercise_id": ex["id"], "answer": ans},
        )
        assert a_res.status_code == 200

    # Complete challenge 1
    comp_res = client.post(f"/api/v1/challenges/sessions/{token1}/complete")
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["status"] == "completed"
    assert comp_data["xp_awarded"] == 20
    assert comp_data["is_first_completion"] is True
    assert comp_data["total_xp"] == initial_xp + 20

    # Idempotent completion check
    idemp_res = client.post(f"/api/v1/challenges/sessions/{token1}/complete")
    assert idemp_res.status_code == 200
    assert idemp_res.json()["is_idempotent"] is True
    assert idemp_res.json()["total_xp"] == initial_xp + 20

    # 2. Start a REPLAY challenge for the same lesson
    replay_start = client.post("/api/v1/challenges/1/start")
    assert replay_start.status_code == 200
    token2 = replay_start.json()["challenge_token"]
    for ex, ans in zip(exercises, answers):
        client.post(
            f"/api/v1/challenges/sessions/{token2}/answer",
            json={"exercise_id": ex["id"], "answer": ans},
        )

    replay_comp = client.post(f"/api/v1/challenges/sessions/{token2}/complete")
    assert replay_comp.status_code == 200
    replay_data = replay_comp.json()
    assert replay_data["status"] == "completed"
    assert replay_data["xp_awarded"] == 0  # Anti-farming: repeat completion gives 0 XP bonus
    assert replay_data["is_first_completion"] is False
    assert replay_data["total_xp"] == initial_xp + 20  # No extra XP added

def test_challenge_completion_after_deadline_rejected_400(client, seeded_db):
    """Verify that completing a challenge after deadline is rejected."""
    res = client.post("/api/v1/challenges/1/start")
    assert res.status_code == 200
    data = res.json()
    token = data["challenge_token"]
    exercises = data["exercises"]

    # Submit 5 answers
    answers = [
        "Hola",
        ["Buenos", "días", "amigo"],
        [{"left": "Hola", "right": "Hello"}, {"left": "Adiós", "right": "Goodbye"}, {"left": "Por favor", "right": "Please"}, {"left": "Gracias", "right": "Thank you"}],
        "Buenos",
        "Hola, adiós",
    ]
    for ex, ans in zip(exercises, answers):
        client.post(
            f"/api/v1/challenges/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": ans},
        )

    # Expire on server
    challenge = seeded_db.query(ChallengeSession).filter(ChallengeSession.challenge_token == token).first()
    challenge.expires_at = datetime.utcnow() - timedelta(seconds=1)
    seeded_db.commit()

    # Completion attempt must fail
    comp_res = client.post(f"/api/v1/challenges/sessions/{token}/complete")
    assert comp_res.status_code == 400
    assert "expired" in comp_res.json()["detail"].lower()
