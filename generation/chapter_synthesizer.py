"""
AI-powered chapter synthesis from extracted medical content.
Generates comprehensive medical-grade chapters from reference materials.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from reference_library.models import (
    DatabaseManager, ExtractedPage, ExtractedImage, Chapter, Book
)
from utils.logger import logger
from utils.exceptions import ValidationError


class ChapterSynthesizer:
    """Synthesizes comprehensive medical chapters from extracted content."""
    
    def __init__(self, db_manager: DatabaseManager, ai_provider: Optional[Any] = None):
        """
        Initialize chapter synthesizer.
        
        Args:
            db_manager: Database manager instance
            ai_provider: Optional AI provider (Anthropic, OpenAI, etc.)
        """
        self.db_manager = db_manager
        self.ai_provider = ai_provider
    
    def generate_chapter(self, subject: str, book_ids: List[int], 
                        search_terms: Optional[List[str]] = None) -> Chapter:
        """
        Generate a comprehensive medical chapter on a subject.
        
        Args:
            subject: Chapter subject/topic
            book_ids: List of book IDs to use as sources
            search_terms: Optional specific terms to search for
        
        Returns:
            Generated Chapter object
        """
        logger.info(f"Generating chapter on: {subject}")
        
        # Collect all relevant content
        relevant_content = self._collect_relevant_content(book_ids, subject, search_terms)
        
        if not relevant_content["pages"]:
            raise ValidationError("subject", "No relevant content found for this subject")
        
        # Organize content by relevance
        organized_content = self._organize_content(relevant_content, subject)
        
        # Generate chapter using AI (or template if no AI available)
        chapter_content = self._synthesize_chapter(subject, organized_content)
        
        # Create chapter record
        session = self.db_manager.get_session()
        try:
            chapter = Chapter(
                book_id=book_ids[0] if book_ids else None,
                title=subject,
                subject=subject,
                content=chapter_content,
                source_pages=",".join(str(p) for p in organized_content["page_ids"]),
                source_images=",".join(str(i) for i in organized_content["image_ids"]),
                created_at=datetime.utcnow(),
                ai_model_used=self._get_ai_model_name()
            )
            
            session.add(chapter)
            session.commit()
            session.refresh(chapter)
            
            logger.info(f"Created chapter: {subject} (ID: {chapter.id})")
            return chapter
        
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create chapter: {e}")
            raise
        finally:
            session.close()
    
    def _collect_relevant_content(self, book_ids: List[int], subject: str,
                                  search_terms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Collect all relevant pages and images from specified books.
        
        Args:
            book_ids: List of book IDs to search
            subject: Main subject
            search_terms: Additional search terms
        
        Returns:
            Dictionary with relevant pages and images
        """
        session = self.db_manager.get_session()
        
        try:
            all_terms = [subject.lower()]
            if search_terms:
                all_terms.extend([term.lower() for term in search_terms])
            
            relevant_pages = []
            relevant_images = []
            
            # Search through extracted pages
            for book_id in book_ids:
                pages = session.query(ExtractedPage).filter(
                    ExtractedPage.book_id == book_id
                ).all()
                
                for page in pages:
                    text_lower = (page.text_content or "").lower()
                    
                    # Check if any search term is in the page
                    if any(term in text_lower for term in all_terms):
                        relevant_pages.append({
                            "id": page.id,
                            "book_id": page.book_id,
                            "page_number": page.page_number,
                            "text": page.text_content,
                            "word_count": page.word_count
                        })
                
                # Get images from relevant pages
                page_numbers = [p["page_number"] for p in relevant_pages if p["book_id"] == book_id]
                if page_numbers:
                    images = session.query(ExtractedImage).filter(
                        ExtractedImage.book_id == book_id,
                        ExtractedImage.page_number.in_(page_numbers)
                    ).all()
                    
                    for img in images:
                        relevant_images.append({
                            "id": img.id,
                            "book_id": img.book_id,
                            "page_number": img.page_number,
                            "path": img.image_path,
                            "filename": img.filename,
                            "annotation": img.annotation
                        })
            
            return {
                "pages": relevant_pages,
                "images": relevant_images
            }
        
        finally:
            session.close()
    
    def _organize_content(self, content: Dict[str, Any], subject: str) -> Dict[str, Any]:
        """
        Organize collected content by relevance and structure.
        
        Args:
            content: Raw collected content
            subject: Chapter subject
        
        Returns:
            Organized content structure
        """
        # Sort pages by relevance (word count as proxy for detail)
        sorted_pages = sorted(content["pages"], 
                             key=lambda x: x["word_count"], 
                             reverse=True)
        
        # Combine text from all pages
        combined_text = "\n\n".join([
            f"[Page {p['page_number']} from Book {p['book_id']}]\n{p['text']}"
            for p in sorted_pages
        ])
        
        return {
            "combined_text": combined_text,
            "page_ids": [p["id"] for p in sorted_pages],
            "image_ids": [i["id"] for i in content["images"]],
            "total_pages": len(sorted_pages),
            "total_images": len(content["images"]),
            "images": content["images"]
        }
    
    def _synthesize_chapter(self, subject: str, organized_content: Dict[str, Any]) -> str:
        """
        Synthesize chapter content from organized materials.
        
        Args:
            subject: Chapter subject
            organized_content: Organized source content
        
        Returns:
            Synthesized chapter text
        """
        if self.ai_provider:
            # Use AI provider for synthesis
            return self._ai_synthesize(subject, organized_content)
        else:
            # Use template-based synthesis
            return self._template_synthesize(subject, organized_content)
    
    def _template_synthesize(self, subject: str, organized_content: Dict[str, Any]) -> str:
        """
        Create chapter using template (no AI).
        
        Args:
            subject: Chapter subject
            organized_content: Organized content
        
        Returns:
            Formatted chapter text
        """
        chapter = f"# {subject}\n\n"
        chapter += f"## Overview\n\n"
        chapter += f"This chapter synthesizes information from {organized_content['total_pages']} "
        chapter += f"pages and includes {organized_content['total_images']} figures.\n\n"
        
        chapter += f"## Comprehensive Content\n\n"
        chapter += organized_content["combined_text"]
        
        if organized_content["images"]:
            chapter += f"\n\n## Figures and Illustrations\n\n"
            for idx, img in enumerate(organized_content["images"], 1):
                chapter += f"{idx}. Page {img['page_number']}: {img['filename']}\n"
                if img["annotation"]:
                    chapter += f"   Annotation: {img['annotation']}\n"
        
        chapter += f"\n\n---\n"
        chapter += f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n"
        chapter += f"Sources: {organized_content['total_pages']} pages from reference materials\n"
        
        return chapter
    
    def _ai_synthesize(self, subject: str, organized_content: Dict[str, Any]) -> str:
        """
        Use AI to synthesize chapter (placeholder for AI integration).
        
        Args:
            subject: Chapter subject
            organized_content: Organized content
        
        Returns:
            AI-synthesized chapter text
        """
        # This would use Anthropic Claude or OpenAI GPT
        # For now, fall back to template
        logger.info("AI synthesis would be used here with configured provider")
        return self._template_synthesize(subject, organized_content)
    
    def _get_ai_model_name(self) -> str:
        """Get the name of the AI model being used."""
        if self.ai_provider:
            return "AI Provider (configured)"
        return "Template-based"
    
    def list_chapters(self, book_id: Optional[int] = None) -> List[Chapter]:
        """
        List all generated chapters.
        
        Args:
            book_id: Optional filter by book ID
        
        Returns:
            List of Chapter objects
        """
        session = self.db_manager.get_session()
        try:
            query = session.query(Chapter)
            if book_id:
                query = query.filter(Chapter.book_id == book_id)
            
            chapters = query.order_by(Chapter.created_at.desc()).all()
            return chapters
        finally:
            session.close()
    
    def get_chapter(self, chapter_id: int) -> Optional[Chapter]:
        """
        Get a specific chapter.
        
        Args:
            chapter_id: Chapter ID
        
        Returns:
            Chapter object or None
        """
        session = self.db_manager.get_session()
        try:
            chapter = session.query(Chapter).filter(Chapter.id == chapter_id).first()
            return chapter
        finally:
            session.close()
