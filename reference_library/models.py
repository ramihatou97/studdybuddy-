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
    text_extracted = Column(Boolean, default=False)
    images_extracted = Column(Boolean, default=False)
    notes = relationship("Note", back_populates="book", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="book", cascade="all, delete-orphan")
    extracted_pages = relationship("ExtractedPage", back_populates="book", cascade="all, delete-orphan")
    extracted_images = relationship("ExtractedImage", back_populates="book", cascade="all, delete-orphan")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Book(id={self.id}, title='{self.title}')>"


class ExtractedPage(Base):
    """Extracted text content from a PDF page."""
    __tablename__ = 'extracted_pages'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    page_number = Column(Integer, nullable=False)
    text_content = Column(Text)
    word_count = Column(Integer, default=0)
    has_tables = Column(Boolean, default=False)
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    book = relationship("Book", back_populates="extracted_pages")
    
    def __repr__(self) -> str:
        return f"<ExtractedPage(book_id={self.book_id}, page={self.page_number})>"


class ExtractedImage(Base):
    """Extracted image or figure from PDF."""
    __tablename__ = 'extracted_images'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    page_number = Column(Integer, nullable=False)
    image_path = Column(String(1000), nullable=False)
    filename = Column(String(500))
    width = Column(Float)
    height = Column(Float)
    size_kb = Column(Float)
    annotation = Column(Text)  # AI-generated or manual annotation
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    book = relationship("Book", back_populates="extracted_images")
    
    def __repr__(self) -> str:
        return f"<ExtractedImage(id={self.id}, page={self.page_number})>"


class Chapter(Base):
    """AI-generated comprehensive medical chapter."""
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)
    title = Column(String(500), nullable=False)
    subject = Column(String(500))
    content = Column(Text)  # Synthesized chapter content
    source_pages = Column(String(1000))  # Comma-separated page numbers
    source_images = Column(String(1000))  # Comma-separated image IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ai_model_used = Column(String(100))
    
    book = relationship("Book", back_populates="chapters")
    
    def __repr__(self) -> str:
        return f"<Chapter(id={self.id}, title='{self.title}')>"


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
