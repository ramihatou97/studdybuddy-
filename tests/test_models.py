"""
Tests for database models
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from reference_library.models import Base, Book, Chapter, Section, Image, ProcessingLog


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()


class TestBookModel:
    """Tests for Book model"""

    def test_create_book(self, db_session):
        """Test creating a book"""
        book = Book(
            isbn="978-0-123-45678-9",
            title="Core Techniques in Operative Neurosurgery",
            authors=["Rahul Jandial"],
            edition="2nd",
            publisher="Elsevier",
            year=2020,
            file_path="/library/books/core_techniques.pdf",
            file_size=52428800,  # 50 MB
            file_hash="abc123def456",
            page_count=1200
        )

        db_session.add(book)
        db_session.commit()

        assert book.id is not None
        assert book.isbn == "978-0-123-45678-9"
        assert book.indexed_at is not None
        assert book.ai_processed is False

    def test_book_chapter_relationship(self, db_session):
        """Test book → chapters relationship"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123",
            page_count=100
        )
        db_session.add(book)
        db_session.commit()

        chapter1 = Chapter(
            book_id=book.id,
            title="Chapter 1",
            start_page=1,
            end_page=10,
            detection_method="manual"
        )
        chapter2 = Chapter(
            book_id=book.id,
            title="Chapter 2",
            start_page=11,
            end_page=20,
            detection_method="manual"
        )

        db_session.add_all([chapter1, chapter2])
        db_session.commit()

        # Test relationship
        assert len(book.chapters) == 2
        assert book.chapters[0].title == "Chapter 1"
        assert book.chapters[1].title == "Chapter 2"

    def test_book_cascade_delete(self, db_session):
        """Test that deleting book deletes chapters"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        chapter = Chapter(
            book_id=book.id,
            title="Chapter 1",
            start_page=1,
            end_page=10,
            detection_method="manual"
        )
        db_session.add(chapter)
        db_session.commit()

        chapter_id = chapter.id

        # Delete book
        db_session.delete(book)
        db_session.commit()

        # Verify chapter was deleted
        deleted_chapter = db_session.query(Chapter).filter_by(id=chapter_id).first()
        assert deleted_chapter is None


class TestChapterModel:
    """Tests for Chapter model"""

    def test_create_chapter(self, db_session):
        """Test creating a chapter"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        chapter = Chapter(
            book_id=book.id,
            chapter_number="3",
            title="Temporal Craniotomy",
            start_page=45,
            end_page=72,
            detection_method="ai",
            confidence_score=0.95,
            anatomical_regions=["temporal lobe", "pterion"],
            procedure_types=["craniotomy"]
        )

        db_session.add(chapter)
        db_session.commit()

        assert chapter.id is not None
        assert chapter.title == "Temporal Craniotomy"
        assert chapter.confidence_score == 0.95
        assert "temporal lobe" in chapter.anatomical_regions

    def test_chapter_hierarchy(self, db_session):
        """Test nested chapter structure"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        # Parent chapter
        parent = Chapter(
            book_id=book.id,
            title="Part I: Cranial Surgery",
            start_page=1,
            end_page=100,
            level=1,
            detection_method="manual"
        )
        db_session.add(parent)
        db_session.commit()

        # Child chapters
        child1 = Chapter(
            book_id=book.id,
            parent_chapter_id=parent.id,
            title="Chapter 1: Approach",
            start_page=1,
            end_page=50,
            level=2,
            detection_method="manual"
        )
        child2 = Chapter(
            book_id=book.id,
            parent_chapter_id=parent.id,
            title="Chapter 2: Closure",
            start_page=51,
            end_page=100,
            level=2,
            detection_method="manual"
        )

        db_session.add_all([child1, child2])
        db_session.commit()

        # Test relationships
        assert len(parent.sub_chapters) == 2
        assert child1.parent_chapter.title == "Part I: Cranial Surgery"

    def test_chapter_sections_relationship(self, db_session):
        """Test chapter → sections relationship"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        chapter = Chapter(
            book_id=book.id,
            title="Test Chapter",
            start_page=1,
            end_page=10,
            detection_method="manual"
        )
        db_session.add(chapter)
        db_session.commit()

        section1 = Section(
            chapter_id=chapter.id,
            title="Introduction",
            content="Test content"
        )
        section2 = Section(
            chapter_id=chapter.id,
            title="Methods",
            content="Test content"
        )

        db_session.add_all([section1, section2])
        db_session.commit()

        assert len(chapter.sections) == 2


class TestImageModel:
    """Tests for Image model"""

    def test_create_image(self, db_session):
        """Test creating an image"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        chapter = Chapter(
            book_id=book.id,
            title="Test Chapter",
            start_page=1,
            end_page=10,
            detection_method="manual"
        )
        db_session.add(chapter)
        db_session.commit()

        image = Image(
            chapter_id=chapter.id,
            file_path="/images/figure_1.png",
            file_hash="image123",
            page_number=5,
            image_type="figure",
            width=800,
            height=600,
            caption="Figure 1. Temporal approach",
            ai_description="Surgical approach showing temporal craniotomy",
            anatomical_structures=["temporal bone", "dura"],
            quality_score=0.85
        )

        db_session.add(image)
        db_session.commit()

        assert image.id is not None
        assert image.quality_score == 0.85
        assert "temporal bone" in image.anatomical_structures


class TestProcessingLog:
    """Tests for ProcessingLog model"""

    def test_create_processing_log(self, db_session):
        """Test creating a processing log"""
        book = Book(
            title="Test Book",
            file_path="/test.pdf",
            file_size=1000,
            file_hash="test123"
        )
        db_session.add(book)
        db_session.commit()

        log = ProcessingLog(
            entity_type="book",
            entity_id=book.id,
            operation="index",
            status="success",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            duration_seconds=5.2,
            result_summary={'chapters_found': 15},
            tokens_used=1000,
            estimated_cost=0.002
        )

        db_session.add(log)
        db_session.commit()

        assert log.id is not None
        assert log.status == "success"
        assert log.duration_seconds == 5.2
