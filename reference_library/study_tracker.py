"""
Study session tracker for progress monitoring.
Tracks study time, topics covered, and progress metrics.
"""
from typing import List, Optional
from datetime import datetime, timedelta

from reference_library.models import StudySession, DatabaseManager
from utils.logger import logger


class StudyTracker:
    """Tracks study sessions and progress."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize study tracker.
        
        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager
    
    def start_session(self, topic: str, book_id: Optional[int] = None) -> dict:
        """
        Start a new study session.
        
        Args:
            topic: Study topic
            book_id: Optional book ID
        
        Returns:
            Session info with start time
        """
        return {
            "topic": topic,
            "book_id": book_id,
            "start_time": datetime.utcnow()
        }
    
    def end_session(self, session_info: dict, notes_count: int = 0, 
                   flashcards_reviewed: int = 0) -> StudySession:
        """
        End a study session and save it.
        
        Args:
            session_info: Session info from start_session
            notes_count: Number of notes created/reviewed
            flashcards_reviewed: Number of flashcards reviewed
        
        Returns:
            Created StudySession object
        """
        duration = (datetime.utcnow() - session_info["start_time"]).total_seconds() / 60
        
        session = self.db_manager.get_session()
        try:
            study_session = StudySession(
                topic=session_info["topic"],
                book_id=session_info.get("book_id"),
                duration_minutes=int(duration),
                notes_count=notes_count,
                flashcards_reviewed=flashcards_reviewed,
                date=datetime.utcnow()
            )
            session.add(study_session)
            session.commit()
            session.refresh(study_session)
            
            logger.info(f"Completed study session: {session_info['topic']} ({int(duration)}min)")
            return study_session
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save study session: {e}")
            raise
        finally:
            session.close()
    
    def get_recent_sessions(self, days: int = 7) -> List[StudySession]:
        """
        Get recent study sessions.
        
        Args:
            days: Number of days to look back
        
        Returns:
            List of StudySession objects
        """
        since = datetime.utcnow() - timedelta(days=days)
        
        session = self.db_manager.get_session()
        try:
            sessions = session.query(StudySession).filter(
                StudySession.date >= since
            ).order_by(StudySession.date.desc()).all()
            return sessions
        finally:
            session.close()
    
    def get_stats(self, days: int = 7) -> dict:
        """
        Get study statistics.
        
        Args:
            days: Number of days to look back
        
        Returns:
            Dictionary with statistics
        """
        sessions = self.get_recent_sessions(days)
        
        total_minutes = sum(s.duration_minutes for s in sessions)
        total_notes = sum(s.notes_count for s in sessions)
        total_flashcards = sum(s.flashcards_reviewed for s in sessions)
        
        # Get unique topics
        topics = set(s.topic for s in sessions if s.topic)
        
        return {
            "period_days": days,
            "total_sessions": len(sessions),
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "avg_session_minutes": int(total_minutes / len(sessions)) if sessions else 0,
            "total_notes": total_notes,
            "total_flashcards_reviewed": total_flashcards,
            "unique_topics": len(topics),
            "topics": sorted(topics)
        }
