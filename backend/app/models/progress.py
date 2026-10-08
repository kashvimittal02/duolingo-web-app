from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class UserLessonCompletion(Base):
    __tablename__ = "user_lesson_completions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("lesson_sessions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    xp_earned = Column(Integer, default=15, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("LessonSession", back_populates="completion")
    user = relationship("User", back_populates="lesson_completions")
    lesson = relationship("Lesson", back_populates="completions")

class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    crowns = Column(Integer, default=0, nullable=False)
    current_lesson_index = Column(Integer, default=0, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress"),
    )

    user = relationship("User", back_populates="skill_progress")
    skill = relationship("Skill", back_populates="progress")
