"""
Library manager for PDF books and references.
Simple CRUD operations for medical textbooks.
"""
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from PyPDF2 import PdfReader

from reference_library.models import Book, DatabaseManager
from utils.exceptions import FileNotFoundError, InvalidFileFormatError, RecordNotFoundError
from utils.logger import logger


class LibraryManager:
    """Manages the reference library of medical textbooks."""
    
    def __init__(self, db_manager: DatabaseManager, books_dir: Path):
        """
        Initialize library manager.
        
        Args:
            db_manager: Database manager instance
            books_dir: Directory to store books
        """
        self.db_manager = db_manager
        self.books_dir = Path(books_dir)
        self.books_dir.mkdir(parents=True, exist_ok=True)
    
    def add_book(self, pdf_path: str, title: Optional[str] = None, 
                 author: Optional[str] = None) -> Book:
        """
        Add a new book to the library.
        
        Args:
            pdf_path: Path to PDF file
            title: Optional book title (uses filename if not provided)
            author: Optional author name
        
        Returns:
            Created Book object
        
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            InvalidFileFormatError: If file is not a valid PDF
        """
        pdf_path = Path(pdf_path)
        
        # Validate file exists
        if not pdf_path.exists():
            raise FileNotFoundError(str(pdf_path))
        
        # Validate PDF format
        if pdf_path.suffix.lower() != '.pdf':
            raise InvalidFileFormatError(str(pdf_path), "PDF")
        
        # Try to read PDF to validate it
        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
        except Exception as e:
            logger.error(f"Failed to read PDF: {e}")
            raise InvalidFileFormatError(str(pdf_path), "Valid PDF")
        
        # Use filename as title if not provided
        if not title:
            title = pdf_path.stem
        
        # Copy file to library directory
        dest_path = self.books_dir / pdf_path.name
        if pdf_path != dest_path:
            shutil.copy2(pdf_path, dest_path)
        
        # Create book record
        session = self.db_manager.get_session()
        try:
            book = Book(
                title=title,
                file_path=str(dest_path),
                author=author,
                total_pages=total_pages,
                added_at=datetime.utcnow()
            )
            session.add(book)
            session.commit()
            session.refresh(book)
            
            logger.info(f"Added book: {title} ({total_pages} pages)")
            return book
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add book: {e}")
            raise
        finally:
            session.close()
    
    def list_books(self) -> List[Book]:
        """
        List all books in the library.
        
        Returns:
            List of Book objects
        """
        session = self.db_manager.get_session()
        try:
            books = session.query(Book).order_by(Book.added_at.desc()).all()
            return books
        finally:
            session.close()
    
    def get_book(self, book_id: int) -> Book:
        """
        Get a specific book by ID.
        
        Args:
            book_id: Book ID
        
        Returns:
            Book object
        
        Raises:
            RecordNotFoundError: If book not found
        """
        session = self.db_manager.get_session()
        try:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise RecordNotFoundError("Book", str(book_id))
            return book
        finally:
            session.close()
    
    def search_books(self, query: str) -> List[Book]:
        """
        Search books by title or author.
        
        Args:
            query: Search query
        
        Returns:
            List of matching Book objects
        """
        session = self.db_manager.get_session()
        try:
            books = session.query(Book).filter(
                (Book.title.ilike(f"%{query}%")) | 
                (Book.author.ilike(f"%{query}%"))
            ).all()
            return books
        finally:
            session.close()
    
    def remove_book(self, book_id: int) -> None:
        """
        Remove a book from the library.
        
        Args:
            book_id: Book ID to remove
        
        Raises:
            RecordNotFoundError: If book not found
        """
        session = self.db_manager.get_session()
        try:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise RecordNotFoundError("Book", str(book_id))
            
            # Delete the file
            file_path = Path(book.file_path)
            if file_path.exists():
                file_path.unlink()
            
            # Delete the record
            session.delete(book)
            session.commit()
            
            logger.info(f"Removed book: {book.title}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to remove book: {e}")
            raise
        finally:
            session.close()
