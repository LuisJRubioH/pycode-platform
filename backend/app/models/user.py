"""
User model for authentication and profile management.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    progress = relationship("UserProgress", back_populates="user")
    submissions = relationship("CodeSubmission", back_populates="user")
    sessions = relationship("TutorSession", back_populates="user")


class UserProfile(Base):
    """Extended user profile information."""
    
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    level = Column(String(50), default="beginner")
    xp_points = Column(Integer, default=0)
    badges = Column(Text, default="[]")  # JSON string
    preferences = Column(Text, default="{}")  # JSON string
    
    user = relationship("User", back_populates="profile")
