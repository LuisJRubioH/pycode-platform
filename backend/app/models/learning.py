"""
Models for lessons, exercises, and user progress.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Lesson(Base):
    """Lesson model for course content."""
    
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text)  # Markdown content
    difficulty = Column(String(50), default="beginner")  # beginner, intermediate, advanced
    category = Column(String(100))
    order = Column(Integer, default=0)
    estimated_duration = Column(Integer, default=15)  # in minutes
    prerequisites = Column(JSON, default=list)  # List of lesson IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="lesson")


class Exercise(Base):
    """Exercise model for practice problems."""
    
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    starter_code = Column(Text)
    solution_code = Column(Text)
    test_cases = Column(JSON, default=list)  # List of test case dicts
    hints = Column(JSON, default=list)  # List of hints
    points = Column(Integer, default=10)
    difficulty = Column(String(50), default="easy")  # easy, medium, hard
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="exercises")
    submissions = relationship("CodeSubmission", back_populates="exercise")


class UserProgress(Base):
    """User progress tracking model."""
    
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed
    progress = Column(Integer, default=0)
    score = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)  # in seconds
    attempts = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")


class CodeSubmission(Base):
    """Code submission model for exercise attempts."""
    
    __tablename__ = "code_submissions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    code = Column(Text, nullable=False)
    result = Column(String(50))  # success, error, timeout
    output = Column(Text)
    error_message = Column(Text)
    execution_time = Column(Integer)  # in milliseconds
    passed_tests = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")


class TutorSession(Base):
    """Tutor session model for AI interactions."""
    
    __tablename__ = "tutor_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    messages = Column(JSON, default=list)  # List of message dicts
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    lesson = relationship("Lesson")


class AIFeedback(Base):
    """AI feedback model for rating tutor responses."""
    
    __tablename__ = "ai_feedback"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("tutor_sessions.id"), nullable=False)
    message_index = Column(Integer, nullable=False)
    helpful_rating = Column(Integer)  # 1-5 rating
    feedback_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
