"""
Database models for StudyBuddy.
Simple, focused models for neurosurgical study tracking.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, DateTime, 
    Float, ForeignKey, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Book(Base):
    """Medical textbook or PDF reference."""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    file_path = Column(String(1000), nullable=False, unique=True)
    author = Column(String(500))
    added_at = Column(DateTime, default=datetime.utcnow)
    total_pages = Column(Integer)
    notes = relationship("Note", back_populates="book", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}')>"


class Note(Base):
    """Study notes for specific topics."""
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    topic = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(String(500))  # Comma-separated tags
    
    book = relationship("Book", back_populates="notes")
    
    def __repr__(self) -> str:
        return f"<Note(id={self.id}, topic='{self.topic}')>"


class Flashcard(Base):
    """Flashcard for spaced repetition learning."""
    __tablename__ = 'flashcards'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    topic = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime, nullable=True)
    next_review = Column(DateTime, nullable=True)
    ease_factor = Column(Float, default=2.5)  # For spaced repetition algorithm
    interval_days = Column(Integer, default=1)
    repetitions = Column(Integer, default=0)
    
    book = relationship("Book", back_populates="flashcards")
    
    def __repr__(self) -> str:
        return f"<Flashcard(id={self.id}, topic='{self.topic}')>"


class StudySession(Base):
    """Track study sessions for progress monitoring."""
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    topic = Column(String(500))
    duration_minutes = Column(Integer, nullable=False)
    notes_count = Column(Integer, default=0)
    flashcards_reviewed = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<StudySession(id={self.id}, topic='{self.topic}', duration={self.duration_minutes}min)>"


# Database session management
class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, db_path: str = "data/database/studybuddy.db"):
        """Initialize database manager."""
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """Get a new database session."""
        return self.SessionLocal()
