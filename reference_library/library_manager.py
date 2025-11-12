"""
Library manager for PDF books and references.
Comprehensive PDF processing with text and image extraction.
"""
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from PyPDF2 import PdfReader

from reference_library.models import Book, DatabaseManager, ExtractedPage, ExtractedImage
from reference_library.pdf_extractor import PDFContentExtractor
from utils.exceptions import FileNotFoundError, InvalidFileFormatError, RecordNotFoundError
from utils.logger import logger


class LibraryManager:
    """Manages the reference library of medical textbooks with content extraction."""
    
    def __init__(self, db_manager: DatabaseManager, books_dir: Path, images_dir: Path):
        """
        Initialize library manager.
        
        Args:
            db_manager: Database manager instance
            books_dir: Directory to store books
            images_dir: Directory to store extracted images
        """
        self.db_manager = db_manager
        self.books_dir = Path(books_dir)
        self.images_dir = Path(images_dir)
        self.books_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.pdf_extractor = PDFContentExtractor(images_dir)
    
    def add_book(self, pdf_path: str, title: Optional[str] = None, 
                 author: Optional[str] = None, extract_content: bool = True) -> Book:
        """
        Add a new book to the library and optionally extract content.
        
        Args:
            pdf_path: Path to PDF file
            title: Optional book title (uses filename if not provided)
            author: Optional author name
            extract_content: Whether to extract text and images
        
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
                added_at=datetime.utcnow(),
                text_extracted=False,
                images_extracted=False
            )
            session.add(book)
            session.commit()
            session.refresh(book)
            
            logger.info(f"Added book: {title} ({total_pages} pages)")
            
            # Extract content if requested
            if extract_content:
                self._extract_and_store_content(book, dest_path)
            
            return book
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add book: {e}")
            raise
        finally:
            session.close()
    
    def _extract_and_store_content(self, book: Book, pdf_path: Path) -> None:
        """
        Extract and store content from PDF.
        
        Args:
            book: Book object
            pdf_path: Path to PDF file
        """
        logger.info(f"Extracting content from: {book.title}")
        
        try:
            # Extract all content
            extracted = self.pdf_extractor.extract_all_content(str(pdf_path), book.id)
            
            session = self.db_manager.get_session()
            try:
                # Store extracted pages
                for page_data in extracted["text_content"]:
                    extracted_page = ExtractedPage(
                        book_id=book.id,
                        page_number=page_data["page_number"],
                        text_content=page_data["text"],
                        word_count=page_data["word_count"],
                        has_tables=len(page_data.get("tables", [])) > 0,
                        extracted_at=datetime.utcnow()
                    )
                    session.add(extracted_page)
                
                # Store extracted images
                for img_data in extracted["images"]:
                    extracted_image = ExtractedImage(
                        book_id=book.id,
                        page_number=img_data["page_number"],
                        image_path=img_data["path"],
                        filename=img_data["filename"],
                        width=img_data["width"],
                        height=img_data["height"],
                        size_kb=img_data["size_kb"],
                        extracted_at=datetime.utcnow()
                    )
                    session.add(extracted_image)
                
                # Update book flags
                book.text_extracted = True
                book.images_extracted = True
                
                session.commit()
                
                logger.info(f"Stored {len(extracted['text_content'])} pages and "
                          f"{len(extracted['images'])} images for book: {book.title}")
            
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to store extracted content: {e}")
                raise
            finally:
                session.close()
        
        except Exception as e:
            logger.error(f"Content extraction failed: {e}")
            # Don't fail the whole operation if extraction fails
    
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
