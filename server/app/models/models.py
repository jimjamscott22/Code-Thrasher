import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class SubmissionStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    submissions: Mapped[list["Submission"]] = relationship(back_populates="user")
    solution_reveals: Mapped[list["SolutionReveal"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    exercises: Mapped[list["Exercise"]] = relationship(back_populates="category")


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str | None] = mapped_column(Text)
    guide: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list, nullable=False)
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.beginner
    )
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), index=True)
    starter_code: Mapped[str] = mapped_column(Text, default="")
    solution_code: Mapped[str | None] = mapped_column(Text)
    solution_explanation: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    category: Mapped["Category | None"] = relationship(back_populates="exercises")
    test_cases: Mapped[list["TestCase"]] = relationship(back_populates="exercise")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="exercise")

    @property
    def has_solution(self) -> bool:
        return bool(self.solution_code and self.solution_code.strip())


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
    input_data: Mapped[str] = mapped_column(Text, default="")
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    score_weight: Mapped[float] = mapped_column(Float, default=1.0)
    is_hidden: Mapped[bool] = mapped_column(default=False)

    exercise: Mapped["Exercise"] = relationship(back_populates="test_cases")


class SolutionReveal(Base):
    __tablename__ = "solution_reveals"
    __table_args__ = (UniqueConstraint("user_id", "exercise_id", name="uq_solution_reveal_user_exercise"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False, index=True)
    revealed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="solution_reveals")
    exercise: Mapped["Exercise"] = relationship()


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    topic_area: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        Enum(DifficultyLevel), nullable=False, default=DifficultyLevel.beginner
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    sections: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        # Covers "all submissions for a user" and "user's attempt on a specific exercise"
        Index("ix_submissions_user_exercise", "user_id", "exercise_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus), default=SubmissionStatus.pending, index=True
    )
    score: Mapped[float] = mapped_column(Float, default=0.0)
    stdout: Mapped[str] = mapped_column(Text, default="")
    stderr: Mapped[str] = mapped_column(Text, default="")
    time_taken_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="submissions")
    exercise: Mapped["Exercise"] = relationship(back_populates="submissions")
