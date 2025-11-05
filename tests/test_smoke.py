"""
Basic smoke tests for StudyBuddy.
Validates core functionality is working.
"""
import tempfile
from pathlib import Path
import pytest

from reference_library.models import DatabaseManager
from reference_library.library_manager import LibraryManager
from reference_library.notes_manager import NotesManager
from reference_library.flashcard_manager import FlashcardManager
from utils.config import AppConfig


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db_manager = DatabaseManager(str(db_path))
        yield db_manager


@pytest.fixture
def library_manager(temp_db):
    """Create a library manager with temp database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        books_dir = Path(tmpdir) / "books"
        books_dir.mkdir(exist_ok=True)
        yield LibraryManager(temp_db, books_dir)


def test_config_loads():
    """Test that configuration loads successfully."""
    config = AppConfig()
    assert config.app_name == "StudyBuddy"
    assert config.version == "0.1.0"
    assert config.study.default_session_duration_minutes == 25


def test_database_creation(temp_db):
    """Test database is created with correct tables."""
    session = temp_db.get_session()
    try:
        # Check that we can query (tables exist)
        from reference_library.models import Book, Note, Flashcard, StudySession
        
        books = session.query(Book).all()
        notes = session.query(Note).all()
        flashcards = session.query(Flashcard).all()
        sessions = session.query(StudySession).all()
        
        assert books == []
        assert notes == []
        assert flashcards == []
        assert sessions == []
    finally:
        session.close()


def test_notes_manager(temp_db):
    """Test notes manager basic operations."""
    notes_mgr = NotesManager(temp_db)
    
    # Create a note
    note = notes_mgr.create_note(
        topic="Craniotomy Approach",
        content="Standard pterional approach involves...",
        tags="surgery,craniotomy"
    )
    
    assert note.id is not None
    assert note.topic == "Craniotomy Approach"
    
    # List notes
    notes = notes_mgr.list_notes()
    assert len(notes) == 1
    
    # Search notes
    results = notes_mgr.search_notes("craniotomy")
    assert len(results) == 1


def test_flashcard_manager(temp_db):
    """Test flashcard manager basic operations."""
    flashcard_mgr = FlashcardManager(temp_db)
    
    # Create a flashcard
    card = flashcard_mgr.create_flashcard(
        question="What is the Circle of Willis?",
        answer="An arterial circle at the base of the brain",
        topic="Neuroanatomy"
    )
    
    assert card.id is not None
    assert card.ease_factor == 2.5
    assert card.interval_days == 1
    
    # Get due flashcards
    due = flashcard_mgr.get_due_flashcards()
    assert len(due) == 1
    
    # Review flashcard with perfect recall
    updated = flashcard_mgr.review_flashcard(card.id, quality=5)
    assert updated.repetitions == 1
    assert updated.interval_days == 1  # First repetition
    
    # Stats
    stats = flashcard_mgr.get_stats()
    assert stats['total'] == 1


def test_exception_hierarchy():
    """Test custom exceptions are structured correctly."""
    from utils.exceptions import (
        StudyBuddyException, DatabaseError, FileError,
        ValidationError, InvalidInputError
    )
    
    # Test base exception
    exc = StudyBuddyException("Test error", "TEST_001", {"key": "value"})
    assert exc.error_code == "TEST_001"
    assert exc.context["key"] == "value"
    assert "[TEST_001]" in str(exc)
    
    # Test inheritance
    assert issubclass(DatabaseError, StudyBuddyException)
    assert issubclass(FileError, StudyBuddyException)
    assert issubclass(ValidationError, StudyBuddyException)
    assert issubclass(InvalidInputError, ValidationError)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
