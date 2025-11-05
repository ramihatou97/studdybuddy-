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
    
    def search_all(self, query: str, limit: int = 20) -> Dict[str, List[Any]]:
        """
        Search across all content types.
        
        Args:
            query: Search query
            limit: Maximum results per type
        
        Returns:
            Dictionary with results by type
        """
        session = self.db_manager.get_session()
        try:
            # Search books
            books = session.query(Book).filter(
                (Book.title.ilike(f"%{query}%")) | 
                (Book.author.ilike(f"%{query}%"))
            ).limit(limit).all()
            
            # Search notes
            notes = session.query(Note).filter(
                (Note.topic.ilike(f"%{query}%")) | 
                (Note.content.ilike(f"%{query}%")) |
                (Note.tags.ilike(f"%{query}%"))
            ).limit(limit).all()
            
            # Search flashcards
            flashcards = session.query(Flashcard).filter(
                (Flashcard.question.ilike(f"%{query}%")) | 
                (Flashcard.answer.ilike(f"%{query}%")) |
                (Flashcard.topic.ilike(f"%{query}%"))
            ).limit(limit).all()
            
            return {
                "books": books,
                "notes": notes,
                "flashcards": flashcards,
                "total": len(books) + len(notes) + len(flashcards)
            }
        finally:
            session.close()
