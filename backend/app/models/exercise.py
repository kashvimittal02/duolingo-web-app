from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    exercise_type = Column(String(30), nullable=False)  # multiple_choice, word_bank, match_pairs, fill_blank, type_answer
    prompt = Column(Text, nullable=False)
    prompt_translation = Column(Text, nullable=True)
    canonical_answer = Column(Text, nullable=False)
    payload_json = Column(Text, nullable=False)  # JSON-encoded options, tokens, pairs, template

    __table_args__ = (
        UniqueConstraint("lesson_id", "order_index", name="uq_exercise_lesson_order"),
    )

    lesson = relationship("Lesson", back_populates="exercises")
    session_answers = relationship("SessionAnswer", back_populates="exercise", cascade="all, delete-orphan")
