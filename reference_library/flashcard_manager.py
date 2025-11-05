"""
Flashcard manager with spaced repetition algorithm.
Implements a simplified SM-2 algorithm for optimal learning.
"""
from typing import List, Optional
from datetime import datetime, timedelta

from reference_library.models import Flashcard, DatabaseManager
from utils.exceptions import RecordNotFoundError
from utils.logger import logger


class FlashcardManager:
    """Manages flashcards with spaced repetition learning."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize flashcard manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def create_flashcard(self, question: str, answer: str, topic: Optional[str] = None,
                        book_id: Optional[int] = None) -> Flashcard:
        """
        Create a new flashcard.
        
        Args:
            question: Flashcard question
            answer: Flashcard answer
            topic: Optional topic/category
            book_id: Optional book ID this card relates to
        
        Returns:
            Created Flashcard object
        """
        session = self.db_manager.get_session()
        try:
            flashcard = Flashcard(
                question=question,
                answer=answer,
                topic=topic,
                book_id=book_id,
                created_at=datetime.utcnow(),
                next_review=datetime.utcnow()  # Available for immediate review
            )
            session.add(flashcard)
            session.commit()
            session.refresh(flashcard)
            
            logger.info(f"Created flashcard: {topic}")
            return flashcard
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to create flashcard: {e}")
            raise
        finally:
            session.close()
    
    def get_due_flashcards(self, topic: Optional[str] = None, limit: int = 20) -> List[Flashcard]:
        """
        Get flashcards that are due for review.
        
        Args:
            topic: Optional topic filter
            limit: Maximum number of cards to return
        
        Returns:
            List of due Flashcard objects
        """
        session = self.db_manager.get_session()
        try:
            query = session.query(Flashcard).filter(
                Flashcard.next_review <= datetime.utcnow()
            )
            
            if topic:
                query = query.filter(Flashcard.topic.ilike(f"%{topic}%"))
            
            flashcards = query.order_by(Flashcard.next_review).limit(limit).all()
            return flashcards
        finally:
            session.close()
    
    def review_flashcard(self, flashcard_id: int, quality: int) -> Flashcard:
        """
        Record a flashcard review and update scheduling using SM-2 algorithm.
        
        Args:
            flashcard_id: Flashcard ID
            quality: Quality of recall (0-5)
                    0-2: Incorrect, restart
                    3: Correct with difficulty
                    4: Correct with hesitation
                    5: Perfect recall
        
        Returns:
            Updated Flashcard object
        
        Raises:
            RecordNotFoundError: If flashcard not found
        """
        session = self.db_manager.get_session()
        try:
            card = session.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
            if not card:
                raise RecordNotFoundError("Flashcard", str(flashcard_id))
            
            # SM-2 Algorithm
            if quality < 3:
                # Incorrect - restart
                card.repetitions = 0
                card.interval_days = 1
            else:
                # Correct - calculate next interval
                if card.repetitions == 0:
                    card.interval_days = 1
                elif card.repetitions == 1:
                    card.interval_days = 6
                else:
                    card.interval_days = int(card.interval_days * card.ease_factor)
                
                card.repetitions += 1
                
                # Update ease factor
                card.ease_factor = max(1.3, card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            
            # Set next review date
            card.last_reviewed = datetime.utcnow()
            card.next_review = datetime.utcnow() + timedelta(days=card.interval_days)
            
            session.commit()
            session.refresh(card)
            
            logger.info(f"Reviewed flashcard {card.id}, next review in {card.interval_days} days")
            return card
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to review flashcard: {e}")
            raise
        finally:
            session.close()
    
    def list_flashcards(self, book_id: Optional[int] = None, 
                       topic: Optional[str] = None) -> List[Flashcard]:
        """
        List all flashcards, optionally filtered.
        
        Args:
            book_id: Optional book ID filter
            topic: Optional topic filter
        
        Returns:
            List of Flashcard objects
        """
        session = self.db_manager.get_session()
        try:
            query = session.query(Flashcard)
            
            if book_id:
                query = query.filter(Flashcard.book_id == book_id)
            if topic:
                query = query.filter(Flashcard.topic.ilike(f"%{topic}%"))
            
            flashcards = query.order_by(Flashcard.created_at.desc()).all()
            return flashcards
        finally:
            session.close()
    
    def delete_flashcard(self, flashcard_id: int) -> None:
        """
        Delete a flashcard.
        
        Args:
            flashcard_id: Flashcard ID to delete
        
        Raises:
            RecordNotFoundError: If flashcard not found
        """
        session = self.db_manager.get_session()
        try:
            card = session.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
            if not card:
                raise RecordNotFoundError("Flashcard", str(flashcard_id))
            
            session.delete(card)
            session.commit()
            
            logger.info(f"Deleted flashcard {flashcard_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete flashcard: {e}")
            raise
        finally:
            session.close()
    
    def get_stats(self) -> dict:
        """
        Get flashcard statistics.
        
        Returns:
            Dictionary with statistics
        """
        session = self.db_manager.get_session()
        try:
            total = session.query(Flashcard).count()
            due = session.query(Flashcard).filter(
                Flashcard.next_review <= datetime.utcnow()
            ).count()
            
            return {
                "total": total,
                "due": due,
                "mastered": total - due if total > due else 0
            }
        finally:
            session.close()
