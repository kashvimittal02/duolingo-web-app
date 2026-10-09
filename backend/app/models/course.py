from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(100), nullable=False)
    target_lang = Column(String(50), nullable=False)

    units = relationship("Unit", back_populates="course", cascade="all, delete-orphan", order_by="Unit.order_index")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    section_index = Column(Integer, default=1, nullable=False)
    section_title = Column(String(100), default="Rookie Basics", nullable=False)
    order_index = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    hex_color = Column(String(7), default="#58cc02", nullable=False)
    is_checkpoint = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("course_id", "order_index", name="uq_unit_course_order"),
    )

    course = relationship("Course", back_populates="units")
    skills = relationship("Skill", back_populates="unit", cascade="all, delete-orphan", order_by="Skill.order_index")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    icon_name = Column(String(50), default="message-circle", nullable=False)
    total_crown_levels = Column(Integer, default=5, nullable=False)

    __table_args__ = (
        UniqueConstraint("unit_id", "order_index", name="uq_skill_unit_order"),
    )

    unit = relationship("Unit", back_populates="skills")
    lessons = relationship("Lesson", back_populates="skill", cascade="all, delete-orphan", order_by="Lesson.order_index")
    progress = relationship("UserSkillProgress", back_populates="skill", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    xp_reward = Column(Integer, default=15, nullable=False)

    __table_args__ = (
        UniqueConstraint("skill_id", "order_index", name="uq_lesson_skill_order"),
    )

    skill = relationship("Skill", back_populates="lessons")
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan", order_by="Exercise.order_index")
    completions = relationship("UserLessonCompletion", back_populates="lesson", cascade="all, delete-orphan")
    sessions = relationship("LessonSession", back_populates="lesson", cascade="all, delete-orphan")
