from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class ChallengeSession(Base):
    __tablename__ = "challenge_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    challenge_token = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    time_limit_seconds = Column(Integer, default=90, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="in_progress", nullable=False)  # in_progress, completed, timed_out, failed
    xp_awarded = Column(Integer, default=0, nullable=False)
    is_first_completion = Column(Boolean, default=False, nullable=False)

    user = relationship("User")
    lesson = relationship("Lesson")
    answers = relationship("ChallengeAnswer", back_populates="challenge", cascade="all, delete-orphan")

class ChallengeAnswer(Base):
    __tablename__ = "challenge_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    challenge_id = Column(Integer, ForeignKey("challenge_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("challenge_id", "exercise_id", name="uq_challenge_exercise"),
    )

    challenge = relationship("ChallengeSession", back_populates="answers")
    exercise = relationship("Exercise")
