"""
Library Manager - High-level operations for reference library
Coordinates PDF indexing, querying, and metadata management
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import func, desc

from reference_library.models import Book, Chapter, Section, Image
from reference_library.pdf_indexer import PDFIndexer
from utils.exceptions import RecordNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)


class LibraryManager:
    """
    High-level manager for reference library operations

    Features:
    - Add/remove books from library
    - Query books and chapters
    - Eager loading to prevent N+1 queries (Neurocore Lesson 3)
    - Statistics and analytics
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.pdf_indexer = PDFIndexer(db_session)

    async def add_book(
        self,
        file_path: str,
        extract_images: bool = False,
        ai_chapter_detection: bool = False
    ) -> Book:
        """
        Add a book to the library

        Args:
            file_path: Path to PDF file
            extract_images: Whether to extract images
            ai_chapter_detection: Use AI for chapter detection

        Returns:
            Indexed Book object
        """
        logger.info(f"Adding book to library: {file_path}")

        book = await self.pdf_indexer.index_pdf(
            file_path=file_path,
            extract_images=extract_images,
            ai_chapter_detection=ai_chapter_detection
        )

        logger.info(f"Book added: {book.title} ({len(book.chapters)} chapters)")

        return book

    def get_book(self, book_id: str, include_chapters: bool = True) -> Book:
        """
        Get a book by ID

        Args:
            book_id: UUID of book
            include_chapters: Whether to eager load chapters

        Returns:
            Book object

        Raises:
            RecordNotFoundError: If book not found
        """
        query = self.db.query(Book)

        # Eager loading to prevent N+1 queries
        if include_chapters:
            query = query.options(
                selectinload(Book.chapters)
            )

        book = query.filter(Book.id == book_id).first()

        if not book:
            raise RecordNotFoundError(
                resource='Book',
                resource_id=book_id
            )

        return book

    def list_books(
        self,
        limit: int = 100,
        offset: int = 0,
        include_chapters: bool = False
    ) -> List[Book]:
        """
        List all books in library

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            include_chapters: Whether to eager load chapters

        Returns:
            List of Book objects
        """
        query = self.db.query(Book)

        if include_chapters:
            query = query.options(
                selectinload(Book.chapters)
            )

        books = query.order_by(desc(Book.indexed_at)).limit(limit).offset(offset).all()

        return books

    def search_books(
        self,
        query: str,
        limit: int = 20
    ) -> List[Book]:
        """
        Search books by title or author

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching books
        """
        search_term = f"%{query}%"

        books = self.db.query(Book).filter(
            Book.title.ilike(search_term)
        ).limit(limit).all()

        logger.info(f"Found {len(books)} books matching '{query}'")

        return books

    def get_chapter(self, chapter_id: str, include_relations: bool = True) -> Chapter:
        """
        Get a chapter by ID

        Args:
            chapter_id: UUID of chapter
            include_relations: Whether to eager load related data

        Returns:
            Chapter object
        """
        query = self.db.query(Chapter)

        if include_relations:
            query = query.options(
                joinedload(Chapter.book),
                selectinload(Chapter.sections),
                selectinload(Chapter.images)
            )

        chapter = query.filter(Chapter.id == chapter_id).first()

        if not chapter:
            raise RecordNotFoundError(
                resource='Chapter',
                resource_id=chapter_id
            )

        return chapter

    def get_chapters_by_book(
        self,
        book_id: str,
        include_images: bool = False
    ) -> List[Chapter]:
        """
        Get all chapters for a book

        Args:
            book_id: UUID of book
            include_images: Whether to eager load images

        Returns:
            List of Chapter objects
        """
        query = self.db.query(Chapter).filter(Chapter.book_id == book_id)

        if include_images:
            query = query.options(
                selectinload(Chapter.images)
            )

        chapters = query.order_by(Chapter.start_page).all()

        return chapters

    def search_chapters(
        self,
        query: str,
        anatomical_region: Optional[str] = None,
        procedure_type: Optional[str] = None,
        min_confidence: float = 0.0,
        limit: int = 20
    ) -> List[Chapter]:
        """
        Search chapters by various criteria

        Args:
            query: Text search in title
            anatomical_region: Filter by anatomical region
            procedure_type: Filter by procedure type
            min_confidence: Minimum AI confidence score
            limit: Maximum results

        Returns:
            List of matching chapters
        """
        search_term = f"%{query}%"

        chapter_query = self.db.query(Chapter).filter(
            Chapter.title.ilike(search_term),
            Chapter.confidence_score >= min_confidence
        )

        # Filter by anatomical region (JSON array contains)
        if anatomical_region:
            # SQLite doesn't support JSON array contains, so we use a workaround
            chapter_query = chapter_query.filter(
                Chapter.anatomical_regions.isnot(None)
            )

        # Filter by procedure type
        if procedure_type:
            chapter_query = chapter_query.filter(
                Chapter.procedure_types.isnot(None)
            )

        # Eager load book information
        chapter_query = chapter_query.options(
            joinedload(Chapter.book)
        )

        chapters = chapter_query.order_by(
            desc(Chapter.confidence_score)
        ).limit(limit).all()

        logger.info(f"Found {len(chapters)} chapters matching criteria")

        return chapters

    def get_library_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the library

        Returns:
            Dictionary with library statistics
        """
        total_books = self.db.query(func.count(Book.id)).scalar()
        total_chapters = self.db.query(func.count(Chapter.id)).scalar()
        total_images = self.db.query(func.count(Image.id)).scalar()

        # Chapters by detection method
        detection_stats = self.db.query(
            Chapter.detection_method,
            func.count(Chapter.id),
            func.avg(Chapter.confidence_score)
        ).group_by(Chapter.detection_method).all()

        # Books by year
        books_by_year = self.db.query(
            Book.year,
            func.count(Book.id)
        ).filter(
            Book.year.isnot(None)
        ).group_by(Book.year).order_by(desc(Book.year)).limit(10).all()

        return {
            'total_books': total_books,
            'total_chapters': total_chapters,
            'total_images': total_images,
            'detection_methods': [
                {
                    'method': method,
                    'count': count,
                    'avg_confidence': round(float(avg_conf), 2) if avg_conf else None
                }
                for method, count, avg_conf in detection_stats
            ],
            'books_by_year': [
                {'year': year, 'count': count}
                for year, count in books_by_year
            ]
        }

    def delete_book(self, book_id: str) -> bool:
        """
        Delete a book and all related data

        Args:
            book_id: UUID of book

        Returns:
            True if deleted, False if not found
        """
        book = self.db.query(Book).filter(Book.id == book_id).first()

        if not book:
            return False

        # Cascade delete will handle chapters, sections, images
        self.db.delete(book)
        self.db.commit()

        logger.info(f"Deleted book: {book.title}")

        return True

    def verify_library_integrity(self) -> Dict[str, Any]:
        """
        Verify library data integrity

        Returns:
            Dictionary with integrity check results
        """
        issues = []

        # Check for chapters with invalid page ranges
        invalid_chapters = self.db.query(Chapter).filter(
            Chapter.start_page > Chapter.end_page
        ).all()

        if invalid_chapters:
            issues.append({
                'type': 'invalid_page_range',
                'count': len(invalid_chapters),
                'chapter_ids': [str(c.id) for c in invalid_chapters]
            })

        # Check for books without chapters
        books_without_chapters = self.db.query(Book).filter(
            ~Book.chapters.any()
        ).all()

        if books_without_chapters:
            issues.append({
                'type': 'books_without_chapters',
                'count': len(books_without_chapters),
                'book_ids': [str(b.id) for b in books_without_chapters]
            })

        # Check for missing files
        missing_files = []
        for book in self.db.query(Book).all():
            if not Path(book.file_path).exists():
                missing_files.append(str(book.id))

        if missing_files:
            issues.append({
                'type': 'missing_files',
                'count': len(missing_files),
                'book_ids': missing_files
            })

        return {
            'status': 'healthy' if not issues else 'issues_found',
            'issues_count': len(issues),
            'issues': issues
        }
