"""
Database models for reference library
Implements Neurocore Lesson 8: Composite indexes from day 1
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, Boolean,
    ForeignKey, Index, JSON, func
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB

# Try to import pgvector for PostgreSQL, fall back for SQLite
try:
    from pgvector.sqlalchemy import Vector
    VECTOR_AVAILABLE = True
except ImportError:
    VECTOR_AVAILABLE = False
    # Placeholder for SQLite - will use LargeBinary
    from sqlalchemy import LargeBinary

Base = declarative_base()


class Book(Base):
    """
    Represents a neurosurgical textbook

    Design Notes:
    - ISBN for unique identification
    - Edition tracking for version control
    - Metadata cached for fast access
    """
    __tablename__ = 'books'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    title = Column(String(500), nullable=False)
    authors = Column(JSON, nullable=True)  # List of author names
    edition = Column(String(50), nullable=True)
    publisher = Column(String(200), nullable=True)
    year = Column(Integer, nullable=True)

    # File management
    file_path = Column(String(1000), nullable=False, unique=True)
    file_size = Column(Integer, nullable=False)  # Bytes
    file_hash = Column(String(64), nullable=False)  # SHA-256
    page_count = Column(Integer, nullable=True)

    # Processing status
    indexed_at = Column(DateTime, nullable=False, default=func.now())
    ai_processed = Column(Boolean, default=False)
    processing_error = Column(Text, nullable=True)

    # Metadata
    book_metadata = Column(JSON, nullable=True)  # Flexible storage

    # Relationships
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")

    # Composite index for common query pattern
    __table_args__ = (
        Index('idx_book_search', 'title', 'authors', 'year'),
        Index('idx_book_processing', 'ai_processed', 'indexed_at'),
    )

    def __repr__(self):
        return f"<Book(title='{self.title}', edition='{self.edition}')>"


class Chapter(Base):
    """
    Represents a chapter within a book

    Design Notes:
    - AI-detected chapter boundaries
    - Confidence score for manual review
    - Hierarchical structure support (nested chapters)
    """
    __tablename__ = 'chapters'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    book_id = Column(String(36), ForeignKey('books.id', ondelete='CASCADE'), nullable=False)

    # Chapter identification
    chapter_number = Column(String(50), nullable=True)  # "3", "3.1", "A"
    title = Column(String(500), nullable=False)
    subtitle = Column(String(500), nullable=True)

    # Location in book
    start_page = Column(Integer, nullable=False)
    end_page = Column(Integer, nullable=False)

    # Hierarchy support
    parent_chapter_id = Column(String(36), ForeignKey('chapters.id', ondelete='CASCADE'), nullable=True)
    level = Column(Integer, default=1)  # 1=chapter, 2=section, 3=subsection

    # Content
    authors = Column(JSON, nullable=True)  # Chapter-specific authors
    abstract = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)

    # AI detection metadata
    detection_method = Column(String(50), nullable=False)  # "ai", "toc", "header", "manual"
    confidence_score = Column(Float, nullable=True)  # 0.0-1.0

    # Classification
    anatomical_regions = Column(JSON, nullable=True)  # ["temporal lobe", "skull base"]
    procedure_types = Column(JSON, nullable=True)  # ["craniotomy", "microsurgery"]
    keywords = Column(JSON, nullable=True)

    # Embedding for semantic search (Neurocore Lesson 4: Add early)
    # Use Vector for PostgreSQL, LargeBinary for SQLite
    if VECTOR_AVAILABLE:
        embedding = Column(Vector(1536), nullable=True)  # OpenAI ada-002 dimension
    else:
        embedding = Column(LargeBinary, nullable=True)  # Store as binary for SQLite

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    book = relationship("Book", back_populates="chapters")
    parent_chapter = relationship("Chapter", remote_side=[id], backref="sub_chapters")
    sections = relationship("Section", back_populates="chapter", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="chapter", cascade="all, delete-orphan")

    # Composite indexes (Neurocore Lesson 8)
    __table_args__ = (
        Index('idx_chapter_book', 'book_id', 'chapter_number'),
        Index('idx_chapter_pages', 'book_id', 'start_page', 'end_page'),
        Index('idx_chapter_detection', 'detection_method', 'confidence_score'),
        Index('idx_chapter_hierarchy', 'parent_chapter_id', 'level'),
    )

    def __repr__(self):
        return f"<Chapter(title='{self.title}', pages={self.start_page}-{self.end_page})>"


class Section(Base):
    """
    Represents a section within a chapter

    Design Notes:
    - Granular content organization
    - Enables precise citations
    - Tracks regeneration history
    """
    __tablename__ = 'sections'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chapter_id = Column(String(36), ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False)

    # Section identification
    section_number = Column(String(50), nullable=True)  # "3.1.2"
    title = Column(String(500), nullable=False)
    heading_level = Column(Integer, default=2)  # 1=h1, 2=h2, etc.

    # Content
    content = Column(Text, nullable=False)  # Original content
    page_number = Column(Integer, nullable=True)

    # Regeneration tracking (Phase 5)
    regenerated_content = Column(Text, nullable=True)
    regeneration_count = Column(Integer, default=0)
    last_regenerated_at = Column(DateTime, nullable=True)
    regeneration_prompt = Column(Text, nullable=True)

    # Embedding for semantic search
    if VECTOR_AVAILABLE:
        embedding = Column(Vector(1536), nullable=True)
    else:
        embedding = Column(LargeBinary, nullable=True)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    chapter = relationship("Chapter", back_populates="sections")

    # Composite index
    __table_args__ = (
        Index('idx_section_chapter', 'chapter_id', 'section_number'),
        Index('idx_section_regenerated', 'regeneration_count', 'last_regenerated_at'),
    )

    def __repr__(self):
        return f"<Section(title='{self.title}', page={self.page_number})>"


class Image(Base):
    """
    Represents an image extracted from a chapter

    Design Notes:
    - Stores both original and processed versions
    - AI-generated descriptions for search
    - Quality scoring for filtering
    """
    __tablename__ = 'images'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chapter_id = Column(String(36), ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False)

    # File management
    file_path = Column(String(1000), nullable=False)
    thumbnail_path = Column(String(1000), nullable=True)
    file_hash = Column(String(64), nullable=False)  # SHA-256

    # Image metadata
    page_number = Column(Integer, nullable=False)
    image_type = Column(String(50), nullable=True)  # "figure", "table", "diagram", "photograph"
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    dpi = Column(Integer, nullable=True)

    # Content description
    caption = Column(Text, nullable=True)  # Original caption
    ai_description = Column(Text, nullable=True)  # AI-generated description
    anatomical_structures = Column(JSON, nullable=True)  # ["temporal bone", "dura"]

    # Quality assessment
    quality_score = Column(Float, nullable=True)  # 0.0-1.0
    is_relevant = Column(Boolean, default=True)

    # Embedding for similarity search (Phase 4)
    if VECTOR_AVAILABLE:
        embedding = Column(Vector(1536), nullable=True)
    else:
        embedding = Column(LargeBinary, nullable=True)

    # Timestamps
    extracted_at = Column(DateTime, nullable=False, default=func.now())
    processed_at = Column(DateTime, nullable=True)

    # Relationships
    chapter = relationship("Chapter", back_populates="images")

    # Composite indexes
    __table_args__ = (
        Index('idx_image_chapter', 'chapter_id', 'page_number'),
        Index('idx_image_quality', 'quality_score', 'is_relevant'),
        Index('idx_image_type', 'image_type', 'quality_score'),
    )

    def __repr__(self):
        return f"<Image(type='{self.image_type}', page={self.page_number})>"


class ProcessingLog(Base):
    """
    Tracks processing history for debugging and auditing

    Design Notes:
    - Detailed error tracking
    - Performance monitoring
    - Audit trail for compliance
    """
    __tablename__ = 'processing_logs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))

    # What was processed
    entity_type = Column(String(50), nullable=False)  # "book", "chapter", "image"
    entity_id = Column(String(36), nullable=False)

    # Processing details
    operation = Column(String(100), nullable=False)  # "index", "ai_analyze", "extract_images"
    status = Column(String(50), nullable=False)  # "success", "failure", "partial"

    # Timing
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Results
    result_summary = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    error_code = Column(String(50), nullable=True)

    # Cost tracking (for AI operations)
    tokens_used = Column(Integer, nullable=True)
    estimated_cost = Column(Float, nullable=True)

    # Composite index for querying
    __table_args__ = (
        Index('idx_log_entity', 'entity_type', 'entity_id', 'operation'),
        Index('idx_log_status', 'status', 'completed_at'),
        Index('idx_log_performance', 'operation', 'duration_seconds'),
    )

    def __repr__(self):
        return f"<ProcessingLog(operation='{self.operation}', status='{self.status}')>"
