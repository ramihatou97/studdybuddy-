"""
Database session management with connection pooling
Implements Neurocore Lesson 3: Eager loading to prevent N+1 queries
"""

from contextlib import contextmanager
from typing import Generator, Optional
import os

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from utils.config import get_settings
from utils.exceptions import DatabaseConnectionError
from utils.logger import get_logger
from reference_library.models import Base

logger = get_logger(__name__)


class DatabaseManager:
    """
    Manages database connections and sessions

    Features:
    - Connection pooling
    - Automatic schema creation
    - SQLite → PostgreSQL abstraction
    - Foreign key enforcement for SQLite
    """

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager

        Args:
            database_url: Optional override for database URL
        """
        self.settings = get_settings()
        self.database_url = database_url or self.settings.database.url

        logger.info(f"Initializing database: {self._safe_url()}")

        try:
            # Create engine with appropriate settings
            if self.database_url.startswith('sqlite'):
                # SQLite-specific configuration
                self.engine = create_engine(
                    self.database_url,
                    connect_args={'check_same_thread': False},
                    poolclass=StaticPool,
                    echo=self.settings.database.echo
                )

                # Enable foreign key constraints for SQLite
                @event.listens_for(Engine, "connect")
                def set_sqlite_pragma(dbapi_conn, connection_record):
                    cursor = dbapi_conn.cursor()
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.close()

            else:
                # PostgreSQL-specific configuration
                self.engine = create_engine(
                    self.database_url,
                    pool_size=self.settings.database.pool_size,
                    max_overflow=self.settings.database.max_overflow,
                    pool_pre_ping=True,  # Verify connections before use
                    echo=self.settings.database.echo
                )

            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            # Create tables
            self._create_tables()

            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise DatabaseConnectionError(
                context={'database_url': self._safe_url()},
                original=e
            )

    def _safe_url(self) -> str:
        """Return database URL with password masked"""
        # Simple masking for SQLite
        if self.database_url.startswith('sqlite'):
            return self.database_url
        # Mask password in connection strings
        import re
        return re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', self.database_url)

    def _create_tables(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created/verified")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session with automatic cleanup

        Usage:
            with db_manager.get_session() as session:
                book = session.query(Book).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()

    def get_session_factory(self) -> sessionmaker:
        """Get the session factory for manual session management"""
        return self.SessionLocal

    def close(self):
        """Close all database connections"""
        self.engine.dispose()
        logger.info("Database connections closed")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get or create the global database manager instance

    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def reset_db_manager():
    """Reset the global database manager (useful for testing)"""
    global _db_manager
    if _db_manager is not None:
        _db_manager.close()
    _db_manager = None


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Convenience function to get a database session

    Usage:
        from reference_library.database import get_db_session

        with get_db_session() as session:
            books = session.query(Book).all()
    """
    db_manager = get_db_manager()
    with db_manager.get_session() as session:
        yield session
