from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base, get_utc_now

class LessonSession(Base):
    __tablename__ = "lesson_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_token = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    initial_hearts = Column(Integer, nullable=False)
    current_hearts = Column(Integer, nullable=False)
    status = Column(String(20), default="in_progress", nullable=False)  # in_progress, completed, failed
    started_at = Column(DateTime, default=get_utc_now, nullable=False)
    finished_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")
    lesson = relationship("Lesson", back_populates="sessions")
    answers = relationship("SessionAnswer", back_populates="session", cascade="all, delete-orphan")
    completion = relationship("UserLessonCompletion", back_populates="session", uselist=False, cascade="all, delete-orphan")

class SessionAnswer(Base):
    __tablename__ = "session_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("lesson_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=get_utc_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("session_id", "exercise_id", name="uq_session_exercise"),
    )

    session = relationship("LessonSession", back_populates="answers")
    exercise = relationship("Exercise", back_populates="session_answers")
