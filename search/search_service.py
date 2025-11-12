"""
Simple search service for StudyBuddy.
Searches across books, notes, and flashcards.
"""
from typing import List, Dict, Any
from reference_library.models import Book, Note, Flashcard, DatabaseManager


class SearchService:
    """Simple search across all content."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize search service.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def _sanitize_query(self, query: str) -> str:
        """
        Sanitize search query to prevent SQL injection.
        Escape special SQL LIKE characters.
        
        Args:
            query: Raw search query
        
        Returns:
            Sanitized query string
        """
        # Escape special LIKE characters
        query = query.replace('%', r'\%').replace('_', r'\_')
        return query
    
    def search_all(self, query: str, limit: int = 20) -> Dict[str, List[Any]]:
        """
        Search across all content types.
        
        Args:
            query: Search query
            limit: Maximum results per type
        
        Returns:
            Dictionary with results by type
        """
        # Sanitize query
        safe_query = self._sanitize_query(query)
        
        session = self.db_manager.get_session()
        try:
            # Search books
            books = session.query(Book).filter(
                (Book.title.ilike(f"%{safe_query}%")) | 
                (Book.author.ilike(f"%{safe_query}%"))
            ).limit(limit).all()
            
            # Search notes
            notes = session.query(Note).filter(
                (Note.topic.ilike(f"%{safe_query}%")) | 
                (Note.content.ilike(f"%{safe_query}%")) |
                (Note.tags.ilike(f"%{safe_query}%"))
            ).limit(limit).all()
            
            # Search flashcards
            flashcards = session.query(Flashcard).filter(
                (Flashcard.question.ilike(f"%{safe_query}%")) | 
                (Flashcard.answer.ilike(f"%{safe_query}%")) |
                (Flashcard.topic.ilike(f"%{safe_query}%"))
            ).limit(limit).all()
            
            return {
                "books": books,
                "notes": notes,
                "flashcards": flashcards,
                "total": len(books) + len(notes) + len(flashcards)
            }
        finally:
            session.close()
