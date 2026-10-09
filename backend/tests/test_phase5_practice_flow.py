import pytest
from datetime import datetime
from app.models.user import User
from app.models.practice import PracticeSession

def test_practice_start_success_returns_sanitized_exercises(client, seeded_db):
    """
    Verify POST /api/v1/practice/start:
    - Creates a new PracticeSession with status='in_progress'.
    - Returns sanitized exercises without canonical answers or answer keys.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 2
    seeded_db.commit()

    resp = client.post("/api/v1/practice/start")
    assert resp.status_code == 200
    data = resp.json()

    assert "session_token" in data
    assert data["current_hearts"] == 2
    assert data["max_hearts"] == 5
    assert len(data["exercises"]) > 0

    # Ensure no canonical answers leaked in any exercise
    for ex in data["exercises"]:
        assert "canonical_answer" not in ex
        assert "accepted_answers" not in ex
        assert "answer_key" not in ex
        assert "payload" in ex

    # Verify session in DB
    session = seeded_db.query(PracticeSession).filter(
        PracticeSession.session_token == data["session_token"]
    ).first()
    assert session is not None
    assert session.status == "in_progress"
    assert session.heart_awarded is False

def test_practice_start_rejected_when_hearts_full(client, seeded_db):
    """
    Verify POST /api/v1/practice/start is rejected with 400 when learner already has 5 hearts.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 5
    seeded_db.commit()

    resp = client.post("/api/v1/practice/start")
    assert resp.status_code == 400
    assert "already full" in resp.json()["detail"].lower()

def test_practice_incomplete_session_rejected_no_heart_awarded(client, seeded_db):
    """
    Verify that an incomplete practice session cannot be completed:
    - Exiting or attempting to complete before answering all exercises is rejected.
    - Zero hearts are awarded.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 1
    seeded_db.commit()

    start_resp = client.post("/api/v1/practice/start")
    assert start_resp.status_code == 200
    token = start_resp.json()["session_token"]
    exercises = start_resp.json()["exercises"]
    assert len(exercises) >= 2

    # Answer only the first exercise
    first_ex = exercises[0]
    client.post(
        f"/api/v1/practice/sessions/{token}/answer",
        json={"exercise_id": first_ex["id"], "answer": "Hola"}
    )

    # Attempt to complete prematurely
    comp_resp = client.post(f"/api/v1/practice/sessions/{token}/complete")
    assert comp_resp.status_code == 400
    assert "only 1 of" in comp_resp.json()["detail"].lower()

    # Verify hearts did NOT increase
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 1

def test_practice_successful_completion_awards_one_heart_and_zero_xp(client, seeded_db):
    """
    Verify that completing all exercises in a practice session:
    - Awards exactly 1 heart.
    - Awards 0 XP (anti-farming protection).
    - Sets heart_awarded=True.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 3
    initial_xp = learner.stats.xp
    seeded_db.commit()

    start_resp = client.post("/api/v1/practice/start")
    assert start_resp.status_code == 200
    token = start_resp.json()["session_token"]
    exercises = start_resp.json()["exercises"]

    # Answer all exercises
    for ex in exercises:
        ans_resp = client.post(
            f"/api/v1/practice/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": "Test answer"}
        )
        assert ans_resp.status_code == 200
        # Mistakes do not deduct hearts
        assert ans_resp.json()["hearts_remaining"] == 3

    # Complete session
    comp_resp = client.post(f"/api/v1/practice/sessions/{token}/complete")
    assert comp_resp.status_code == 200
    data = comp_resp.json()
    assert data["status"] == "completed"
    assert data["hearts"] == 4
    assert data["heart_awarded"] is True
    assert data["is_idempotent"] is False

    # Check DB state
    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 4
    assert learner.stats.xp == initial_xp  # 0 XP awarded!

def test_practice_duplicate_completion_is_idempotent(client, seeded_db):
    """
    Verify that calling complete multiple times on the same session:
    - Returns idempotent response.
    - Does NOT award a second heart.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 2
    seeded_db.commit()

    start_resp = client.post("/api/v1/practice/start")
    token = start_resp.json()["session_token"]
    exercises = start_resp.json()["exercises"]

    for ex in exercises:
        client.post(
            f"/api/v1/practice/sessions/{token}/answer",
            json={"exercise_id": ex["id"], "answer": "Test answer"}
        )

    # First completion: 2 -> 3
    comp1 = client.post(f"/api/v1/practice/sessions/{token}/complete")
    assert comp1.status_code == 200
    assert comp1.json()["hearts"] == 3
    assert comp1.json()["heart_awarded"] is True

    # Duplicate completion replay: must not award another heart!
    comp2 = client.post(f"/api/v1/practice/sessions/{token}/complete")
    assert comp2.status_code == 200
    assert comp2.json()["hearts"] == 3
    assert comp2.json()["heart_awarded"] is False
    assert comp2.json()["is_idempotent"] is True

    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 3

def test_practice_abandoned_session_awards_no_hearts(client, seeded_db):
    """
    Verify that an abandoned session grants no hearts.
    """
    learner = seeded_db.query(User).filter(User.username == "duo_learner").first()
    learner.stats.hearts = 1
    seeded_db.commit()

    # Start session but never complete
    start_resp = client.post("/api/v1/practice/start")
    assert start_resp.status_code == 200

    seeded_db.refresh(learner.stats)
    assert learner.stats.hearts == 1
