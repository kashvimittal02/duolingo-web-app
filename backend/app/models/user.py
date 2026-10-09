from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base, get_utc_now

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)

    # Relationships
    stats = relationship("UserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")
    skill_progress = relationship("UserSkillProgress", back_populates="user", cascade="all, delete-orphan")
    lesson_completions = relationship("UserLessonCompletion", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("LessonSession", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    xp = Column(Integer, default=0, nullable=False)
    hearts = Column(Integer, default=5, nullable=False)
    max_hearts = Column(Integer, default=5, nullable=False)
    gems = Column(Integer, default=500, nullable=False)
    streak = Column(Integer, default=0, nullable=False)
    last_streak_date = Column(Date, nullable=True)
    last_heart_loss_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("xp >= 0", name="chk_user_stats_xp"),
        CheckConstraint("hearts >= 0 AND hearts <= max_hearts", name="chk_user_stats_hearts"),
        CheckConstraint("gems >= 0", name="chk_user_stats_gems"),
        CheckConstraint("streak >= 0", name="chk_user_stats_streak"),
    )

    user = relationship("User", back_populates="stats")
