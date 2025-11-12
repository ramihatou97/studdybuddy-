"""
Notes manager for study notes.
Simple note-taking functionality for neurosurgical topics.
"""
from typing import List, Optional
from datetime import datetime

from reference_library.models import Note, DatabaseManager
from utils.exceptions import RecordNotFoundError
from utils.logger import logger


class NotesManager:
    """Manages study notes."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize notes manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def create_note(self, topic: str, content: str, book_id: Optional[int] = None,
                    page_number: Optional[int] = None, tags: Optional[str] = None) -> Note:
        """
        Create a new study note.
        
        Args:
            topic: Note topic/title
            content: Note content
            book_id: Optional book ID this note relates to
            page_number: Optional page number reference
            tags: Optional comma-separated tags
        
        Returns:
            Created Note object
        """
        session = self.db_manager.get_session()
        try:
            note = Note(
                topic=topic,
                content=content,
                book_id=book_id,
                page_number=page_number,
                tags=tags,
                created_at=datetime.utcnow()
            )
            session.add(note)
            session.commit()
            session.refresh(note)
            
            logger.info(f"Created note: {topic}")
            return note
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create note: {e}")
            raise
        finally:
            session.close()
    
    def get_note(self, note_id: int) -> Note:
        """
        Get a specific note by ID.
        
        Args:
            note_id: Note ID
        
        Returns:
            Note object
        
        Raises:
            RecordNotFoundError: If note not found
        """
        session = self.db_manager.get_session()
        try:
            note = session.query(Note).filter(Note.id == note_id).first()
            if not note:
                raise RecordNotFoundError("Note", str(note_id))
            return note
        finally:
            session.close()
    
    def list_notes(self, book_id: Optional[int] = None) -> List[Note]:
        """
        List all notes, optionally filtered by book.
        
        Args:
            book_id: Optional book ID to filter by
        
        Returns:
            List of Note objects
        """
        session = self.db_manager.get_session()
        try:
            query = session.query(Note)
            if book_id:
                query = query.filter(Note.book_id == book_id)
            notes = query.order_by(Note.created_at.desc()).all()
            return notes
        finally:
            session.close()
    
    def search_notes(self, query: str) -> List[Note]:
        """
        Search notes by topic, content, or tags.
        
        Args:
            query: Search query
        
        Returns:
            List of matching Note objects
        """
        session = self.db_manager.get_session()
        try:
            notes = session.query(Note).filter(
                (Note.topic.ilike(f"%{query}%")) | 
                (Note.content.ilike(f"%{query}%")) |
                (Note.tags.ilike(f"%{query}%"))
            ).order_by(Note.updated_at.desc()).all()
            return notes
        finally:
            session.close()
    
    def update_note(self, note_id: int, topic: Optional[str] = None,
                    content: Optional[str] = None, tags: Optional[str] = None) -> Note:
        """
        Update an existing note.
        
        Args:
            note_id: Note ID to update
            topic: New topic (if provided)
            content: New content (if provided)
            tags: New tags (if provided)
        
        Returns:
            Updated Note object
        
        Raises:
            RecordNotFoundError: If note not found
        """
        session = self.db_manager.get_session()
        try:
            note = session.query(Note).filter(Note.id == note_id).first()
            if not note:
                raise RecordNotFoundError("Note", str(note_id))
            
            if topic:
                note.topic = topic
            if content:
                note.content = content
            if tags is not None:
                note.tags = tags
            
            note.updated_at = datetime.utcnow()
            session.commit()
            session.refresh(note)
            
            logger.info(f"Updated note: {note.topic}")
            return note
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update note: {e}")
            raise
        finally:
            session.close()
    
    def delete_note(self, note_id: int) -> None:
        """
        Delete a note.
        
        Args:
            note_id: Note ID to delete
        
        Raises:
            RecordNotFoundError: If note not found
        """
        session = self.db_manager.get_session()
        try:
            note = session.query(Note).filter(Note.id == note_id).first()
            if not note:
                raise RecordNotFoundError("Note", str(note_id))
            
            session.delete(note)
            session.commit()
            
            logger.info(f"Deleted note: {note.topic}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete note: {e}")
            raise
        finally:
            session.close()
