# Comprehensive Implementation Plan
## Transforming the Standardized Chapter Generator into a Reference Library-Powered System

**Version:** 1.0
**Date:** 2025-11-04
**Objective:** Integrate essential features from Neurocore services while maintaining simplicity, modularity, and guaranteed functionality

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Phase 1: Reference Library Foundation](#phase-1-reference-library-foundation)
4. [Phase 2: Hybrid Search Integration](#phase-2-hybrid-search-integration)
5. [Phase 3: Parallel Research & PubMed Caching](#phase-3-parallel-research--pubmed-caching)
6. [Phase 4: Image Recommendations](#phase-4-image-recommendations)
7. [Phase 5: Section Regeneration](#phase-5-section-regeneration)
8. [Phase 6: Dual AI Provider System](#phase-6-dual-ai-provider-system)
9. [Phase 7: "Alive Chapter" Foundation](#phase-7-alive-chapter-foundation)
10. [Testing Strategy](#testing-strategy)
11. [Migration Guide](#migration-guide)
12. [Timeline & Milestones](#timeline--milestones)

---

## Executive Summary

### Current State
- Simple, configuration-driven chapter generator
- Single-use PDF extraction per generation
- No persistent knowledge base
- Linear research execution
- Single AI provider

### Target State
- Reference library with indexed medical literature
- Hybrid search (keyword + semantic + recency)
- Parallel research execution (40% speedup)
- PubMed caching (300x speedup on repeated queries)
- Smart image recommendations with diversity boosting
- Section-level regeneration (84% cost savings)
- Dual AI providers with automatic fallback
- Foundation for continuously evolving "alive" chapters

### Core Principles
1. **Modularity**: Each component is independent and pluggable
2. **Simplicity**: No over-engineering, clear interfaces
3. **Power**: Professional-grade features adapted from enterprise system
4. **Guaranteed Functionality**: Battle-tested patterns from Neurocore
5. **Progressive Enhancement**: System works at each phase, features add incrementally

---

## Critical Lessons from Neurocore (10 Weeks of Pain = Your Gain)

**⚠️ Context**: Neurocore spent 10+ weeks fixing these issues after the fact. Each lesson would have taken 1-2 days if done from the start. Our plan incorporates ALL lessons from Day 1.

### 🏗️ Lesson 1: Start Modular from Day 1
**Neurocore's Mistake**: 2,840 lines in a single file → 3 weeks to refactor
**Our Solution**:
- **Rule**: Never exceed 500 lines per file
- **Applied**: Each module has single responsibility
  - `reference_library/database.py` (~200 lines)
  - `search/hybrid_search.py` (~250 lines)
  - `research/research_orchestrator.py` (~300 lines)
- **Pattern**: Strategy + Template Method from the start
- **Benefit**: Easy to test, maintain, and extend

### 🔒 Lesson 2: Security from Day 1
**Neurocore's Mistake**: XSS vulnerabilities discovered in production
**Our Solution**:
```python
# Applied throughout all user-facing inputs
class InputValidator:
    @staticmethod
    def sanitize_topic(text: str) -> str:
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Escape special characters
        text = html.escape(text)
        # Validate path traversal
        if '../' in text or '..\\' in text:
            raise ValidationError("Invalid characters")
        return text
```
**Protected Against**: XSS, SQL injection, path traversal
**Files**: All config loaders, API inputs, file path handlers

### ⚡ Lesson 3: Avoid N+1 Queries (100x Performance)
**Neurocore's Mistake**: 301 queries for 100 records → 3000ms
**Our Solution**:
```python
# ✅ CORRECT: Eager loading with proper strategy
chapters = db.query(Chapter).options(
    joinedload(Chapter.pdf),           # One-to-one: JOIN
    selectinload(Chapter.images)       # One-to-many: SELECT IN
).all()
# Result: 3 queries, ~30ms (100x faster!)
```
**Applied**: All database queries in Phase 1 (Reference Library)
**Impact**: Sub-50ms query times even with large datasets

### 💾 Lesson 4: Caching with Invalidation (300x Speedup)
**Neurocore's Mistake**: Added caching late, forgot invalidation → stale data
**Our Solution** (Phase 3):
```python
# Cache with automatic invalidation
@cache_result(key_prefix="pubmed", ttl=86400)  # 24 hours
async def search_pubmed(query: str):
    # First call: 15-30 seconds
    # Cached call: <10ms (300x faster!)
    ...

# Invalidation on new data
def add_new_research(chapter_id: str):
    cache.invalidate(f"pubmed:{chapter_id}")
```
**Strategy**:
- Static data (PDFs): 1 hour TTL
- Dynamic data (PubMed): 24 hour TTL with invalidation
- Hot cache: Track access, extend TTL for frequently used data

### 🚨 Lesson 5: Structured Exceptions with Error Codes
**Neurocore's Mistake**: Generic exceptions → impossible to handle properly
**Our Solution**:
```python
# Custom exception hierarchy
class NeurosurgicalKBException(Exception):
    def __init__(self, message: str, error_code: str, context: dict = None):
        self.message = message
        self.error_code = error_code  # "DB_001", "API_002"
        self.context = context or {}

class DatabaseConnectionError(NeurosurgicalKBException):
    def __init__(self, context: dict = None):
        super().__init__(
            message="Database connection failed",
            error_code="DB_001",
            context=context
        )

# Usage
try:
    db.connect()
except DatabaseConnectionError as e:
    logger.error(f"Error {e.error_code}: {e.message}", extra=e.context)
    # Can handle specifically: retry, alert, fallback
```
**Benefit**: Machine-readable errors, better debugging, graceful degradation

### 🧪 Lesson 6: Testing Infrastructure First
**Neurocore's Mistake**: 19 collection errors, 0% coverage on critical paths
**Our Solution** (Week 1 Checklist):
```python
# pytest.ini - configured from Day 1
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*

# conftest.py - reusable fixtures
@pytest.fixture
def db_session():
    """Transaction-isolated database for tests"""
    session = Session()
    try:
        yield session
    finally:
        session.rollback()  # Cleanup
        session.close()

# test_reference_library.py - tests WITH features
def test_index_pdf(db_session):
    library = ReferenceLibraryManager(db_session)
    result = await library.add_pdf("test.pdf")
    assert result['status'] == 'success'
```
**Target Coverage**:
- Critical paths (research, generation): 80-90%
- Core services: 70-80%
- Overall: 60%+ before production

### ⏱️ Lesson 7: Timeouts from Day 1
**Neurocore's Mistake**: Tasks ran indefinitely, workers hung
**Our Solution**:
```python
# All async operations have timeouts
async def search_pubmed(query: str, timeout: int = 30):
    try:
        async with asyncio.timeout(timeout):
            results = await pubmed_api.search(query)
            return results
    except asyncio.TimeoutError:
        logger.warning(f"PubMed search timed out: {query}")
        return []  # Graceful degradation

# AI provider calls
response = await provider.generate_text(
    prompt,
    timeout=60  # 1 minute max
)
```
**Applied**: All external API calls, AI generation, database operations
**Benefit**: System never hangs, predictable behavior

### 📊 Lesson 8: Composite Indexes for Query Patterns
**Neurocore's Mistake**: Sequential scans on 10k+ rows → 100ms queries
**Our Solution** (Phase 1 Database Schema):
```sql
-- ✅ Composite index: filter + sort columns
CREATE INDEX idx_chapters_pdf_created
ON chapters(pdf_id, created_at DESC);

-- ✅ Covering index: includes frequently selected columns
CREATE INDEX idx_chapters_search
ON chapters(pdf_id, title, created_at)
INCLUDE (content);

-- Query pattern: Fast index scan
SELECT * FROM chapters
WHERE pdf_id = 'uuid'
ORDER BY created_at DESC
LIMIT 10;
-- Result: ~1ms (was 100ms)
```
**Rule**: Index columns in WHERE → ORDER BY order
**Impact**: 100x query speedup on filtered sorts

### ⚙️ Lesson 9: Type-Safe Configuration with Pydantic
**Neurocore's Mistake**: Runtime errors from misconfiguration
**Our Solution**:
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class ChapterConfig(BaseModel):
    """Type-safe configuration with validation"""
    topic: str = Field(..., min_length=3, max_length=200)
    reference_pdfs: list[str]
    max_images_per_section: int = Field(default=5, ge=1, le=20)
    use_reference_library: bool = True
    library_db_path: str = "neurosurgery_library.db"

    @validator('reference_pdfs')
    def validate_pdfs_exist(cls, v):
        for pdf in v:
            if not Path(pdf).exists():
                raise ValueError(f"PDF not found: {pdf}")
        return v

    class Config:
        validate_assignment = True  # Validate on attribute change
```
**Benefits**:
- Type checking at runtime
- Automatic type conversion
- Clear error messages
- Single source of truth

### 🔄 Lesson 10: Dependency Injection
**Neurocore's Mistake**: Services instantiated dependencies → hard to test
**Our Solution**:
```python
# ✅ GOOD: Constructor injection
class HybridSearch:
    def __init__(self, db_manager: DatabaseManager):
        self.keyword_search = KeywordSearch(db_manager)
        self.semantic_search = SemanticSearch(db_manager)

# Easy to test with mocks
def test_hybrid_search():
    mock_db = MockDatabase()
    search = HybridSearch(mock_db)
    results = await search.search("query")
    assert len(results) > 0

# ❌ BAD: Hard-coded instantiation
class BadSearch:
    def __init__(self):
        self.db = DatabaseManager()  # Can't mock!
```
**Pattern Applied**: All services receive dependencies via constructor
**Benefit**: Testable, maintainable, clear dependency graph

---

## Week 1 Implementation Checklist (Lessons Applied)

Before writing any feature code, set up:

**Architecture** (Lesson 1):
- [ ] Module structure with <500 lines per file
- [ ] Abstract base classes for shared behavior
- [ ] Dependency injection pattern throughout

**Security** (Lesson 2):
- [ ] `utils/security.py` with input sanitization
- [ ] Validation at config/API boundaries
- [ ] Path traversal protection

**Database** (Lessons 3, 8):
- [ ] Eager loading helpers documented
- [ ] Composite indexes for query patterns
- [ ] Connection pool sizing (Phase 1)

**Caching** (Lesson 4):
- [ ] Redis setup (Phase 3)
- [ ] Cache invalidation strategy
- [ ] TTL configuration per data type

**Error Handling** (Lesson 5):
- [ ] Custom exception hierarchy
- [ ] Error codes for all exceptions
- [ ] Context preservation in errors

**Testing** (Lesson 6):
- [ ] pytest.ini configured
- [ ] Transaction-isolated fixtures
- [ ] One smoke test passing
- [ ] Coverage target: 60%+

**Configuration** (Lesson 9):
- [ ] Pydantic models for all configs
- [ ] .env.example with documentation
- [ ] Validation on startup

**Timeouts** (Lesson 7):
- [ ] Default timeouts for all async ops
- [ ] Graceful degradation on timeout
- [ ] Timeout configuration in settings

---

## Cost of Ignoring These Lessons

**Neurocore's Retroactive Fixes**:
- Monolith refactoring: 3 weeks → 120+ tests
- Exception handling: 2 weeks → 115+ tests
- Security hardening: 2 weeks → 87 tests
- Performance optimization: 3 weeks
- **Total: 10+ weeks of rework**

**Our Approach**:
- Build right from Day 1: 1-2 days per lesson
- **Total: 2 weeks (8x faster, better quality)**

**ROI**: 8+ weeks saved, fewer bugs, better developer experience

---

## Architecture Overview

### System Transformation

```
BEFORE (Simple Pipeline):
User Config → Extract Images → Generate Outline → Synthesize → PDF

AFTER (Reference Library System):
                        ┌─────────────────────────────┐
                        │   Reference Library         │
                        │  (Indexed Medical PDFs)     │
                        │  - Vector Embeddings        │
                        │  - Full-Text Search         │
                        │  - Chapter-Level Index      │
                        └─────────────────────────────┘
                                    ↓
User Config → Hybrid Search → Parallel Research → Synthesize → PDF
                   ↓                    ↓
            (Keyword +         (Internal + External
             Semantic +          Concurrent)
             Recency)                  ↓
                              PubMed Cache (Redis)
                                    ↓
                         AI Provider Router
                         (Claude/GPT-4/Gemini)
                                    ↓
                         Section Regeneration
                         (Reuse research data)
```

### Module Structure

```
neurosurgical_chapter_system/
├── core/
│   ├── chapter_generator.py          # Main orchestrator (existing)
│   ├── config.py                      # Configuration management (existing)
│   └── quality_tracker.py             # Metrics tracking (existing)
│
├── reference_library/                 # NEW - Phase 1
│   ├── __init__.py
│   ├── library_manager.py            # Index management
│   ├── indexer.py                    # PDF processing & embedding
│   ├── database.py                   # SQLite storage
│   └── models.py                     # Data models
│
├── search/                            # NEW - Phase 2
│   ├── __init__.py
│   ├── hybrid_search.py              # Multi-algorithm search
│   ├── keyword_search.py             # Full-text search
│   ├── semantic_search.py            # Vector similarity
│   └── ranker.py                     # Scoring & ranking
│
├── research/                          # NEW - Phase 3
│   ├── __init__.py
│   ├── research_orchestrator.py      # Parallel execution
│   ├── internal_research.py          # Library search
│   ├── external_research.py          # PubMed/AI research
│   ├── pubmed_client.py              # PubMed API wrapper
│   └── cache_manager.py              # Redis/memory cache
│
├── images/                            # NEW - Phase 4
│   ├── __init__.py
│   ├── image_recommender.py          # Similarity-based selection
│   ├── diversity_booster.py          # Avoid duplicates
│   └── embedding_service.py          # Image embeddings
│
├── ai/                                # NEW - Phase 6
│   ├── __init__.py
│   ├── provider_router.py            # Multi-provider routing
│   ├── providers/
│   │   ├── claude_provider.py
│   │   ├── openai_provider.py
│   │   └── gemini_provider.py
│   └── circuit_breaker.py            # Failure handling
│
├── generation/                        # Enhanced - Phase 5
│   ├── __init__.py
│   ├── synthesizer.py                # Content generation (existing)
│   ├── section_regenerator.py        # NEW - Targeted updates
│   └── pdf_builder.py                # PDF creation (existing)
│
├── alive_chapters/                    # NEW - Phase 7
│   ├── __init__.py
│   ├── monitor.py                    # Update detection
│   ├── evolution_tracker.py          # Change management
│   └── interaction_logger.py         # User feedback
│
└── utils/
    ├── __init__.py
    ├── embeddings.py                 # Shared embedding logic
    ├── logger.py                     # Logging (existing)
    └── config_loader.py              # Config utilities (existing)
```

### Database Schema (SQLite for Simplicity)

```sql
-- Reference Library Tables

CREATE TABLE pdfs (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL UNIQUE,
    title TEXT,
    authors TEXT,
    publication_year INTEGER,
    total_pages INTEGER,
    file_size_bytes INTEGER,
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0
);

CREATE TABLE chapters (
    id TEXT PRIMARY KEY,
    pdf_id TEXT NOT NULL,
    chapter_number INTEGER,
    title TEXT NOT NULL,
    start_page INTEGER,
    end_page INTEGER,
    content TEXT,  -- Full text for keyword search
    embedding BLOB,  -- Vector embedding (numpy array serialized)
    embedding_model TEXT DEFAULT 'text-embedding-3-small',
    word_count INTEGER,
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pdf_id) REFERENCES pdfs(id) ON DELETE CASCADE
);

CREATE TABLE images (
    id TEXT PRIMARY KEY,
    pdf_id TEXT NOT NULL,
    chapter_id TEXT,
    page_number INTEGER,
    file_path TEXT NOT NULL,
    thumbnail_path TEXT,
    width INTEGER,
    height INTEGER,
    format TEXT,
    embedding BLOB,  -- Image embedding
    anatomical_structures TEXT,  -- JSON array
    image_type TEXT,  -- MRI, CT, Illustration, etc.
    quality_score REAL,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pdf_id) REFERENCES pdfs(id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE SET NULL
);

-- Research Cache Tables

CREATE TABLE pubmed_cache (
    cache_key TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    max_results INTEGER,
    recent_years INTEGER,
    results TEXT NOT NULL,  -- JSON serialized
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 1,
    ttl_hours INTEGER DEFAULT 24
);

-- Generated Chapters Tables

CREATE TABLE generated_chapters (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    config_path TEXT,
    output_pdf_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    version INTEGER DEFAULT 1,
    research_data TEXT,  -- JSON: stage 3-5 data for reuse
    metrics TEXT  -- JSON: quality metrics
);

CREATE TABLE chapter_sections (
    id TEXT PRIMARY KEY,
    chapter_id TEXT NOT NULL,
    section_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_ids TEXT,  -- JSON array of source references
    regenerated_at TIMESTAMP,
    regeneration_count INTEGER DEFAULT 0,
    FOREIGN KEY (chapter_id) REFERENCES generated_chapters(id) ON DELETE CASCADE
);

-- Indexes for Performance
CREATE INDEX idx_chapters_embedding ON chapters(pdf_id);
CREATE INDEX idx_images_pdf ON images(pdf_id);
CREATE INDEX idx_images_chapter ON images(chapter_id);
CREATE INDEX idx_pubmed_cache_query ON pubmed_cache(query);
CREATE INDEX idx_pubmed_cache_accessed ON pubmed_cache(accessed_at);
```

---

## Phase 0: Foundation Setup (Apply Lessons Before Writing Features)

**Duration:** 2-3 days
**Complexity:** Low
**Benefit:** Saves 8+ weeks of refactoring
**Status:** CRITICAL - Must complete before Phase 1

### 0.1 Objective

Set up the foundational infrastructure that applies all 10 Neurocore lessons. This prevents technical debt and ensures quality from Day 1.

### 0.2 Project Structure

```
neurosurgical_chapter_system/
├── .env.example                    # Environment variables documentation
├── .gitignore                      # Exclude .env, *.db, __pycache__
├── pytest.ini                      # Testing configuration
├── pyproject.toml                  # Dependencies and tool configuration
│
├── utils/                          # Shared utilities (Lessons 2, 5, 9)
│   ├── __init__.py
│   ├── security.py                 # Input sanitization (Lesson 2)
│   ├── exceptions.py               # Custom exception hierarchy (Lesson 5)
│   ├── logger.py                   # Structured logging
│   └── validators.py               # Pydantic validators (Lesson 9)
│
├── tests/                          # Testing infrastructure (Lesson 6)
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures
│   ├── test_utils.py               # Test utilities
│   └── fixtures/                   # Test data
│
└── docs/
    ├── ARCHITECTURE.md             # System design
    └── LESSONS_APPLIED.md          # Neurocore lessons checklist
```

### 0.3 Core Utilities Implementation

#### 0.3.1 Security & Validation (`utils/security.py`)

```python
"""
Security utilities (Lesson 2: Security from Day 1)
Prevents: XSS, SQL injection, path traversal
"""

import re
import html
from pathlib import Path
from typing import Optional

class InputValidator:
    """Validate and sanitize all user inputs"""

    @staticmethod
    def sanitize_text(text: str, max_length: int = 1000) -> str:
        """
        Sanitize text input

        Protections:
        - XSS: Strip HTML tags, escape special characters
        - Length: Prevent DoS via huge inputs
        """
        if not text:
            return ""

        # Truncate to max length
        text = text[:max_length]

        # Strip HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Escape HTML special characters
        text = html.escape(text)

        return text.strip()

    @staticmethod
    def validate_file_path(path: str, allowed_dirs: list[str]) -> Path:
        """
        Validate file path to prevent path traversal

        Raises:
            ValueError: If path is outside allowed directories
        """
        # Normalize path
        path_obj = Path(path).resolve()

        # Check for path traversal
        if '../' in str(path) or '..\\'  in str(path):
            raise ValueError(f"Path traversal detected: {path}")

        # Verify path is within allowed directories
        allowed = any(
            path_obj.is_relative_to(Path(allowed_dir).resolve())
            for allowed_dir in allowed_dirs
        )

        if not allowed:
            raise ValueError(f"Path not in allowed directories: {path}")

        return path_obj

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent injection

        Removes: special characters, path separators
        """
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')

        # Remove special characters except alphanumeric, dash, underscore, dot
        filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

        # Prevent hidden files
        if filename.startswith('.'):
            filename = '_' + filename

        return filename
```

#### 0.3.2 Exception Hierarchy (`utils/exceptions.py`)

```python
"""
Custom exception hierarchy (Lesson 5: Structured Exceptions)
All exceptions include error codes and context for debugging
"""

from typing import Optional, Dict, Any

class NeurosurgicalKBException(Exception):
    """Base exception for all system errors"""

    def __init__(
        self,
        message: str,
        error_code: str,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for logging/API responses"""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'context': self.context
        }

# Database Errors (DB_xxx)
class DatabaseError(NeurosurgicalKBException):
    """Base class for database errors"""
    pass

class DatabaseConnectionError(DatabaseError):
    def __init__(self, context: Optional[Dict] = None):
        super().__init__(
            message="Failed to connect to database",
            error_code="DB_001",
            context=context
        )

class RecordNotFoundError(DatabaseError):
    def __init__(self, resource: str, resource_id: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"{resource} not found: {resource_id}",
            error_code="DB_002",
            context={'resource': resource, 'id': resource_id, **(context or {})}
        )

# Validation Errors (VAL_xxx)
class ValidationError(NeurosurgicalKBException):
    """Base class for validation errors"""
    pass

class MissingFieldError(ValidationError):
    def __init__(self, field: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Required field missing: {field}",
            error_code="VAL_001",
            context={'field': field, **(context or {})}
        )

class InvalidFormatError(ValidationError):
    def __init__(self, field: str, expected: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Invalid format for {field}: expected {expected}",
            error_code="VAL_002",
            context={'field': field, 'expected': expected, **(context or {})}
        )

# External API Errors (API_xxx)
class ExternalAPIError(NeurosurgicalKBException):
    """Base class for external API errors"""
    pass

class OpenAIAPIError(ExternalAPIError):
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"OpenAI API error: {message}",
            error_code="API_001",
            context=context
        )

class PubMedAPIError(ExternalAPIError):
    def __init__(self, message: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"PubMed API error: {message}",
            error_code="API_002",
            context=context
        )

# File Processing Errors (FILE_xxx)
class FileProcessingError(NeurosurgicalKBException):
    """Base class for file processing errors"""
    pass

class PDFReadError(FileProcessingError):
    def __init__(self, file_path: str, context: Optional[Dict] = None):
        super().__init__(
            message=f"Failed to read PDF: {file_path}",
            error_code="FILE_001",
            context={'file_path': file_path, **(context or {})}
        )

# Timeout Errors (TIMEOUT_xxx)
class TimeoutError(NeurosurgicalKBException):
    """Operation exceeded timeout"""
    def __init__(self, operation: str, timeout_seconds: int, context: Optional[Dict] = None):
        super().__init__(
            message=f"Operation timed out: {operation} ({timeout_seconds}s)",
            error_code="TIMEOUT_001",
            context={'operation': operation, 'timeout': timeout_seconds, **(context or {})}
        )
```

#### 0.3.3 Structured Logging (`utils/logger.py`)

```python
"""
Structured logging with context (Lesson 5)
"""

import logging
import sys
from typing import Optional, Dict, Any
import json
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance

    Features:
    - Structured JSON logging
    - Request ID tracking
    - Error context preservation
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = StructuredFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger

class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra context if present
        if hasattr(record, 'context'):
            log_data['context'] = record.context

        return json.dumps(log_data)
```

#### 0.3.4 Testing Infrastructure (`tests/conftest.py`)

```python
"""
Shared test fixtures (Lesson 6: Testing First)
"""

import pytest
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def temp_db():
    """
    Temporary database for tests
    Each test gets a fresh database, automatically cleaned up
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_path = temp_file.name
    temp_file.close()

    engine = create_engine(f'sqlite:///{db_path}')
    # Create tables here

    yield engine

    # Cleanup
    engine.dispose()
    Path(db_path).unlink()

@pytest.fixture
def db_session(temp_db):
    """
    Transaction-isolated database session
    All changes rollback after test
    """
    Session = sessionmaker(bind=temp_db)
    session = Session()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def sample_pdf(tmp_path):
    """Sample PDF file for testing"""
    pdf_path = tmp_path / "test.pdf"
    # Create minimal valid PDF
    pdf_path.write_bytes(b'%PDF-1.4\n...')  # Minimal PDF
    return pdf_path

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API keys for testing"""
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'test_key_123')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key_456')
```

#### 0.3.5 Configuration (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Show extra test summary info
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=.
    --cov-report=term-missing
    --cov-report=html

# Markers for test organization
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (slower, may use external services)
    performance: Performance benchmarks
    slow: Tests that take >1 second

# Timeout for tests
timeout = 300
timeout_method = thread
```

### 0.4 Environment Configuration

#### `.env.example`

```bash
# API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here  # Optional

# Database
DATABASE_URL=sqlite:///neurosurgery_library.db

# Redis Cache (Optional, defaults to memory cache)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# PubMed API
PUBMED_EMAIL=your.email@domain.com  # Required by NCBI
PUBMED_API_KEY=  # Optional, for higher rate limits

# Timeouts (seconds)
DEFAULT_TIMEOUT=30
AI_GENERATION_TIMEOUT=60
RESEARCH_TIMEOUT=120

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json  # or 'text'

# Feature Flags
USE_REFERENCE_LIBRARY=true
ENABLE_CACHING=true
ENABLE_ALIVE_CHAPTERS=false
```

### 0.5 Dependencies (`pyproject.toml`)

```toml
[project]
name = "neurosurgical-chapter-system"
version = "0.1.0"
description = "AI-powered neurosurgical chapter generation"
requires-python = ">=3.10"

dependencies = [
    "anthropic>=0.18.0",
    "openai>=1.0.0",
    "google-generativeai>=0.3.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "sqlalchemy>=2.0.0",
    "redis>=5.0.0",
    "biopython>=1.81",  # For PubMed
    "pypdf2>=3.0.0",
    "pillow>=10.0.0",
    "numpy>=1.24.0",
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-timeout>=2.1.0"
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### 0.6 Deliverables

- [ ] `utils/security.py` - Input validation and sanitization
- [ ] `utils/exceptions.py` - Complete exception hierarchy (50+ classes)
- [ ] `utils/logger.py` - Structured logging
- [ ] `utils/validators.py` - Pydantic validators
- [ ] `tests/conftest.py` - Testing fixtures
- [ ] `pytest.ini` - Test configuration
- [ ] `.env.example` - Environment variables documentation
- [ ] `pyproject.toml` - Dependencies and configuration
- [ ] `docs/LESSONS_APPLIED.md` - Checklist verification

### 0.7 Verification Tests

```python
# tests/test_utils.py - Verify foundation works

def test_input_sanitization():
    """Test XSS protection"""
    malicious = "<script>alert('XSS')</script>Hello"
    clean = InputValidator.sanitize_text(malicious)
    assert '<' not in clean
    assert 'script' not in clean
    assert 'Hello' in clean

def test_path_traversal_protection():
    """Test path traversal prevention"""
    with pytest.raises(ValueError, match="Path traversal"):
        InputValidator.validate_file_path(
            "../../../etc/passwd",
            allowed_dirs=["/safe/dir"]
        )

def test_exception_serialization():
    """Test exceptions can be logged/returned as JSON"""
    error = DatabaseConnectionError(context={'host': 'localhost'})
    error_dict = error.to_dict()

    assert error_dict['error_code'] == 'DB_001'
    assert 'host' in error_dict['context']
    assert 'localhost' in str(error_dict)

def test_database_fixture(db_session):
    """Test database fixture provides clean session"""
    # Session should be empty
    assert db_session.query(Chapter).count() == 0

    # Changes don't persist between tests
    # (verified by rollback in fixture)
```

### 0.8 Success Criteria

✅ All 10 Neurocore lessons applied
✅ Security utilities prevent common vulnerabilities
✅ Exception hierarchy covers all error types
✅ Testing infrastructure configured and working
✅ One smoke test passing
✅ Dependencies installed
✅ Ready to start Phase 1

**Time Investment**: 2-3 days
**Time Saved**: 8+ weeks of refactoring

---

## Phase 1: Reference Library Foundation

**Duration:** 1-2 weeks
**Complexity:** Medium
**Benefit:** Foundation for all other features
**Status:** ESSENTIAL

### 1.1 Objective

Create a persistent, indexed library of neurosurgical reference materials that can be searched efficiently using both keyword and semantic methods.

### 1.2 Components

#### 1.2.1 Database Manager (`reference_library/database.py`)

```python
"""
Database management for reference library
Uses SQLite for simplicity, easy to upgrade to PostgreSQL later
"""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
import json
from contextlib import contextmanager

class DatabaseManager:
    """Manages SQLite database for reference library"""

    def __init__(self, db_path: str = "reference_library.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dicts
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialize_database(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            # Execute schema from above
            conn.executescript("""
                -- Copy SQL schema from above here
                CREATE TABLE IF NOT EXISTS pdfs (...);
                -- etc.
            """)

    def add_pdf(self, pdf_data: Dict[str, Any]) -> str:
        """Add PDF metadata to database"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO pdfs (id, file_path, title, authors, publication_year,
                                  total_pages, file_size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                pdf_data['id'], pdf_data['file_path'], pdf_data.get('title'),
                pdf_data.get('authors'), pdf_data.get('publication_year'),
                pdf_data.get('total_pages'), pdf_data.get('file_size_bytes')
            ))
            return pdf_data['id']

    def add_chapter(self, chapter_data: Dict[str, Any]) -> str:
        """Add chapter with embedding to database"""
        import numpy as np

        # Serialize embedding as bytes
        embedding_bytes = None
        if chapter_data.get('embedding') is not None:
            embedding_array = np.array(chapter_data['embedding'], dtype=np.float32)
            embedding_bytes = embedding_array.tobytes()

        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO chapters (id, pdf_id, chapter_number, title, start_page,
                                     end_page, content, embedding, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chapter_data['id'], chapter_data['pdf_id'],
                chapter_data.get('chapter_number'),
                chapter_data['title'], chapter_data.get('start_page'),
                chapter_data.get('end_page'), chapter_data.get('content'),
                embedding_bytes, chapter_data.get('word_count')
            ))
            return chapter_data['id']

    def get_all_chapters_with_embeddings(self):
        """Retrieve all chapters that have embeddings"""
        import numpy as np

        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT c.*, p.title as pdf_title, p.file_path as pdf_path
                FROM chapters c
                JOIN pdfs p ON c.pdf_id = p.id
                WHERE c.embedding IS NOT NULL
            """)

            chapters = []
            for row in cursor.fetchall():
                chapter_dict = dict(row)

                # Deserialize embedding
                if chapter_dict['embedding']:
                    embedding_bytes = chapter_dict['embedding']
                    embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)
                    chapter_dict['embedding'] = embedding_array.tolist()

                chapters.append(chapter_dict)

            return chapters
```

#### 1.2.2 PDF Indexer (`reference_library/indexer.py`)

```python
"""
PDF indexing pipeline: Extract chapters, generate embeddings, store in DB
"""

import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import PyPDF2
from anthropic import Anthropic
import asyncio
import time

from .database import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class PDFIndexer:
    """Indexes PDF documents into the reference library"""

    def __init__(self, db_manager: DatabaseManager, anthropic_api_key: str):
        self.db = db_manager
        self.client = Anthropic(api_key=anthropic_api_key)

    async def index_pdf(self, pdf_path: str, extract_chapters: bool = True) -> Dict[str, Any]:
        """
        Index a PDF into the reference library

        Args:
            pdf_path: Path to PDF file
            extract_chapters: If True, attempt to detect chapter boundaries

        Returns:
            Indexing results with statistics
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        logger.info(f"Indexing PDF: {pdf_path.name}")
        start_time = time.time()

        # Step 1: Generate PDF ID and extract metadata
        pdf_id = self._generate_pdf_id(pdf_path)
        metadata = self._extract_pdf_metadata(pdf_path)

        # Check if already indexed
        if self._is_already_indexed(pdf_id):
            logger.info(f"PDF already indexed: {pdf_path.name}")
            return {"status": "already_indexed", "pdf_id": pdf_id}

        # Step 2: Add PDF to database
        pdf_data = {
            'id': pdf_id,
            'file_path': str(pdf_path.absolute()),
            'title': metadata.get('title'),
            'authors': metadata.get('authors'),
            'publication_year': metadata.get('year'),
            'total_pages': metadata['page_count'],
            'file_size_bytes': pdf_path.stat().st_size
        }
        self.db.add_pdf(pdf_data)

        # Step 3: Extract chapters
        if extract_chapters:
            chapters = await self._extract_chapters(pdf_path, pdf_id)
        else:
            # Treat entire PDF as one chapter
            chapters = await self._extract_full_pdf_as_chapter(pdf_path, pdf_id)

        # Step 4: Generate embeddings for each chapter
        indexed_chapters = []
        for chapter in chapters:
            try:
                embedding = await self._generate_embedding(chapter['content'])
                chapter['embedding'] = embedding

                # Add to database
                chapter_id = self.db.add_chapter(chapter)
                indexed_chapters.append(chapter_id)

                logger.info(f"Indexed chapter: {chapter['title']}")

                # Rate limiting (1 request per second for OpenAI)
                await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Failed to index chapter '{chapter['title']}': {e}")
                continue

        duration = time.time() - start_time

        result = {
            'status': 'success',
            'pdf_id': pdf_id,
            'pdf_title': metadata.get('title'),
            'chapters_indexed': len(indexed_chapters),
            'duration_seconds': round(duration, 2)
        }

        logger.info(f"Indexing complete: {len(indexed_chapters)} chapters in {duration:.1f}s")
        return result

    def _generate_pdf_id(self, pdf_path: Path) -> str:
        """Generate unique ID for PDF based on file path and size"""
        identifier = f"{pdf_path.name}_{pdf_path.stat().st_size}"
        return hashlib.md5(identifier.encode()).hexdigest()

    def _extract_pdf_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract basic metadata from PDF"""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata or {}

            return {
                'title': metadata.get('/Title') or pdf_path.stem,
                'authors': metadata.get('/Author'),
                'year': None,  # Could extract from metadata if available
                'page_count': len(reader.pages)
            }

    def _is_already_indexed(self, pdf_id: str) -> bool:
        """Check if PDF already indexed"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT id FROM pdfs WHERE id = ?", (pdf_id,))
            return cursor.fetchone() is not None

    async def _extract_chapters(self, pdf_path: Path, pdf_id: str) -> List[Dict[str, Any]]:
        """
        Extract chapter boundaries using AI

        Strategy:
        1. Extract text from first 20 pages
        2. Use AI to detect chapter structure
        3. Extract full text for each chapter
        """
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            # Step 1: Extract TOC/early pages
            toc_text = ""
            for i in range(min(20, len(reader.pages))):
                toc_text += reader.pages[i].extract_text()

            # Step 2: Use AI to detect chapter boundaries
            chapter_boundaries = await self._detect_chapter_boundaries(toc_text, len(reader.pages))

            # Step 3: Extract full text for each chapter
            chapters = []
            for boundary in chapter_boundaries:
                chapter_text = ""
                for page_num in range(boundary['start_page'], boundary['end_page'] + 1):
                    if page_num < len(reader.pages):
                        chapter_text += reader.pages[page_num].extract_text()

                chapters.append({
                    'id': f"{pdf_id}_ch{boundary['chapter_number']}",
                    'pdf_id': pdf_id,
                    'chapter_number': boundary['chapter_number'],
                    'title': boundary['title'],
                    'start_page': boundary['start_page'],
                    'end_page': boundary['end_page'],
                    'content': chapter_text,
                    'word_count': len(chapter_text.split())
                })

            return chapters

    async def _detect_chapter_boundaries(self, toc_text: str, total_pages: int) -> List[Dict[str, Any]]:
        """Use AI to detect chapter structure from table of contents"""

        prompt = f"""Analyze this table of contents and extract chapter information.

Table of Contents:
{toc_text[:4000]}

Total pages in document: {total_pages}

Extract each chapter's:
1. Chapter number
2. Title
3. Start page number
4. Estimated end page (next chapter's start - 1, or total pages for last chapter)

Return as JSON array:
[
  {{"chapter_number": 1, "title": "...", "start_page": 1, "end_page": 25}},
  ...
]

If you cannot detect clear chapter boundaries, return:
[{{"chapter_number": 1, "title": "Full Document", "start_page": 0, "end_page": {total_pages - 1}}}]
"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )

            import json
            boundaries = json.loads(response.content[0].text)
            return boundaries

        except Exception as e:
            logger.warning(f"Failed to detect chapters, treating as single document: {e}")
            # Fallback: entire PDF as one chapter
            return [{
                'chapter_number': 1,
                'title': 'Full Document',
                'start_page': 0,
                'end_page': total_pages - 1
            }]

    async def _generate_embedding(self, text: str, max_length: int = 8000) -> List[float]:
        """
        Generate embedding for text using OpenAI's embedding model

        Note: Using OpenAI because it's more reliable for embeddings
              Claude doesn't provide embedding API
        """
        from openai import OpenAI
        import os

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length]

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    async def _extract_full_pdf_as_chapter(self, pdf_path: Path, pdf_id: str) -> List[Dict[str, Any]]:
        """Extract entire PDF as a single chapter"""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()

            return [{
                'id': f"{pdf_id}_ch1",
                'pdf_id': pdf_id,
                'chapter_number': 1,
                'title': pdf_path.stem,
                'start_page': 0,
                'end_page': len(reader.pages) - 1,
                'content': full_text,
                'word_count': len(full_text.split())
            }]
```

#### 1.2.3 Library Manager (`reference_library/library_manager.py`)

```python
"""
High-level interface for managing the reference library
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import asyncio

from .database import DatabaseManager
from .indexer import PDFIndexer
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ReferenceLibraryManager:
    """High-level manager for reference library operations"""

    def __init__(self, db_path: str = "reference_library.db", anthropic_api_key: str = None):
        self.db = DatabaseManager(db_path)
        self.indexer = PDFIndexer(self.db, anthropic_api_key)

    async def add_pdf(self, pdf_path: str, extract_chapters: bool = True) -> Dict[str, Any]:
        """Add a PDF to the library"""
        return await self.indexer.index_pdf(pdf_path, extract_chapters)

    async def add_directory(self, directory_path: str, recursive: bool = True) -> Dict[str, Any]:
        """
        Add all PDFs in a directory to the library

        Returns:
            Summary statistics
        """
        directory = Path(directory_path)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Find all PDFs
        if recursive:
            pdf_files = list(directory.rglob("*.pdf"))
        else:
            pdf_files = list(directory.glob("*.pdf"))

        logger.info(f"Found {len(pdf_files)} PDFs in {directory}")

        results = {
            'total_pdfs': len(pdf_files),
            'indexed': 0,
            'already_indexed': 0,
            'failed': 0,
            'chapters_added': 0
        }

        for pdf_file in pdf_files:
            try:
                result = await self.add_pdf(str(pdf_file))

                if result['status'] == 'success':
                    results['indexed'] += 1
                    results['chapters_added'] += result['chapters_indexed']
                elif result['status'] == 'already_indexed':
                    results['already_indexed'] += 1

            except Exception as e:
                logger.error(f"Failed to index {pdf_file.name}: {e}")
                results['failed'] += 1

        logger.info(f"Indexing complete: {results['indexed']} new, "
                   f"{results['already_indexed']} already indexed, {results['failed']} failed")

        return results

    def get_library_stats(self) -> Dict[str, Any]:
        """Get statistics about the library"""
        with self.db.get_connection() as conn:
            # Count PDFs
            cursor = conn.execute("SELECT COUNT(*) FROM pdfs")
            total_pdfs = cursor.fetchone()[0]

            # Count chapters
            cursor = conn.execute("SELECT COUNT(*) FROM chapters")
            total_chapters = cursor.fetchone()[0]

            # Count chapters with embeddings
            cursor = conn.execute("SELECT COUNT(*) FROM chapters WHERE embedding IS NOT NULL")
            chapters_with_embeddings = cursor.fetchone()[0]

            # Total words
            cursor = conn.execute("SELECT SUM(word_count) FROM chapters")
            total_words = cursor.fetchone()[0] or 0

            return {
                'total_pdfs': total_pdfs,
                'total_chapters': total_chapters,
                'chapters_with_embeddings': chapters_with_embeddings,
                'embedding_coverage': round(chapters_with_embeddings / total_chapters * 100, 1) if total_chapters > 0 else 0,
                'total_words': total_words,
                'status': 'ready' if chapters_with_embeddings > 0 else 'empty'
            }

    def list_pdfs(self) -> List[Dict[str, Any]]:
        """List all PDFs in the library"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT p.*, COUNT(c.id) as chapter_count
                FROM pdfs p
                LEFT JOIN chapters c ON p.id = c.pdf_id
                GROUP BY p.id
                ORDER BY p.indexed_at DESC
            """)

            return [dict(row) for row in cursor.fetchall()]

    def remove_pdf(self, pdf_id: str) -> bool:
        """Remove a PDF and all its chapters from the library"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("DELETE FROM pdfs WHERE id = ?", (pdf_id,))
            return cursor.rowcount > 0
```

### 1.3 Usage Example

```python
"""
Example: Building your reference library
"""

import asyncio
from reference_library.library_manager import ReferenceLibraryManager

async def main():
    # Initialize library
    library = ReferenceLibraryManager(
        db_path="neurosurgery_library.db",
        anthropic_api_key="your-api-key"
    )

    # Add your reference directory
    result = await library.add_directory(
        "/Users/ramihatoum/Desktop/Neurosurgery /reference library /Book chapters",
        recursive=True
    )

    print(f"Indexed {result['indexed']} PDFs")
    print(f"Added {result['chapters_added']} chapters")

    # Check library status
    stats = library.get_library_stats()
    print(f"\nLibrary Statistics:")
    print(f"  Total PDFs: {stats['total_pdfs']}")
    print(f"  Total Chapters: {stats['total_chapters']}")
    print(f"  Embedding Coverage: {stats['embedding_coverage']}%")
    print(f"  Total Words: {stats['total_words']:,}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 1.4 Testing Strategy

```python
"""
test_reference_library.py
"""

import pytest
import asyncio
from pathlib import Path
from reference_library.library_manager import ReferenceLibraryManager

@pytest.fixture
def library():
    """Create temporary test library"""
    import tempfile
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    lib = ReferenceLibraryManager(db_path=temp_db.name)
    yield lib
    # Cleanup
    Path(temp_db.name).unlink()

@pytest.mark.asyncio
async def test_add_single_pdf(library):
    """Test indexing a single PDF"""
    test_pdf = "tests/fixtures/sample_neurosurgery.pdf"
    result = await library.add_pdf(test_pdf)

    assert result['status'] == 'success'
    assert result['chapters_indexed'] > 0

@pytest.mark.asyncio
async def test_duplicate_pdf(library):
    """Test adding same PDF twice"""
    test_pdf = "tests/fixtures/sample_neurosurgery.pdf"

    # First add
    result1 = await library.add_pdf(test_pdf)
    assert result1['status'] == 'success'

    # Second add
    result2 = await library.add_pdf(test_pdf)
    assert result2['status'] == 'already_indexed'

def test_library_stats(library):
    """Test statistics retrieval"""
    stats = library.get_library_stats()

    assert 'total_pdfs' in stats
    assert 'total_chapters' in stats
    assert 'embedding_coverage' in stats
    assert stats['status'] in ['ready', 'empty']
```

### 1.5 CLI Integration

Add to `quickstart.sh`:

```bash
# New menu option: Manage Reference Library
manage_library() {
    echo "Reference Library Management"
    echo "1. Add PDF to library"
    echo "2. Add directory to library"
    echo "3. View library statistics"
    echo "4. List all PDFs"
    echo "5. Remove PDF"
    echo "6. Back to main menu"

    read -p "Choose option: " choice

    case $choice in
        1)
            read -p "Enter PDF path: " pdf_path
            python3 -c "
import asyncio
from reference_library.library_manager import ReferenceLibraryManager
async def main():
    lib = ReferenceLibraryManager()
    result = await lib.add_pdf('$pdf_path')
    print(f\"Status: {result['status']}\")
    if result['status'] == 'success':
        print(f\"Indexed {result['chapters_indexed']} chapters\")
asyncio.run(main())
            "
            ;;
        2)
            read -p "Enter directory path: " dir_path
            python3 -c "
import asyncio
from reference_library.library_manager import ReferenceLibraryManager
async def main():
    lib = ReferenceLibraryManager()
    result = await lib.add_directory('$dir_path', recursive=True)
    print(f\"Indexed: {result['indexed']} PDFs\")
    print(f\"Chapters: {result['chapters_added']}\")
asyncio.run(main())
            "
            ;;
        3)
            python3 -c "
from reference_library.library_manager import ReferenceLibraryManager
lib = ReferenceLibraryManager()
stats = lib.get_library_stats()
print(f\"PDFs: {stats['total_pdfs']}\")
print(f\"Chapters: {stats['total_chapters']}\")
print(f\"Coverage: {stats['embedding_coverage']}%\")
print(f\"Status: {stats['status']}\")
            "
            ;;
    esac
}
```

### 1.6 Configuration Updates

Add to `ChapterConfig`:

```python
@dataclass
class ChapterConfig:
    # ... existing fields ...

    # Reference library settings
    use_reference_library: bool = True
    library_db_path: str = "neurosurgery_library.db"
    max_reference_results: int = 10
    min_reference_similarity: float = 0.7
```

### 1.7 Deliverables

- [ ] `reference_library/database.py` - SQLite database management
- [ ] `reference_library/indexer.py` - PDF indexing pipeline
- [ ] `reference_library/library_manager.py` - High-level interface
- [ ] `reference_library/models.py` - Data models
- [ ] `tests/test_reference_library.py` - Comprehensive tests
- [ ] Updated `quickstart.sh` with library management
- [ ] Documentation: `REFERENCE_LIBRARY_GUIDE.md`

### 1.8 Success Criteria

✅ Can index a single PDF into library
✅ Can index entire directory of PDFs
✅ Detects and avoids duplicate PDFs
✅ Generates embeddings for all chapters
✅ Provides accurate library statistics
✅ All tests pass (100% coverage)

---

## Phase 2: Hybrid Search Integration

**Duration:** 3-5 days
**Complexity:** Medium
**Benefit:** Professional-grade content retrieval
**Status:** MUST HAVE
**Dependencies:** Phase 1 complete

### 2.1 Objective

Implement multi-algorithm search that combines keyword matching, semantic similarity, and recency scoring for optimal results.

### 2.2 Components

#### 2.2.1 Keyword Search (`search/keyword_search.py`)

```python
"""
Full-text keyword search using SQLite FTS5
"""

from typing import List, Dict, Any
from ..reference_library.database import DatabaseManager

class KeywordSearch:
    """Full-text search using SQLite FTS5"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._setup_fts()

    def _setup_fts(self):
        """Create FTS5 virtual table for full-text search"""
        with self.db.get_connection() as conn:
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS chapters_fts USING fts5(
                    chapter_id UNINDEXED,
                    title,
                    content,
                    tokenize='porter unicode61'
                )
            """)

            # Populate FTS table from chapters
            conn.execute("""
                INSERT OR REPLACE INTO chapters_fts (chapter_id, title, content)
                SELECT id, title, content FROM chapters WHERE content IS NOT NULL
            """)

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search chapters using full-text search

        Returns:
            List of results with BM25 scores
        """
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT
                    c.*,
                    p.title as pdf_title,
                    fts.rank as keyword_score
                FROM chapters_fts fts
                JOIN chapters c ON fts.chapter_id = c.id
                JOIN pdfs p ON c.pdf_id = p.id
                WHERE chapters_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, max_results))

            results = []
            for row in cursor.fetchall():
                result = dict(row)
                # Normalize BM25 score to 0-1 range
                # FTS5 rank is negative, higher (less negative) is better
                result['keyword_score'] = self._normalize_bm25_score(result['keyword_score'])
                results.append(result)

            return results

    def _normalize_bm25_score(self, raw_score: float) -> float:
        """
        Normalize BM25 score to 0-1 range
        FTS5 returns negative scores, with 0 being best match
        """
        # Convert to positive and normalize (approximate)
        # -20 is typical poor match, -1 is excellent match
        normalized = max(0, min(1, (-raw_score + 20) / 20))
        return normalized
```

#### 2.2.2 Semantic Search (`search/semantic_search.py`)

```python
"""
Vector similarity search using cosine distance
"""

import numpy as np
from typing import List, Dict, Any, Optional
from openai import OpenAI
import os

from ..reference_library.database import DatabaseManager

class SemanticSearch:
    """Semantic search using vector embeddings"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def search(
        self,
        query: str,
        max_results: int = 10,
        min_similarity: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search chapters using semantic similarity

        Args:
            query: Search query
            max_results: Maximum results to return
            min_similarity: Minimum cosine similarity (0-1)

        Returns:
            List of results with similarity scores
        """
        # Generate embedding for query
        query_embedding = await self._generate_embedding(query)

        # Get all chapters with embeddings
        chapters = self.db.get_all_chapters_with_embeddings()

        # Calculate cosine similarity for each
        results = []
        for chapter in chapters:
            chapter_embedding = np.array(chapter['embedding'])
            similarity = self._cosine_similarity(query_embedding, chapter_embedding)

            if similarity >= min_similarity:
                chapter['semantic_score'] = float(similarity)
                results.append(chapter)

        # Sort by similarity descending
        results.sort(key=lambda x: x['semantic_score'], reverse=True)

        return results[:max_results]

    async def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]  # Truncate if needed
        )
        return np.array(response.data[0].embedding)

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
```

#### 2.2.3 Hybrid Search Ranker (`search/ranker.py`)

```python
"""
Combines multiple search signals into unified ranking
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta

class HybridRanker:
    """Combines keyword, semantic, and recency scores"""

    def __init__(
        self,
        keyword_weight: float = 0.3,
        semantic_weight: float = 0.5,
        recency_weight: float = 0.2
    ):
        self.keyword_weight = keyword_weight
        self.semantic_weight = semantic_weight
        self.recency_weight = recency_weight

        # Ensure weights sum to 1.0
        total = keyword_weight + semantic_weight + recency_weight
        self.keyword_weight /= total
        self.semantic_weight /= total
        self.recency_weight /= total

    def merge_and_rank(
        self,
        keyword_results: List[Dict[str, Any]],
        semantic_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge keyword and semantic results with hybrid scoring

        Algorithm:
        1. Create unified set of unique chapters (by ID)
        2. Calculate hybrid score for each
        3. Sort by hybrid score descending
        """
        # Create unified results dict (chapter_id -> chapter data)
        unified = {}

        # Add keyword results
        for result in keyword_results:
            chapter_id = result['id']
            unified[chapter_id] = result
            unified[chapter_id]['keyword_score'] = result.get('keyword_score', 0)
            unified[chapter_id]['semantic_score'] = 0  # Will update if found in semantic

        # Add/update with semantic results
        for result in semantic_results:
            chapter_id = result['id']
            if chapter_id in unified:
                unified[chapter_id]['semantic_score'] = result.get('semantic_score', 0)
            else:
                unified[chapter_id] = result
                unified[chapter_id]['keyword_score'] = 0
                unified[chapter_id]['semantic_score'] = result.get('semantic_score', 0)

        # Calculate hybrid score for each
        ranked_results = []
        for chapter_id, chapter in unified.items():
            # Get scores (default to 0 if missing)
            keyword_score = chapter.get('keyword_score', 0)
            semantic_score = chapter.get('semantic_score', 0)

            # Calculate recency score
            recency_score = self._calculate_recency_score(chapter.get('indexed_at'))

            # Hybrid score = weighted sum
            hybrid_score = (
                keyword_score * self.keyword_weight +
                semantic_score * self.semantic_weight +
                recency_score * self.recency_weight
            )

            chapter['recency_score'] = recency_score
            chapter['hybrid_score'] = round(hybrid_score, 4)

            ranked_results.append(chapter)

        # Sort by hybrid score descending
        ranked_results.sort(key=lambda x: x['hybrid_score'], reverse=True)

        return ranked_results

    def _calculate_recency_score(self, indexed_at: Optional[str]) -> float:
        """
        Calculate recency score based on when content was indexed

        Scoring:
        - Last 30 days: 1.0
        - 30-90 days: 0.8
        - 90-180 days: 0.6
        - 180-365 days: 0.4
        - >365 days: 0.2
        """
        if not indexed_at:
            return 0.5  # Default if unknown

        try:
            indexed_date = datetime.fromisoformat(indexed_at)
            age_days = (datetime.now() - indexed_date).days

            if age_days <= 30:
                return 1.0
            elif age_days <= 90:
                return 0.8
            elif age_days <= 180:
                return 0.6
            elif age_days <= 365:
                return 0.4
            else:
                return 0.2

        except Exception:
            return 0.5
```

#### 2.2.4 Unified Search Interface (`search/hybrid_search.py`)

```python
"""
Unified search interface combining all search methods
"""

from typing import List, Dict, Any, Optional
import asyncio

from .keyword_search import KeywordSearch
from .semantic_search import SemanticSearch
from .ranker import HybridRanker
from ..reference_library.database import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class HybridSearch:
    """
    Professional-grade hybrid search combining multiple algorithms

    Features:
    - Full-text keyword search (BM25)
    - Semantic similarity search (vector embeddings)
    - Recency-based ranking
    - Configurable weight adjustments
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        keyword_weight: float = 0.3,
        semantic_weight: float = 0.5,
        recency_weight: float = 0.2
    ):
        self.keyword_search = KeywordSearch(db_manager)
        self.semantic_search = SemanticSearch(db_manager)
        self.ranker = HybridRanker(keyword_weight, semantic_weight, recency_weight)

    async def search(
        self,
        query: str,
        max_results: int = 10,
        min_similarity: float = 0.7,
        search_mode: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """
        Execute hybrid search

        Args:
            query: Search query
            max_results: Maximum results to return
            min_similarity: Minimum semantic similarity for semantic search
            search_mode: "hybrid", "keyword_only", or "semantic_only"

        Returns:
            Ranked search results with scores
        """
        logger.info(f"Hybrid search: '{query}' (mode: {search_mode})")

        if search_mode == "keyword_only":
            results = self.keyword_search.search(query, max_results * 3)
            return results[:max_results]

        elif search_mode == "semantic_only":
            results = await self.semantic_search.search(query, max_results, min_similarity)
            return results

        else:  # hybrid mode
            # Execute both searches in parallel
            keyword_task = asyncio.create_task(
                asyncio.to_thread(self.keyword_search.search, query, max_results * 3)
            )
            semantic_task = asyncio.create_task(
                self.semantic_search.search(query, max_results * 3, min_similarity)
            )

            keyword_results, semantic_results = await asyncio.gather(
                keyword_task, semantic_task
            )

            # Merge and rank
            hybrid_results = self.ranker.merge_and_rank(keyword_results, semantic_results)

            logger.info(f"Found {len(hybrid_results)} results "
                       f"(keyword: {len(keyword_results)}, semantic: {len(semantic_results)})")

            return hybrid_results[:max_results]

    def explain_ranking(self, result: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of why result was ranked highly
        """
        explanations = []

        if result.get('keyword_score', 0) > 0.7:
            explanations.append(f"Strong keyword match (score: {result['keyword_score']:.2f})")

        if result.get('semantic_score', 0) > 0.8:
            explanations.append(f"Highly relevant content (similarity: {result['semantic_score']:.2f})")

        if result.get('recency_score', 0) >= 0.8:
            explanations.append("Recently indexed")

        if result.get('hybrid_score', 0) > 0.8:
            explanations.append(f"Overall excellent match (hybrid: {result['hybrid_score']:.2f})")

        return " • ".join(explanations) if explanations else "Good match"
```

### 2.3 Integration with Chapter Generator

Update `neurosurgical_chapter_generator.py`:

```python
class StandardizedChapterGenerator:
    def __init__(self, config: ChapterConfig):
        self.config = config

        # Initialize reference library if enabled
        if config.use_reference_library:
            from reference_library.library_manager import ReferenceLibraryManager
            from search.hybrid_search import HybridSearch

            self.library = ReferenceLibraryManager(config.library_db_path)
            self.hybrid_search = HybridSearch(self.library.db)

    async def _gather_reference_materials(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search reference library for relevant materials

        This replaces manual PDF specification with automatic retrieval
        """
        if not self.config.use_reference_library:
            return []

        # Search library
        results = await self.hybrid_search.search(
            query=topic,
            max_results=self.config.max_reference_results,
            min_similarity=self.config.min_reference_similarity
        )

        # Log results
        logger.info(f"Found {len(results)} relevant references for '{topic}'")
        for i, result in enumerate(results[:5], 1):
            explanation = self.hybrid_search.explain_ranking(result)
            logger.info(f"  {i}. {result['title']} - {explanation}")

        return results
```

### 2.4 Testing Strategy

```python
"""
test_hybrid_search.py
"""

import pytest
import asyncio
from search.hybrid_search import HybridSearch
from reference_library.database import DatabaseManager

@pytest.fixture
async def search_system():
    """Set up test database with sample data"""
    db = DatabaseManager("test_search.db")

    # Add sample chapters
    # ... (add test data)

    search = HybridSearch(db)
    yield search

    # Cleanup
    import os
    os.remove("test_search.db")

@pytest.mark.asyncio
async def test_hybrid_search_combines_results(search_system):
    """Test that hybrid search merges keyword and semantic results"""
    results = await search_system.search(
        query="temporal craniotomy technique",
        max_results=10,
        search_mode="hybrid"
    )

    assert len(results) > 0

    # Check that results have all score components
    for result in results:
        assert 'keyword_score' in result
        assert 'semantic_score' in result
        assert 'recency_score' in result
        assert 'hybrid_score' in result

        # Hybrid score should be weighted combination
        expected = (
            result['keyword_score'] * 0.3 +
            result['semantic_score'] * 0.5 +
            result['recency_score'] * 0.2
        )
        assert abs(result['hybrid_score'] - expected) < 0.01

@pytest.mark.asyncio
async def test_semantic_search_finds_similar_meaning(search_system):
    """Test semantic search finds conceptually similar content"""
    results = await search_system.search(
        query="surgical approach to the temporal lobe",
        max_results=5,
        search_mode="semantic_only"
    )

    # Should find "temporal craniotomy" even if exact words differ
    titles = [r['title'].lower() for r in results]
    assert any('temporal' in title or 'craniotomy' in title for title in titles)

@pytest.mark.asyncio
async def test_keyword_search_exact_matches(search_system):
    """Test keyword search prioritizes exact term matches"""
    results = await search_system.search(
        query="middle fossa",
        max_results=5,
        search_mode="keyword_only"
    )

    # First result should contain exact phrase
    if results:
        assert 'middle fossa' in results[0]['content'].lower()
```

### 2.5 Configuration Updates

```yaml
# config_templates/temporal_craniotomy.yaml

# Reference Library Settings
use_reference_library: true
library_db_path: "neurosurgery_library.db"
max_reference_results: 10
min_reference_similarity: 0.7

# Search Algorithm Weights
search_weights:
  keyword: 0.3    # Full-text keyword matching
  semantic: 0.5   # Vector similarity
  recency: 0.2    # Prefer recent additions

# Search behavior
search_mode: "hybrid"  # Options: hybrid, keyword_only, semantic_only
```

### 2.6 Deliverables

- [ ] `search/keyword_search.py` - FTS5 implementation
- [ ] `search/semantic_search.py` - Vector similarity
- [ ] `search/ranker.py` - Hybrid scoring algorithm
- [ ] `search/hybrid_search.py` - Unified interface
- [ ] `tests/test_hybrid_search.py` - Comprehensive tests
- [ ] Updated chapter generator integration
- [ ] Documentation: `HYBRID_SEARCH_GUIDE.md`

### 2.7 Success Criteria

✅ Hybrid search combines keyword + semantic + recency
✅ Semantic search finds conceptually similar content
✅ Keyword search prioritizes exact matches
✅ Ranking explanation is human-readable
✅ Search completes in <2 seconds for typical queries
✅ All tests pass

---

## Phase 3: Parallel Research & PubMed Caching

**Duration:** 4-6 days
**Complexity:** Medium-High
**Benefit:** 40% speedup + 300x cache speedup
**Status:** MUST HAVE
**Dependencies:** Phase 2 complete

### 3.1 Objective

Execute internal and external research in parallel, with intelligent caching for PubMed queries to dramatically reduce redundant API calls.

### 3.2 Architecture

```
Research Orchestrator
       │
       ├─── Internal Research (Library)
       │    └─── Hybrid Search (from Phase 2)
       │
       └─── External Research (Parallel)
            ├─── PubMed Search
            │    └─── Cache Layer (Redis or Memory)
            │
            └─── AI Research (Perplexity/Gemini)
                 └─── Dual Provider (Phase 6)

All tasks execute concurrently via asyncio.gather()
```

### 3.3 Components

#### 3.3.1 Cache Manager (`research/cache_manager.py`)

```python
"""
Caching layer for external research queries
Supports both Redis (production) and memory (development)
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json
import hashlib

# Try Redis, fall back to memory
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from ..utils.logger import get_logger

logger = get_logger(__name__)

class CacheManager:
    """
    Intelligent caching for research queries

    Features:
    - Automatic TTL management
    - Adaptive caching (hot vs cold queries)
    - Memory fallback if Redis unavailable
    """

    def __init__(
        self,
        use_redis: bool = True,
        redis_host: str = "localhost",
        redis_port: int = 6379,
        default_ttl_hours: int = 24
    ):
        self.default_ttl_hours = default_ttl_hours
        self.use_redis = use_redis and REDIS_AVAILABLE

        if self.use_redis:
            try:
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    decode_responses=True
                )
                # Test connection
                self.redis_client.ping()
                logger.info("Connected to Redis cache")
            except Exception as e:
                logger.warning(f"Redis unavailable, using memory cache: {e}")
                self.use_redis = False
                self.memory_cache = {}
        else:
            logger.info("Using memory cache (Redis not available)")
            self.memory_cache = {}

    def _generate_cache_key(self, query: str, source: str, params: Dict[str, Any]) -> str:
        """Generate unique cache key for query"""
        # Include all relevant parameters in key
        key_data = {
            'query': query.lower().strip(),
            'source': source,
            'params': params
        }
        key_string = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return f"research_cache:{source}:{key_hash}"

    async def get(
        self,
        query: str,
        source: str,
        params: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve cached results if available

        Returns:
            Cached results or None if not found/expired
        """
        cache_key = self._generate_cache_key(query, source, params)

        if self.use_redis:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    # Update access tracking
                    self._track_access(cache_key)

                    result = json.loads(cached_data)
                    logger.info(f"Cache HIT: {source} query '{query}' "
                               f"(age: {result.get('cached_hours_ago', 0):.1f}h)")
                    return result['results']
            except Exception as e:
                logger.error(f"Redis get error: {e}")
                return None

        else:  # Memory cache
            if cache_key in self.memory_cache:
                cached_entry = self.memory_cache[cache_key]

                # Check if expired
                age_hours = (datetime.now() - cached_entry['cached_at']).total_seconds() / 3600
                if age_hours < cached_entry['ttl_hours']:
                    logger.info(f"Cache HIT (memory): {source} query '{query}' (age: {age_hours:.1f}h)")
                    return cached_entry['results']
                else:
                    # Expired, remove
                    del self.memory_cache[cache_key]

        logger.info(f"Cache MISS: {source} query '{query}'")
        return None

    async def set(
        self,
        query: str,
        source: str,
        params: Dict[str, Any],
        results: List[Dict[str, Any]],
        ttl_hours: Optional[int] = None
    ):
        """
        Cache results with TTL

        Args:
            ttl_hours: Time to live in hours (None = use default)
        """
        cache_key = self._generate_cache_key(query, source, params)
        ttl_hours = ttl_hours or self.default_ttl_hours

        cache_data = {
            'results': results,
            'cached_at': datetime.now().isoformat(),
            'query': query,
            'source': source,
            'ttl_hours': ttl_hours
        }

        if self.use_redis:
            try:
                # Store with expiration
                self.redis_client.setex(
                    cache_key,
                    timedelta(hours=ttl_hours),
                    json.dumps(cache_data)
                )

                # Initialize access tracking
                access_key = f"{cache_key}:access_count"
                self.redis_client.set(access_key, 0, ex=timedelta(hours=ttl_hours))

                logger.info(f"Cached {source} query '{query}' (TTL: {ttl_hours}h)")

            except Exception as e:
                logger.error(f"Redis set error: {e}")

        else:  # Memory cache
            self.memory_cache[cache_key] = cache_data
            logger.info(f"Cached (memory) {source} query '{query}' (TTL: {ttl_hours}h)")

    def _track_access(self, cache_key: str):
        """Track cache access for adaptive TTL"""
        if self.use_redis:
            try:
                access_key = f"{cache_key}:access_count"
                self.redis_client.incr(access_key)
            except Exception:
                pass

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if self.use_redis:
            try:
                # Count all cache keys
                all_keys = self.redis_client.keys("research_cache:*")
                cache_keys = [k for k in all_keys if not k.endswith(':access_count')]

                # Calculate hit rate (approximate)
                total_accesses = sum(
                    int(self.redis_client.get(f"{key}:access_count") or 0)
                    for key in cache_keys
                )

                return {
                    'backend': 'redis',
                    'total_entries': len(cache_keys),
                    'total_accesses': total_accesses,
                    'avg_accesses_per_entry': round(total_accesses / len(cache_keys), 1) if cache_keys else 0
                }
            except Exception as e:
                logger.error(f"Error getting cache stats: {e}")
                return {'backend': 'redis', 'error': str(e)}

        else:  # Memory cache
            return {
                'backend': 'memory',
                'total_entries': len(self.memory_cache)
            }

    def clear_cache(self, source: Optional[str] = None):
        """Clear cache (all or specific source)"""
        if self.use_redis:
            try:
                if source:
                    pattern = f"research_cache:{source}:*"
                else:
                    pattern = "research_cache:*"

                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
                    logger.info(f"Cleared {len(keys)} cache entries (source: {source or 'all'})")
            except Exception as e:
                logger.error(f"Error clearing cache: {e}")

        else:  # Memory cache
            if source:
                # Filter by source in key
                keys_to_remove = [k for k in self.memory_cache.keys() if f":{source}:" in k]
                for key in keys_to_remove:
                    del self.memory_cache[key]
            else:
                self.memory_cache.clear()

            logger.info(f"Cleared memory cache (source: {source or 'all'})")
```

#### 3.3.2 PubMed Client (`research/pubmed_client.py`)

```python
"""
PubMed API client with error handling and rate limiting
"""

from typing import List, Dict, Any, Optional
from Bio import Entrez
import asyncio
from datetime import datetime

from ..utils.logger import get_logger

logger = get_logger(__name__)

class PubMedClient:
    """
    PubMed/NCBI API client

    Features:
    - Rate limiting (3 requests/second for free tier)
    - Error handling and retries
    - Result formatting
    """

    def __init__(self, email: str, api_key: Optional[str] = None):
        """
        Initialize PubMed client

        Args:
            email: Required by NCBI
            api_key: Optional API key for higher rate limits
        """
        Entrez.email = email
        if api_key:
            Entrez.api_key = api_key

        self.rate_limit_delay = 0.34 if api_key else 0.34  # ~3 requests/second

    async def search(
        self,
        query: str,
        max_results: int = 10,
        recent_years: Optional[int] = None,
        sort_by: str = "relevance"
    ) -> List[Dict[str, Any]]:
        """
        Search PubMed for articles

        Args:
            query: Search query
            max_results: Maximum articles to return
            recent_years: Limit to articles from last N years
            sort_by: Sort order (relevance, pub_date)

        Returns:
            List of formatted article data
        """
        logger.info(f"Searching PubMed: '{query}' (max: {max_results})")

        # Build search query with date filter
        search_query = query
        if recent_years:
            current_year = datetime.now().year
            start_year = current_year - recent_years
            search_query = f"{query} AND {start_year}:{current_year}[pdat]"

        try:
            # Step 1: Search for PMIDs
            await asyncio.sleep(self.rate_limit_delay)

            search_handle = Entrez.esearch(
                db="pubmed",
                term=search_query,
                retmax=max_results,
                sort=sort_by
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()

            pmids = search_results['IdList']

            if not pmids:
                logger.warning(f"No PubMed results for: {query}")
                return []

            logger.info(f"Found {len(pmids)} PubMed articles")

            # Step 2: Fetch article details
            await asyncio.sleep(self.rate_limit_delay)

            fetch_handle = Entrez.efetch(
                db="pubmed",
                id=pmids,
                retmode="xml"
            )
            articles = Entrez.read(fetch_handle)
            fetch_handle.close()

            # Step 3: Format results
            formatted_results = []
            for article in articles['PubmedArticle']:
                try:
                    formatted = self._format_article(article)
                    formatted_results.append(formatted)
                except Exception as e:
                    logger.warning(f"Error formatting article: {e}")
                    continue

            return formatted_results

        except Exception as e:
            logger.error(f"PubMed search error: {e}")
            return []

    def _format_article(self, article: Dict) -> Dict[str, Any]:
        """Format PubMed article data"""
        medline = article['MedlineCitation']
        pubmed = article.get('PubmedData', {})

        # Extract article data
        article_data = medline['Article']

        # Title
        title = article_data.get('ArticleTitle', 'No title')

        # Authors
        authors = []
        if 'AuthorList' in article_data:
            for author in article_data['AuthorList']:
                if 'LastName' in author:
                    name = f"{author.get('ForeName', '')} {author['LastName']}".strip()
                    authors.append(name)

        # Abstract
        abstract = ""
        if 'Abstract' in article_data:
            abstract_texts = article_data['Abstract'].get('AbstractText', [])
            if isinstance(abstract_texts, list):
                abstract = " ".join(str(text) for text in abstract_texts)
            else:
                abstract = str(abstract_texts)

        # Journal
        journal = article_data.get('Journal', {}).get('Title', 'Unknown journal')

        # Publication date
        pub_date = None
        if 'PubDate' in article_data.get('Journal', {}).get('JournalIssue', {}):
            date_parts = article_data['Journal']['JournalIssue']['PubDate']
            year = date_parts.get('Year')
            month = date_parts.get('Month', '01')
            day = date_parts.get('Day', '01')
            if year:
                pub_date = f"{year}-{month}-{day}"

        # PMID
        pmid = medline.get('PMID', '')

        # DOI
        doi = None
        if 'ArticleIdList' in pubmed:
            for article_id in pubmed['ArticleIdList']:
                if article_id.attributes.get('IdType') == 'doi':
                    doi = str(article_id)
                    break

        return {
            'pmid': str(pmid),
            'title': title,
            'authors': authors,
            'journal': journal,
            'publication_date': pub_date,
            'abstract': abstract,
            'doi': doi,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
            'source': 'pubmed',
            'retrieved_at': datetime.now().isoformat()
        }
```

#### 3.3.3 Research Orchestrator (`research/research_orchestrator.py`)

```python
"""
Orchestrates parallel internal and external research
"""

from typing import List, Dict, Any, Optional
import asyncio
import time

from .internal_research import InternalResearch
from .external_research import ExternalResearch
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ResearchOrchestrator:
    """
    Coordinates parallel research from multiple sources

    Features:
    - Concurrent internal + external research
    - Configurable research strategies
    - Result merging and deduplication
    """

    def __init__(
        self,
        internal_research: InternalResearch,
        external_research: ExternalResearch
    ):
        self.internal = internal_research
        self.external = external_research

    async def research_topic(
        self,
        topic: str,
        include_internal: bool = True,
        include_external: bool = True,
        internal_max_results: int = 10,
        external_pubmed_max: int = 5,
        external_ai_enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Execute comprehensive research on topic

        Returns:
            {
                'internal_sources': [...],
                'external_pubmed': [...],
                'external_ai': [...],
                'total_sources': N,
                'duration_seconds': X.X
            }
        """
        logger.info(f"Researching topic: '{topic}'")
        start_time = time.time()

        # Create tasks for parallel execution
        tasks = []
        task_names = []

        if include_internal:
            tasks.append(self.internal.search(topic, internal_max_results))
            task_names.append('internal')

        if include_external:
            tasks.append(self.external.search_pubmed(topic, external_pubmed_max))
            task_names.append('pubmed')

            if external_ai_enabled:
                tasks.append(self.external.search_ai(topic))
                task_names.append('ai')

        # Execute all research tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        research_data = {
            'internal_sources': [],
            'external_pubmed': [],
            'external_ai': [],
            'errors': []
        }

        for task_name, result in zip(task_names, results):
            if isinstance(result, Exception):
                logger.error(f"{task_name} research failed: {result}")
                research_data['errors'].append({
                    'source': task_name,
                    'error': str(result)
                })
            else:
                if task_name == 'internal':
                    research_data['internal_sources'] = result
                elif task_name == 'pubmed':
                    research_data['external_pubmed'] = result
                elif task_name == 'ai':
                    research_data['external_ai'] = result

        # Calculate totals
        research_data['total_sources'] = (
            len(research_data['internal_sources']) +
            len(research_data['external_pubmed']) +
            len(research_data['external_ai'])
        )

        duration = time.time() - start_time
        research_data['duration_seconds'] = round(duration, 2)

        logger.info(f"Research complete: {research_data['total_sources']} sources in {duration:.1f}s")
        logger.info(f"  Internal: {len(research_data['internal_sources'])}")
        logger.info(f"  PubMed: {len(research_data['external_pubmed'])}")
        logger.info(f"  AI: {len(research_data['external_ai'])}")

        return research_data

    async def research_multiple_queries(
        self,
        queries: List[str],
        **kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """
        Execute research for multiple queries in parallel

        Returns:
            {query1: research_data1, query2: research_data2, ...}
        """
        logger.info(f"Researching {len(queries)} queries in parallel")

        # Create research tasks for all queries
        tasks = [
            self.research_topic(query, **kwargs)
            for query in queries
        ]

        # Execute all in parallel
        results = await asyncio.gather(*tasks)

        # Return as dict keyed by query
        return {
            query: result
            for query, result in zip(queries, results)
        }
```

#### 3.3.4 Internal Research (`research/internal_research.py`)

```python
"""
Internal research using reference library
"""

from typing import List, Dict, Any
from ..search.hybrid_search import HybridSearch

class InternalResearch:
    """Search internal reference library"""

    def __init__(self, hybrid_search: HybridSearch):
        self.search = hybrid_search

    async def search(
        self,
        query: str,
        max_results: int = 10,
        min_similarity: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search internal library

        Returns list of relevant chapters
        """
        results = await self.search.search(
            query=query,
            max_results=max_results,
            min_similarity=min_similarity,
            search_mode="hybrid"
        )

        # Format for consistent interface
        formatted = []
        for result in results:
            formatted.append({
                'id': result['id'],
                'title': result['title'],
                'source': 'internal_library',
                'pdf_title': result.get('pdf_title'),
                'content_preview': result.get('content', '')[:500],
                'chapter_number': result.get('chapter_number'),
                'page_range': f"{result.get('start_page')}-{result.get('end_page')}",
                'relevance_score': result.get('hybrid_score'),
                'explanation': self.search.explain_ranking(result)
            })

        return formatted
```

#### 3.3.5 External Research (`research/external_research.py`)

```python
"""
External research (PubMed + AI)
"""

from typing import List, Dict, Any, Optional
from .pubmed_client import PubMedClient
from .cache_manager import CacheManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ExternalResearch:
    """External research sources"""

    def __init__(
        self,
        pubmed_email: str,
        pubmed_api_key: Optional[str] = None,
        cache_manager: Optional[CacheManager] = None
    ):
        self.pubmed = PubMedClient(pubmed_email, pubmed_api_key)
        self.cache = cache_manager

    async def search_pubmed(
        self,
        query: str,
        max_results: int = 10,
        recent_years: int = 10,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search PubMed with caching

        Performance:
        - First call: 15-30 seconds
        - Cached call: <10ms (300x speedup!)
        """
        # Check cache first
        if use_cache and self.cache:
            cached = await self.cache.get(
                query=query,
                source='pubmed',
                params={'max_results': max_results, 'recent_years': recent_years}
            )
            if cached:
                return cached

        # Cache miss, fetch from PubMed
        logger.info(f"Fetching from PubMed (no cache): {query}")
        results = await self.pubmed.search(
            query=query,
            max_results=max_results,
            recent_years=recent_years
        )

        # Cache results
        if self.cache:
            await self.cache.set(
                query=query,
                source='pubmed',
                params={'max_results': max_results, 'recent_years': recent_years},
                results=results,
                ttl_hours=24  # PubMed results stable for 24h
            )

        return results

    async def search_ai(self, query: str) -> List[Dict[str, Any]]:
        """
        AI-powered research (Perplexity/Gemini)

        Implementation in Phase 6 (Dual AI Providers)
        """
        # Placeholder - will be implemented in Phase 6
        logger.info(f"AI research: {query} (not yet implemented)")
        return []
```

### 3.4 Integration Example

```python
"""
Integration with chapter generator
"""

# In neurosurgical_chapter_generator.py

async def _execute_research(self, topic: str) -> Dict[str, Any]:
    """
    Execute comprehensive research using parallel execution

    40% faster than sequential execution!
    """
    from research.research_orchestrator import ResearchOrchestrator
    from research.internal_research import InternalResearch
    from research.external_research import ExternalResearch
    from research.cache_manager import CacheManager

    # Initialize components
    cache = CacheManager(use_redis=self.config.use_redis_cache)

    internal = InternalResearch(self.hybrid_search)

    external = ExternalResearch(
        pubmed_email=self.config.pubmed_email,
        pubmed_api_key=self.config.pubmed_api_key,
        cache_manager=cache
    )

    orchestrator = ResearchOrchestrator(internal, external)

    # Execute parallel research
    research_data = await orchestrator.research_topic(
        topic=topic,
        include_internal=True,
        include_external=True,
        internal_max_results=10,
        external_pubmed_max=5,
        external_ai_enabled=False  # Phase 6
    )

    return research_data
```

### 3.5 Performance Comparison

```
BEFORE (Sequential):
┌─────────────┐
│ Internal    │ 2-3 seconds
├─────────────┤
│ PubMed      │ 15-30 seconds (first call)
├─────────────┤
│ AI Research │ 10-15 seconds
└─────────────┘
TOTAL: 27-48 seconds

AFTER (Parallel + Cache):
┌─────────────┬─────────────┬─────────────┐
│ Internal    │ PubMed      │ AI Research │
│ 2-3 sec     │ <10ms cache │ 10-15 sec   │
└─────────────┴─────────────┴─────────────┘
TOTAL: 12-18 seconds (first call)
TOTAL: 2-3 seconds (cached PubMed)

SPEEDUP:
- First call: 40% faster
- Cached call: 85% faster
```

### 3.6 Configuration

```yaml
# Research settings
research:
  enable_parallel: true

  # Internal research (reference library)
  internal:
    enabled: true
    max_results: 10
    min_similarity: 0.7

  # External research
  external:
    pubmed:
      enabled: true
      max_results: 5
      recent_years: 10
      email: "your.email@domain.com"  # Required by NCBI
      api_key: null  # Optional, for higher rate limits

    ai_research:
      enabled: false  # Implemented in Phase 6

  # Caching
  cache:
    enabled: true
    backend: "redis"  # Options: redis, memory
    redis_host: "localhost"
    redis_port: 6379
    default_ttl_hours: 24
```

### 3.7 Deliverables

- [ ] `research/cache_manager.py` - Redis/memory caching
- [ ] `research/pubmed_client.py` - PubMed API wrapper
- [ ] `research/research_orchestrator.py` - Parallel execution
- [ ] `research/internal_research.py` - Library search
- [ ] `research/external_research.py` - External sources
- [ ] `tests/test_research.py` - Comprehensive tests
- [ ] Documentation: `RESEARCH_SYSTEM_GUIDE.md`

### 3.8 Success Criteria

✅ Parallel execution 40% faster than sequential
✅ PubMed cache provides 300x speedup on cached queries
✅ Redis and memory cache both work correctly
✅ Graceful degradation if Redis unavailable
✅ All research sources complete successfully
✅ Error in one source doesn't block others
✅ All tests pass

---

## Phase 4: Image Recommendations

**Duration:** 3-4 days
**Complexity:** Medium
**Benefit:** Smart image selection, avoid duplicates
**Status:** SHOULD HAVE
**Dependencies:** Phase 1 complete

### 4.1 Objective

Automatically select the most relevant images for each chapter section using vector similarity, with diversity boosting to avoid near-duplicate images.

### 4.2 Architecture

```
Image Recommendation Flow:
1. Extract images from reference PDFs (existing)
2. Generate embeddings for images (new)
3. Associate images with chapters (new)
4. Query-based similarity search (new)
5. Diversity boosting (new)
6. Return diverse, relevant images
```

### 4.3 Components

#### 4.3.1 Image Embedding Service (`images/embedding_service.py`)

```python
"""
Generate embeddings for images using CLIP or similar
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np
from PIL import Image as PILImage
from openai import OpenAI
import os
import base64
import io

from ..utils.logger import get_logger

logger = get_logger(__name__)

class ImageEmbeddingService:
    """
    Generate embeddings for images

    Uses OpenAI's CLIP-based image understanding
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def generate_image_embedding(
        self,
        image_path: str,
        text_description: Optional[str] = None
    ) -> List[float]:
        """
        Generate embedding for image

        Args:
            image_path: Path to image file
            text_description: Optional text to combine with image

        Returns:
            Image embedding vector
        """
        try:
            # Load and prepare image
            img = PILImage.open(image_path)

            # Resize if too large (max 2048px)
            max_size = 2048
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, PILImage.Resampling.LANCZOS)

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Generate embedding using vision model
            # Note: OpenAI doesn't directly provide image embeddings via API
            # We'll use GPT-4V to describe the image, then embed the description

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this medical image in detail for embedding purposes. Focus on: anatomical structures, surgical approach, imaging modality, and clinical context. Keep it concise (2-3 sentences)."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=200
            )

            description = response.choices[0].message.content

            # Combine with provided text if available
            if text_description:
                description = f"{text_description}. {description}"

            # Generate text embedding
            embedding_response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=description
            )

            return embedding_response.data[0].embedding

        except Exception as e:
            logger.error(f"Failed to generate image embedding for {image_path}: {e}")
            raise

    async def generate_batch_embeddings(
        self,
        image_paths: List[str],
        batch_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for multiple images

        Returns:
            List of {image_path, embedding, description}
        """
        import asyncio

        results = []

        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i+batch_size]

            # Process batch sequentially to respect rate limits
            for image_path in batch:
                try:
                    embedding = await self.generate_image_embedding(image_path)
                    results.append({
                        'image_path': image_path,
                        'embedding': embedding,
                        'success': True
                    })

                    # Rate limiting
                    await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"Failed to process {image_path}: {e}")
                    results.append({
                        'image_path': image_path,
                        'embedding': None,
                        'success': False,
                        'error': str(e)
                    })

            logger.info(f"Processed batch {i//batch_size + 1}/{(len(image_paths)-1)//batch_size + 1}")

        return results
```

#### 4.3.2 Diversity Booster (`images/diversity_booster.py`)

```python
"""
Ensure diverse image selection to avoid near-duplicates
"""

import numpy as np
from typing import List, Dict, Any, Tuple

from ..utils.logger import get_logger

logger = get_logger(__name__)

class DiversityBooster:
    """
    Apply diversity boosting to image recommendations

    Algorithm: Greedy selection with similarity threshold
    1. Start with most relevant image
    2. Only add images sufficiently different from already selected
    3. Continue until desired count reached
    """

    def __init__(self, diversity_threshold: float = 0.95):
        """
        Args:
            diversity_threshold: Minimum similarity to consider duplicates
                                (0.95 = 95% similar = too similar)
        """
        self.diversity_threshold = diversity_threshold

    def apply_diversity_boosting(
        self,
        candidates: List[Dict[str, Any]],
        max_results: int,
        embedding_key: str = 'embedding',
        score_key: str = 'similarity_score'
    ) -> List[Dict[str, Any]]:
        """
        Apply diversity boosting to candidate images

        Args:
            candidates: List of image candidates with embeddings and scores
            max_results: Maximum images to return
            embedding_key: Key for embedding in candidate dict
            score_key: Key for relevance score in candidate dict

        Returns:
            Diverse subset of candidates
        """
        if not candidates:
            return []

        # Sort by relevance score descending
        candidates = sorted(
            candidates,
            key=lambda x: x.get(score_key, 0),
            reverse=True
        )

        selected = []
        selected_embeddings = []

        for candidate in candidates:
            if len(selected) >= max_results:
                break

            embedding = candidate.get(embedding_key)
            if embedding is None:
                continue

            embedding_array = np.array(embedding)

            # First image always selected
            if len(selected) == 0:
                selected.append(candidate)
                selected_embeddings.append(embedding_array)
                continue

            # Check diversity against already selected
            is_diverse = self._is_diverse_enough(
                embedding_array,
                selected_embeddings
            )

            if is_diverse:
                selected.append(candidate)
                selected_embeddings.append(embedding_array)
                logger.debug(f"Selected diverse image: {candidate.get('image_path', 'unknown')}")
            else:
                logger.debug(f"Skipped similar image: {candidate.get('image_path', 'unknown')}")

        logger.info(f"Diversity boosting: {len(candidates)} candidates → {len(selected)} diverse images")

        return selected

    def _is_diverse_enough(
        self,
        candidate_embedding: np.ndarray,
        selected_embeddings: List[np.ndarray]
    ) -> bool:
        """
        Check if candidate is sufficiently different from selected images
        """
        for selected_emb in selected_embeddings:
            similarity = self._cosine_similarity(candidate_embedding, selected_emb)

            if similarity > self.diversity_threshold:
                return False  # Too similar

        return True  # Sufficiently diverse

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
```

#### 4.3.3 Image Recommender (`images/image_recommender.py`)

```python
"""
Main image recommendation service
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np

from .embedding_service import ImageEmbeddingService
from .diversity_booster import DiversityBooster
from ..reference_library.database import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ImageRecommender:
    """
    Recommend relevant images for chapter sections

    Features:
    - Query-based image search
    - Relevance scoring via embedding similarity
    - Diversity boosting to avoid duplicates
    - Chapter/PDF filtering
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        diversity_threshold: float = 0.95
    ):
        self.db = db_manager
        self.embedding_service = ImageEmbeddingService()
        self.diversity_booster = DiversityBooster(diversity_threshold)

    async def recommend_for_section(
        self,
        section_title: str,
        section_content: str,
        max_images: int = 5,
        filter_pdf_ids: Optional[List[str]] = None,
        min_quality: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Recommend images for a chapter section

        Args:
            section_title: Section title
            section_content: Section text content
            max_images: Maximum images to return
            filter_pdf_ids: Optional list of PDF IDs to search within
            min_quality: Minimum quality score (if available)

        Returns:
            List of recommended images with metadata
        """
        logger.info(f"Finding images for section: {section_title}")

        # Generate query embedding from section content
        query_text = f"{section_title}. {section_content[:500]}"
        query_embedding = await self._generate_query_embedding(query_text)

        # Get candidate images from database
        candidates = self._get_image_candidates(
            filter_pdf_ids=filter_pdf_ids,
            min_quality=min_quality
        )

        if not candidates:
            logger.warning("No candidate images found")
            return []

        # Calculate similarity scores
        scored_candidates = self._score_candidates(
            candidates,
            query_embedding
        )

        # Apply diversity boosting
        diverse_images = self.diversity_booster.apply_diversity_boosting(
            scored_candidates,
            max_results=max_images * 3  # Get extras for boosting
        )

        # Return top results
        results = diverse_images[:max_images]

        # Format results
        formatted_results = []
        for img in results:
            formatted_results.append({
                'image_id': img['id'],
                'file_path': img['file_path'],
                'thumbnail_path': img.get('thumbnail_path'),
                'page_number': img.get('page_number'),
                'pdf_title': img.get('pdf_title'),
                'width': img.get('width'),
                'height': img.get('height'),
                'quality_score': img.get('quality_score'),
                'similarity_score': img['similarity_score'],
                'explanation': self._generate_explanation(img)
            })

        logger.info(f"Recommended {len(formatted_results)} images for '{section_title}'")

        return formatted_results

    async def _generate_query_embedding(self, query_text: str) -> np.ndarray:
        """Generate embedding for query text"""
        from openai import OpenAI
        import os

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=query_text[:8000]
        )

        return np.array(response.data[0].embedding)

    def _get_image_candidates(
        self,
        filter_pdf_ids: Optional[List[str]] = None,
        min_quality: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Get candidate images from database"""
        with self.db.get_connection() as conn:
            query = """
                SELECT
                    i.*,
                    p.title as pdf_title
                FROM images i
                JOIN pdfs p ON i.pdf_id = p.id
                WHERE i.embedding IS NOT NULL
            """

            params = []

            if filter_pdf_ids:
                placeholders = ','.join('?' * len(filter_pdf_ids))
                query += f" AND i.pdf_id IN ({placeholders})"
                params.extend(filter_pdf_ids)

            if min_quality > 0:
                query += " AND i.quality_score >= ?"
                params.append(min_quality)

            cursor = conn.execute(query, params)

            candidates = []
            for row in cursor.fetchall():
                img_dict = dict(row)

                # Deserialize embedding
                if img_dict['embedding']:
                    embedding_bytes = img_dict['embedding']
                    embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)
                    img_dict['embedding'] = embedding_array.tolist()

                candidates.append(img_dict)

            return candidates

    def _score_candidates(
        self,
        candidates: List[Dict[str, Any]],
        query_embedding: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Calculate similarity scores for candidates"""
        scored = []

        for candidate in candidates:
            img_embedding = np.array(candidate['embedding'])

            # Cosine similarity
            similarity = self._cosine_similarity(query_embedding, img_embedding)

            candidate['similarity_score'] = float(similarity)
            scored.append(candidate)

        return scored

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _generate_explanation(self, image: Dict[str, Any]) -> str:
        """Generate explanation for why image was recommended"""
        explanations = []

        similarity = image.get('similarity_score', 0)
        if similarity > 0.8:
            explanations.append("Highly relevant")
        elif similarity > 0.7:
            explanations.append("Relevant")

        quality = image.get('quality_score')
        if quality and quality > 0.7:
            explanations.append("High quality")

        return " • ".join(explanations) if explanations else "Good match"
```

### 4.4 Integration with Chapter Generator

```python
# In neurosurgical_chapter_generator.py

async def _select_images_for_sections(
    self,
    sections: List[Dict[str, Any]],
    reference_pdf_ids: List[str]
) -> Dict[int, List[Dict[str, Any]]]:
    """
    Select images for each section using recommendation system

    Returns:
        {section_index: [image_list]}
    """
    from images.image_recommender import ImageRecommender

    recommender = ImageRecommender(
        db_manager=self.library.db,
        diversity_threshold=self.config.image_diversity_threshold
    )

    section_images = {}

    for i, section in enumerate(sections):
        images = await recommender.recommend_for_section(
            section_title=section['title'],
            section_content=section['content'],
            max_images=self.config.max_images_per_section,
            filter_pdf_ids=reference_pdf_ids
        )

        section_images[i] = images

        logger.info(f"Section '{section['title']}': {len(images)} images")

    return section_images
```

### 4.5 Testing Strategy

```python
"""
test_image_recommendations.py
"""

import pytest
import numpy as np
from images.diversity_booster import DiversityBooster
from images.image_recommender import ImageRecommender

def test_diversity_booster_removes_duplicates():
    """Test that diversity boosting removes near-duplicate images"""
    booster = DiversityBooster(diversity_threshold=0.95)

    # Create mock candidates with embeddings
    # First two are very similar (0.98 similarity)
    # Third is different
    candidates = [
        {
            'id': '1',
            'embedding': [1.0, 0.0, 0.0],
            'similarity_score': 0.9
        },
        {
            'id': '2',
            'embedding': [0.98, 0.02, 0.0],  # Very similar to first
            'similarity_score': 0.85
        },
        {
            'id': '3',
            'embedding': [0.0, 1.0, 0.0],  # Different
            'similarity_score': 0.8
        }
    ]

    results = booster.apply_diversity_boosting(candidates, max_results=3)

    # Should select 1 and 3, skip 2 (too similar to 1)
    assert len(results) == 2
    assert results[0]['id'] == '1'
    assert results[1]['id'] == '3'

@pytest.mark.asyncio
async def test_image_recommender_finds_relevant_images(mock_db):
    """Test that recommender finds relevant images"""
    recommender = ImageRecommender(mock_db)

    results = await recommender.recommend_for_section(
        section_title="Temporal Craniotomy Approach",
        section_content="Description of surgical approach to temporal lobe...",
        max_images=5
    )

    assert len(results) > 0
    assert all('similarity_score' in r for r in results)
    assert all('file_path' in r for r in results)
```

### 4.6 Configuration

```yaml
# Image recommendation settings
images:
  enable_recommendations: true
  max_images_per_section: 5
  min_quality_score: 0.5
  diversity_threshold: 0.95  # 95% similar = duplicate

  # Filtering
  filter_by_pdf: true  # Only use images from specified reference PDFs
  prefer_recent: false
```

### 4.7 Deliverables

- [ ] `images/embedding_service.py` - Image embedding generation
- [ ] `images/diversity_booster.py` - Duplicate avoidance
- [ ] `images/image_recommender.py` - Main recommendation service
- [ ] Integration with chapter generator
- [ ] `tests/test_image_recommendations.py` - Tests
- [ ] Documentation: `IMAGE_RECOMMENDATIONS_GUIDE.md`

### 4.8 Success Criteria

✅ Automatically selects relevant images for sections
✅ Diversity boosting prevents near-duplicates
✅ Image quality filtering works correctly
✅ Similarity scoring is accurate
✅ All tests pass

---

## Phase 5: Section Regeneration

**Duration:** 2-3 days
**Complexity:** Low-Medium
**Benefit:** 84% cost savings for updates
**Status:** SHOULD HAVE
**Dependencies:** Phases 1-3 complete

### 5.1 Objective

Enable targeted regeneration of individual chapter sections without re-running the entire pipeline, achieving massive cost savings.

### 5.2 Cost Comparison

```
FULL REGENERATION:
┌──────────────────────────────────────┐
│ Stage 1: Topic Analysis       $0.05  │
│ Stage 2: Outline Generation   $0.05  │
│ Stage 3: Internal Research    $0.10  │
│ Stage 4: External Research    $0.15  │
│ Stage 5: Gap Detection        $0.10  │
│ Stage 6: Section Generation   $0.15  │
└──────────────────────────────────────┘
TOTAL: $0.60

SECTION REGENERATION:
┌──────────────────────────────────────┐
│ Reuse Stages 1-5 (cached)     $0.00  │
│ Stage 6: Regenerate Section   $0.10  │
└──────────────────────────────────────┘
TOTAL: $0.10

SAVINGS: 84%
```

### 5.3 Architecture

```
Research Data Storage:
┌─────────────────────────────────────────┐
│  Generated Chapter Metadata             │
│  - topic, config, outline               │
│  - research_data (stages 3-5) ← CACHED │
│  - sections (individual content)        │
└─────────────────────────────────────────┘

Section Regeneration Flow:
1. Load existing chapter metadata
2. Retrieve cached research_data
3. Optionally add new sources
4. Apply user instructions
5. Regenerate target section ONLY
6. Update section in database
7. Rebuild PDF
```

### 5.4 Components

#### 5.4.1 Chapter Storage (`generation/chapter_storage.py`)

```python
"""
Persistent storage for generated chapters
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from ..reference_library.database import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ChapterStorage:
    """
    Store and retrieve generated chapters with research data

    Enables section regeneration without re-running research
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def save_chapter(
        self,
        chapter_id: str,
        topic: str,
        config_path: Optional[str],
        output_pdf_path: str,
        research_data: Dict[str, Any],
        sections: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> str:
        """
        Save generated chapter with all metadata

        Args:
            chapter_id: Unique chapter identifier
            topic: Chapter topic
            config_path: Path to config file used
            output_pdf_path: Path to generated PDF
            research_data: Complete research data (stages 3-5)
            sections: List of section content
            metrics: Quality metrics

        Returns:
            chapter_id
        """
        with self.db.get_connection() as conn:
            # Save main chapter record
            conn.execute("""
                INSERT INTO generated_chapters
                (id, topic, config_path, output_pdf_path, research_data, metrics, created_at, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chapter_id,
                topic,
                config_path,
                output_pdf_path,
                json.dumps(research_data),
                json.dumps(metrics),
                datetime.now().isoformat(),
                1
            ))

            # Save sections
            for i, section in enumerate(sections):
                section_id = f"{chapter_id}_sec{i}"

                conn.execute("""
                    INSERT INTO chapter_sections
                    (id, chapter_id, section_number, title, content, source_ids)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    section_id,
                    chapter_id,
                    i,
                    section['title'],
                    section['content'],
                    json.dumps(section.get('source_ids', []))
                ))

        logger.info(f"Saved chapter '{topic}' with {len(sections)} sections")
        return chapter_id

    def load_chapter(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        """Load complete chapter data"""
        with self.db.get_connection() as conn:
            # Load main chapter
            cursor = conn.execute("""
                SELECT * FROM generated_chapters WHERE id = ?
            """, (chapter_id,))

            chapter_row = cursor.fetchone()
            if not chapter_row:
                return None

            chapter = dict(chapter_row)

            # Parse JSON fields
            chapter['research_data'] = json.loads(chapter['research_data'])
            chapter['metrics'] = json.loads(chapter['metrics'])

            # Load sections
            cursor = conn.execute("""
                SELECT * FROM chapter_sections
                WHERE chapter_id = ?
                ORDER BY section_number
            """, (chapter_id,))

            sections = []
            for row in cursor.fetchall():
                section = dict(row)
                section['source_ids'] = json.loads(section['source_ids'])
                sections.append(section)

            chapter['sections'] = sections

            return chapter

    def update_section(
        self,
        chapter_id: str,
        section_number: int,
        new_content: str,
        new_source_ids: List[str]
    ):
        """Update a specific section"""
        with self.db.get_connection() as conn:
            conn.execute("""
                UPDATE chapter_sections
                SET content = ?,
                    source_ids = ?,
                    regenerated_at = ?,
                    regeneration_count = regeneration_count + 1
                WHERE chapter_id = ? AND section_number = ?
            """, (
                new_content,
                json.dumps(new_source_ids),
                datetime.now().isoformat(),
                chapter_id,
                section_number
            ))

            # Update chapter version
            conn.execute("""
                UPDATE generated_chapters
                SET version = version + 1,
                    updated_at = ?
                WHERE id = ?
            """, (datetime.now().isoformat(), chapter_id))

        logger.info(f"Updated section {section_number} in chapter {chapter_id}")
```

#### 5.4.2 Section Regenerator (`generation/section_regenerator.py`)

```python
"""
Regenerate individual sections efficiently
"""

from typing import Dict, Any, List, Optional
import asyncio

from .chapter_storage import ChapterStorage
from ..ai.provider_router import AIProviderRouter
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SectionRegenerator:
    """
    Regenerate individual chapter sections

    Key Innovation: Reuse research data (stages 3-5) from original generation
    Cost: ~$0.10 vs $0.60 for full regeneration (84% savings)
    """

    def __init__(
        self,
        chapter_storage: ChapterStorage,
        ai_provider: AIProviderRouter
    ):
        self.storage = chapter_storage
        self.ai = ai_provider

    async def regenerate_section(
        self,
        chapter_id: str,
        section_number: int,
        instructions: Optional[str] = None,
        additional_sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Regenerate a specific section

        Args:
            chapter_id: Chapter to update
            section_number: Section index to regenerate (0-based)
            instructions: Optional instructions (e.g., "Add more detail on complications")
            additional_sources: Optional additional reference IDs to include

        Returns:
            {
                'section_number': int,
                'new_content': str,
                'old_content': str,
                'changes_summary': str,
                'cost': float
            }
        """
        logger.info(f"Regenerating section {section_number} in chapter {chapter_id}")

        # Step 1: Load existing chapter
        chapter = self.storage.load_chapter(chapter_id)

        if not chapter:
            raise ValueError(f"Chapter {chapter_id} not found")

        if section_number >= len(chapter['sections']):
            raise ValueError(f"Section {section_number} does not exist")

        target_section = chapter['sections'][section_number]
        old_content = target_section['content']

        # Step 2: Retrieve cached research data
        research_data = chapter['research_data']

        # Step 3: Optionally enhance with additional sources
        if additional_sources:
            logger.info(f"Adding {len(additional_sources)} additional sources")
            # Add to internal sources
            if 'internal_sources' not in research_data:
                research_data['internal_sources'] = []

            for source_id in additional_sources:
                research_data['internal_sources'].append({
                    'id': source_id,
                    'manually_added': True
                })

        # Step 4: Generate new section content
        new_content = await self._generate_section_content(
            section_title=target_section['title'],
            section_number=section_number,
            total_sections=len(chapter['sections']),
            research_data=research_data,
            instructions=instructions,
            previous_content=old_content
        )

        # Step 5: Update storage
        self.storage.update_section(
            chapter_id=chapter_id,
            section_number=section_number,
            new_content=new_content,
            new_source_ids=self._extract_source_ids(research_data)
        )

        # Step 6: Generate change summary
        changes_summary = await self._summarize_changes(old_content, new_content)

        return {
            'section_number': section_number,
            'section_title': target_section['title'],
            'new_content': new_content,
            'old_content': old_content,
            'changes_summary': changes_summary,
            'cost': 0.10,  # Approximate
            'savings_vs_full': 0.50  # Saved $0.50 vs full regeneration
        }

    async def _generate_section_content(
        self,
        section_title: str,
        section_number: int,
        total_sections: int,
        research_data: Dict[str, Any],
        instructions: Optional[str],
        previous_content: str
    ) -> str:
        """Generate new content for section"""

        # Build context from research data
        context = self._build_research_context(research_data)

        # Build prompt
        prompt = f"""You are a neurosurgeon writing a comprehensive textbook chapter.

SECTION TO REGENERATE: {section_title} (Section {section_number + 1} of {total_sections})

RESEARCH MATERIALS:
{context}

PREVIOUS VERSION:
{previous_content[:1000]}...

REGENERATION INSTRUCTIONS:
{instructions or "Improve clarity, add more technical detail, and ensure accuracy."}

Write an improved version of this section that:
1. Incorporates the research materials
2. Follows the regeneration instructions
3. Maintains consistent style with a medical textbook
4. Is comprehensive and detailed (500-800 words)
5. Uses proper medical terminology

IMPORTANT: Write ONLY the section content, no meta-commentary."""

        response = await self.ai.generate_text(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7
        )

        return response['content']

    def _build_research_context(self, research_data: Dict[str, Any]) -> str:
        """Build research context string"""
        context_parts = []

        # Internal sources
        if 'internal_sources' in research_data:
            context_parts.append("INTERNAL REFERENCES:")
            for source in research_data['internal_sources'][:10]:
                context_parts.append(f"- {source.get('title', 'Unknown')}")

        # External sources
        if 'external_pubmed' in research_data:
            context_parts.append("\nPUBMED ARTICLES:")
            for source in research_data['external_pubmed'][:5]:
                context_parts.append(f"- {source.get('title', 'Unknown')}")

        return "\n".join(context_parts)

    def _extract_source_ids(self, research_data: Dict[str, Any]) -> List[str]:
        """Extract source IDs from research data"""
        source_ids = []

        if 'internal_sources' in research_data:
            source_ids.extend([s['id'] for s in research_data['internal_sources']])

        return source_ids

    async def _summarize_changes(self, old_content: str, new_content: str) -> str:
        """Generate summary of changes"""

        prompt = f"""Compare these two versions of a medical textbook section and summarize the key changes in 2-3 bullet points.

OLD VERSION:
{old_content[:500]}...

NEW VERSION:
{new_content[:500]}...

Summarize what changed (focus on content changes, not just wording):"""

        response = await self.ai.generate_text(
            prompt=prompt,
            max_tokens=200,
            temperature=0.3
        )

        return response['content']
```

### 5.5 CLI Integration

```bash
# Add to quickstart.sh

regenerate_section() {
    echo "Section Regeneration"
    echo "===================="

    read -p "Enter chapter ID: " chapter_id
    read -p "Enter section number (0-based): " section_num
    read -p "Enter instructions (optional): " instructions

    python3 -c "
import asyncio
from generation.section_regenerator import SectionRegenerator
from generation.chapter_storage import ChapterStorage
from reference_library.database import DatabaseManager
from ai.provider_router import AIProviderRouter

async def main():
    db = DatabaseManager()
    storage = ChapterStorage(db)
    ai = AIProviderRouter()
    regenerator = SectionRegenerator(storage, ai)

    result = await regenerator.regenerate_section(
        chapter_id='$chapter_id',
        section_number=int('$section_num'),
        instructions='$instructions' if '$instructions' else None
    )

    print(f\"Section regenerated: {result['section_title']}\")
    print(f\"Changes: {result['changes_summary']}\")
    print(f\"Cost: \${result['cost']:.2f}\")
    print(f\"Savings: \${result['savings_vs_full']:.2f}\")

asyncio.run(main())
    "
}
```

### 5.6 Configuration

```yaml
# Section regeneration settings
section_regeneration:
  enabled: true
  save_chapter_metadata: true  # Required for regeneration
  save_research_data: true     # Cache stages 3-5
  keep_versions: 5             # Number of versions to keep
```

### 5.7 Deliverables

- [ ] `generation/chapter_storage.py` - Persistent storage
- [ ] `generation/section_regenerator.py` - Regeneration logic
- [ ] Database schema updates for chapter storage
- [ ] CLI integration
- [ ] `tests/test_section_regeneration.py` - Tests
- [ ] Documentation: `SECTION_REGENERATION_GUIDE.md`

### 5.8 Success Criteria

✅ Can regenerate individual sections
✅ Reuses cached research data (84% cost savings)
✅ Can add additional sources to regeneration
✅ Tracks section versions
✅ Generates accurate change summaries
✅ All tests pass

---

## Phase 6: Dual AI Provider System

**Duration:** 3-4 days
**Complexity:** Medium
**Benefit:** Cost optimization + resilience
**Status:** SHOULD HAVE
**Dependencies:** None (independent)

### 6.1 Objective

Implement multi-provider AI routing with automatic failover, cost optimization, and task-specific model selection.

### 6.2 Provider Comparison

```
┌─────────────┬──────────────┬───────────┬────────────┐
│ Provider    │ Cost/1M Tok  │ Speed     │ Best For   │
├─────────────┼──────────────┼───────────┼────────────┤
│ Claude      │ $3.00-$15.00 │ Medium    │ Medical    │
│             │              │           │ Accuracy   │
├─────────────┼──────────────┼───────────┼────────────┤
│ GPT-4       │ $2.50-$10.00 │ Fast      │ Reliability│
│             │              │           │ JSON       │
├─────────────┼──────────────┼───────────┼────────────┤
│ Gemini      │ $0.075-$7.50 │ Very Fast │ Cost       │
│             │              │           │ Drafts     │
└─────────────┴──────────────┴───────────┴────────────┘

Cost Savings Example:
- Using Gemini for drafts: 96% cheaper than Perplexity
- Using Claude for final: Quality where it matters
- Automatic failover: 99.9% uptime
```

### 6.3 Components

#### 6.3.1 Provider Interface (`ai/providers/base_provider.py`)

```python
"""
Base interface for AI providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate text completion

        Returns:
            {
                'content': str,
                'tokens_used': int,
                'cost': float,
                'provider': str,
                'model': str
            }
        """
        pass

    @abstractmethod
    async def generate_embedding(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Generate embedding vector

        Returns:
            {
                'embedding': List[float],
                'model': str,
                'cost': float
            }
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
```

#### 6.3.2 Claude Provider (`ai/providers/claude_provider.py`)

```python
"""
Anthropic Claude provider
"""

from typing import Dict, Any, Optional
from anthropic import Anthropic, APIError
import os

from .base_provider import BaseAIProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)

class ClaudeProvider(BaseAIProvider):
    """
    Claude AI provider

    Best for:
    - Medical accuracy
    - Complex reasoning
    - Long-form content
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "claude-3-5-sonnet-20241022"
    ):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.default_model = default_model
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate text using Claude"""

        if not self.client:
            raise ValueError("Claude API key not configured")

        try:
            response = self.client.messages.create(
                model=self.default_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "You are a helpful AI assistant.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens

            # Estimate cost (Sonnet 3.5: $3/$15 per 1M tokens)
            cost = (response.usage.input_tokens * 3 / 1_000_000) + \
                   (response.usage.output_tokens * 15 / 1_000_000)

            return {
                'content': content,
                'tokens_used': tokens_used,
                'cost': cost,
                'provider': 'claude',
                'model': self.default_model
            }

        except APIError as e:
            logger.error(f"Claude API error: {e}")
            raise

    async def generate_embedding(self, text: str) -> Dict[str, Any]:
        """Claude doesn't provide embeddings - raise error"""
        raise NotImplementedError("Claude doesn't provide embedding API")

    def get_provider_name(self) -> str:
        return "claude"

    def is_available(self) -> bool:
        return self.client is not None
```

#### 6.3.3 OpenAI Provider (`ai/providers/openai_provider.py`)

```python
"""
OpenAI GPT provider
"""

from typing import Dict, Any, Optional
from openai import OpenAI, APIError
import os

from .base_provider import BaseAIProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)

class OpenAIProvider(BaseAIProvider):
    """
    OpenAI GPT provider

    Best for:
    - Reliability
    - JSON outputs
    - Embeddings
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gpt-4o"
    ):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.default_model = default_model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate text using GPT"""

        if not self.client:
            raise ValueError("OpenAI API key not configured")

        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_prompt or "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            # Estimate cost (GPT-4o: $2.50/$10 per 1M tokens)
            cost = (response.usage.prompt_tokens * 2.50 / 1_000_000) + \
                   (response.usage.completion_tokens * 10 / 1_000_000)

            return {
                'content': content,
                'tokens_used': tokens_used,
                'cost': cost,
                'provider': 'openai',
                'model': self.default_model
            }

        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def generate_embedding(self, text: str) -> Dict[str, Any]:
        """Generate embedding using text-embedding-3-small"""

        if not self.client:
            raise ValueError("OpenAI API key not configured")

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:8000]
        )

        # Cost: $0.02 per 1M tokens
        cost = len(text.split()) * 0.02 / 1_000_000

        return {
            'embedding': response.data[0].embedding,
            'model': 'text-embedding-3-small',
            'cost': cost
        }

    def get_provider_name(self) -> str:
        return "openai"

    def is_available(self) -> bool:
        return self.client is not None
```

#### 6.3.4 Gemini Provider (`ai/providers/gemini_provider.py`)

```python
"""
Google Gemini provider
"""

from typing import Dict, Any, Optional
import google.generativeai as genai
import os

from .base_provider import BaseAIProvider
from ...utils.logger import get_logger

logger = get_logger(__name__)

class GeminiProvider(BaseAIProvider):
    """
    Google Gemini provider

    Best for:
    - Cost savings (96% cheaper than Perplexity)
    - Fast drafts
    - High volume operations
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gemini-1.5-flash"
    ):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.default_model = default_model

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(default_model)
        else:
            self.model = None

    async def generate_text(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate text using Gemini"""

        if not self.model:
            raise ValueError("Gemini API key not configured")

        try:
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )

            content = response.text

            # Estimate tokens (approximate)
            tokens_used = len(prompt.split()) + len(content.split())

            # Cost (Gemini Flash: $0.075/$0.30 per 1M tokens)
            cost = tokens_used * 0.15 / 1_000_000

            return {
                'content': content,
                'tokens_used': tokens_used,
                'cost': cost,
                'provider': 'gemini',
                'model': self.default_model
            }

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    async def generate_embedding(self, text: str) -> Dict[str, Any]:
        """Generate embedding using Gemini"""

        if not self.model:
            raise ValueError("Gemini API key not configured")

        result = genai.embed_content(
            model="models/embedding-001",
            content=text[:8000]
        )

        return {
            'embedding': result['embedding'],
            'model': 'embedding-001',
            'cost': 0.0  # Free tier
        }

    def get_provider_name(self) -> str:
        return "gemini"

    def is_available(self) -> bool:
        return self.model is not None
```

#### 6.3.5 Provider Router (`ai/provider_router.py`)

```python
"""
Smart routing between AI providers
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import asyncio

from .providers.base_provider import BaseAIProvider
from .providers.claude_provider import ClaudeProvider
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider
from .circuit_breaker import CircuitBreaker
from ..utils.logger import get_logger

logger = get_logger(__name__)

class TaskType(Enum):
    """Types of AI tasks for routing"""
    MEDICAL_CONTENT = "medical_content"      # Use Claude (accuracy)
    DRAFT_CONTENT = "draft_content"          # Use Gemini (cost)
    JSON_EXTRACTION = "json_extraction"      # Use GPT-4 (reliability)
    EMBEDDING = "embedding"                  # Use OpenAI (only option)
    GENERAL = "general"                      # Use cheapest available

class AIProviderRouter:
    """
    Route AI requests to optimal provider

    Features:
    - Task-specific routing
    - Automatic failover
    - Circuit breaker pattern
    - Cost tracking
    """

    def __init__(self):
        # Initialize providers
        self.providers = {
            'claude': ClaudeProvider(),
            'openai': OpenAIProvider(),
            'gemini': GeminiProvider()
        }

        # Circuit breakers for each provider
        self.circuit_breakers = {
            name: CircuitBreaker(
                failure_threshold=3,
                recovery_timeout=60
            )
            for name in self.providers.keys()
        }

        # Cost tracking
        self.total_cost = 0.0
        self.cost_by_provider = {name: 0.0 for name in self.providers.keys()}

    async def generate_text(
        self,
        prompt: str,
        task_type: TaskType = TaskType.GENERAL,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
        force_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate text using optimal provider

        Args:
            prompt: Text prompt
            task_type: Type of task (determines provider selection)
            force_provider: Override automatic selection

        Returns:
            Generation result with metadata
        """

        # Determine provider order
        if force_provider:
            provider_order = [force_provider]
        else:
            provider_order = self._get_provider_order(task_type)

        # Try providers in order with circuit breaker
        last_error = None

        for provider_name in provider_order:
            provider = self.providers.get(provider_name)
            circuit_breaker = self.circuit_breakers[provider_name]

            if not provider or not provider.is_available():
                logger.debug(f"Provider {provider_name} not available")
                continue

            # Check circuit breaker
            if not circuit_breaker.can_execute():
                logger.warning(f"Circuit breaker open for {provider_name}")
                continue

            try:
                logger.info(f"Using provider: {provider_name} for {task_type.value}")

                result = await provider.generate_text(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system_prompt=system_prompt
                )

                # Track cost
                cost = result.get('cost', 0)
                self.total_cost += cost
                self.cost_by_provider[provider_name] += cost

                # Record success
                circuit_breaker.record_success()

                return result

            except Exception as e:
                logger.error(f"Provider {provider_name} failed: {e}")
                circuit_breaker.record_failure()
                last_error = e
                continue

        # All providers failed
        raise Exception(f"All AI providers failed. Last error: {last_error}")

    async def generate_embedding(
        self,
        text: str,
        force_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate embedding (uses OpenAI or Gemini)"""

        provider_order = [force_provider] if force_provider else ['openai', 'gemini']

        for provider_name in provider_order:
            provider = self.providers.get(provider_name)

            if not provider or not provider.is_available():
                continue

            try:
                result = await provider.generate_embedding(text)
                return result
            except NotImplementedError:
                continue
            except Exception as e:
                logger.error(f"Embedding failed with {provider_name}: {e}")
                continue

        raise Exception("No providers available for embeddings")

    def _get_provider_order(self, task_type: TaskType) -> List[str]:
        """
        Determine provider priority order based on task type

        Strategy:
        - Medical content: Claude > GPT-4 > Gemini (accuracy priority)
        - Draft content: Gemini > GPT-4 > Claude (cost priority)
        - JSON: GPT-4 > Claude > Gemini (reliability priority)
        - General: Gemini > GPT-4 > Claude (cost priority)
        """

        if task_type == TaskType.MEDICAL_CONTENT:
            return ['claude', 'openai', 'gemini']

        elif task_type == TaskType.DRAFT_CONTENT:
            return ['gemini', 'openai', 'claude']

        elif task_type == TaskType.JSON_EXTRACTION:
            return ['openai', 'claude', 'gemini']

        else:  # GENERAL
            return ['gemini', 'openai', 'claude']

    def get_cost_stats(self) -> Dict[str, Any]:
        """Get cost statistics"""
        return {
            'total_cost': round(self.total_cost, 2),
            'cost_by_provider': {
                name: round(cost, 2)
                for name, cost in self.cost_by_provider.items()
            },
            'primary_provider': max(
                self.cost_by_provider.items(),
                key=lambda x: x[1]
            )[0] if self.total_cost > 0 else None
        }
```

#### 6.3.6 Circuit Breaker (`ai/circuit_breaker.py`)

```python
"""
Circuit breaker pattern for provider resilience
"""

from datetime import datetime, timedelta
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failures detected, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures

    Pattern:
    - CLOSED: Normal operation, track failures
    - OPEN: Too many failures, reject requests
    - HALF_OPEN: After timeout, test if service recovered
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 60
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.opened_at = None

    def can_execute(self) -> bool:
        """Check if request can be executed"""

        if self.state == CircuitState.CLOSED:
            return True

        elif self.state == CircuitState.OPEN:
            # Check if recovery timeout passed
            if self.opened_at:
                elapsed = (datetime.now() - self.opened_at).total_seconds()
                if elapsed >= self.recovery_timeout:
                    self.state = CircuitState.HALF_OPEN
                    return True
            return False

        else:  # HALF_OPEN
            return True

    def record_success(self):
        """Record successful request"""
        if self.state == CircuitState.HALF_OPEN:
            # Service recovered
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            self.opened_at = None

        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self):
        """Record failed request"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
```

### 6.8 Configuration

```yaml
# AI provider settings
ai_providers:
  # Task routing strategy
  routing:
    medical_content: ["claude", "openai", "gemini"]
    draft_content: ["gemini", "openai", "claude"]
    json_extraction: ["openai", "claude", "gemini"]

  # API keys
  claude_api_key: ${ANTHROPIC_API_KEY}
  openai_api_key: ${OPENAI_API_KEY}
  gemini_api_key: ${GOOGLE_API_KEY}

  # Circuit breaker
  circuit_breaker:
    failure_threshold: 3
    recovery_timeout_seconds: 60

  # Cost tracking
  track_costs: true
  cost_alert_threshold: 10.0  # Alert if cost exceeds $10
```

### 6.9 Deliverables

- [ ] `ai/providers/base_provider.py` - Abstract interface
- [ ] `ai/providers/claude_provider.py` - Claude implementation
- [ ] `ai/providers/openai_provider.py` - OpenAI implementation
- [ ] `ai/providers/gemini_provider.py` - Gemini implementation
- [ ] `ai/provider_router.py` - Smart routing
- [ ] `ai/circuit_breaker.py` - Resilience pattern
- [ ] `tests/test_ai_providers.py` - Comprehensive tests
- [ ] Documentation: `AI_PROVIDERS_GUIDE.md`

### 6.10 Success Criteria

✅ All three providers work correctly
✅ Automatic failover on provider failure
✅ Circuit breaker prevents cascading failures
✅ Task-specific routing chooses optimal provider
✅ Cost tracking is accurate
✅ All tests pass

---

## Phase 7: "Alive Chapter" Foundation

**Duration:** 4-5 days
**Complexity:** Medium-High
**Benefit:** Long-term chapter evolution
**Status:** NICE TO HAVE (Foundation for future)
**Dependencies:** Phases 1-6 complete

### 7.1 Objective

Create the foundational architecture for chapters that can evolve over time based on new research, user feedback, and detected knowledge gaps.

### 7.2 Concept

```
"Alive Chapter" = Chapter that continuously improves itself

Components:
1. Update Monitor: Detect new relevant research
2. Gap Detector: Identify missing information
3. User Feedback: Collect improvement suggestions
4. Auto-Regeneration: Trigger section updates when needed

Flow:
┌─────────────────┐
│ Monitor PubMed  │ ← Check weekly for new research
│ New Papers      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyze Gap     │ ← Compare to existing chapter
│ Detection       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Notify User     │ ← "3 new relevant papers found"
│ Suggest Update  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Auto-Regenerate │ ← Update relevant sections
│ Affected Sections│
└─────────────────┘
```

### 7.3 Components

#### 7.3.1 Update Monitor (`alive_chapters/monitor.py`)

```python
"""
Monitor for new relevant research
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from ..research.external_research import ExternalResearch
from ..generation.chapter_storage import ChapterStorage
from ..utils.logger import get_logger

logger = get_logger(__name__)

class UpdateMonitor:
    """
    Monitor external sources for updates relevant to chapters

    Features:
    - Periodic PubMed checks
    - New paper detection
    - Relevance scoring
    - Update notifications
    """

    def __init__(
        self,
        chapter_storage: ChapterStorage,
        external_research: ExternalResearch
    ):
        self.storage = chapter_storage
        self.research = external_research

    async def check_for_updates(
        self,
        chapter_id: str,
        days_since_last_check: int = 7
    ) -> Dict[str, Any]:
        """
        Check for new relevant research since last update

        Args:
            chapter_id: Chapter to check
            days_since_last_check: Days to look back

        Returns:
            {
                'new_papers': List[Dict],
                'relevance_scores': List[float],
                'update_recommended': bool,
                'affected_sections': List[int]
            }
        """
        logger.info(f"Checking for updates to chapter {chapter_id}")

        # Load chapter
        chapter = self.storage.load_chapter(chapter_id)
        if not chapter:
            raise ValueError(f"Chapter {chapter_id} not found")

        topic = chapter['topic']

        # Search for recent papers
        cutoff_date = datetime.now() - timedelta(days=days_since_last_check)

        new_papers = await self.research.search_pubmed(
            query=topic,
            max_results=20,
            recent_years=1  # Only very recent
        )

        # Filter to papers published after cutoff
        new_papers = [
            paper for paper in new_papers
            if self._parse_date(paper.get('publication_date')) > cutoff_date
        ]

        if not new_papers:
            logger.info(f"No new papers found for {topic}")
            return {
                'new_papers': [],
                'update_recommended': False
            }

        logger.info(f"Found {len(new_papers)} new papers")

        # Score relevance to existing sections
        section_relevance = await self._score_section_relevance(
            new_papers,
            chapter['sections']
        )

        # Determine if update is recommended
        update_recommended = any(
            max(scores) > 0.7  # High relevance threshold
            for scores in section_relevance.values()
        )

        # Identify most affected sections
        affected_sections = [
            section_num
            for section_num, scores in section_relevance.items()
            if max(scores) > 0.7
        ]

        return {
            'new_papers': new_papers,
            'total_new_papers': len(new_papers),
            'update_recommended': update_recommended,
            'affected_sections': affected_sections,
            'checked_at': datetime.now().isoformat()
        }

    def _parse_date(self, date_str: Optional[str]) -> datetime:
        """Parse publication date"""
        if not date_str:
            return datetime.min

        try:
            return datetime.fromisoformat(date_str)
        except:
            return datetime.min

    async def _score_section_relevance(
        self,
        papers: List[Dict[str, Any]],
        sections: List[Dict[str, Any]]
    ) -> Dict[int, List[float]]:
        """
        Score relevance of each paper to each section

        Returns:
            {section_number: [relevance_scores]}
        """
        # Simple implementation: keyword overlap
        # Could be enhanced with embeddings in future

        section_relevance = {}

        for section_num, section in enumerate(sections):
            section_text = f"{section['title']} {section['content']}"
            section_keywords = set(section_text.lower().split())

            relevance_scores = []

            for paper in papers:
                paper_text = f"{paper['title']} {paper.get('abstract', '')}"
                paper_keywords = set(paper_text.lower().split())

                # Jaccard similarity
                overlap = len(section_keywords & paper_keywords)
                union = len(section_keywords | paper_keywords)

                relevance = overlap / union if union > 0 else 0
                relevance_scores.append(relevance)

            section_relevance[section_num] = relevance_scores

        return section_relevance
```

#### 7.3.2 Interaction Logger (`alive_chapters/interaction_logger.py`)

```python
"""
Log user interactions and feedback
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json

from ..reference_library.database import DatabaseManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class InteractionLogger:
    """
    Track user interactions with chapters

    Metrics:
    - Sections viewed/read time
    - User ratings
    - Feedback comments
    - Requested improvements
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self._create_tables()

    def _create_tables(self):
        """Create interaction tracking tables"""
        with self.db.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chapter_interactions (
                    id TEXT PRIMARY KEY,
                    chapter_id TEXT NOT NULL,
                    interaction_type TEXT NOT NULL,
                    section_number INTEGER,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_interactions_chapter
                ON chapter_interactions(chapter_id)
            """)

    def log_section_view(
        self,
        chapter_id: str,
        section_number: int,
        duration_seconds: Optional[int] = None
    ):
        """Log section view"""
        self._log_interaction(
            chapter_id=chapter_id,
            interaction_type='section_view',
            section_number=section_number,
            data={'duration_seconds': duration_seconds}
        )

    def log_rating(
        self,
        chapter_id: str,
        rating: int,
        section_number: Optional[int] = None,
        comment: Optional[str] = None
    ):
        """Log user rating (1-5 stars)"""
        self._log_interaction(
            chapter_id=chapter_id,
            interaction_type='rating',
            section_number=section_number,
            data={
                'rating': rating,
                'comment': comment
            }
        )

    def log_feedback(
        self,
        chapter_id: str,
        feedback_type: str,
        section_number: Optional[int],
        content: str
    ):
        """
        Log feedback

        Types:
        - 'missing_info': Section is missing important information
        - 'incorrect': Information appears incorrect
        - 'unclear': Explanation is confusing
        - 'improvement': General improvement suggestion
        """
        self._log_interaction(
            chapter_id=chapter_id,
            interaction_type='feedback',
            section_number=section_number,
            data={
                'feedback_type': feedback_type,
                'content': content
            }
        )

    def _log_interaction(
        self,
        chapter_id: str,
        interaction_type: str,
        section_number: Optional[int],
        data: Dict[str, Any]
    ):
        """Internal method to log interaction"""
        import uuid

        interaction_id = str(uuid.uuid4())

        with self.db.get_connection() as conn:
            conn.execute("""
                INSERT INTO chapter_interactions
                (id, chapter_id, interaction_type, section_number, data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                interaction_id,
                chapter_id,
                interaction_type,
                section_number,
                json.dumps(data)
            ))

        logger.debug(f"Logged {interaction_type} for chapter {chapter_id}")

    def get_chapter_analytics(self, chapter_id: str) -> Dict[str, Any]:
        """Get analytics for chapter"""
        with self.db.get_connection() as conn:
            # Total views
            cursor = conn.execute("""
                SELECT COUNT(*) FROM chapter_interactions
                WHERE chapter_id = ? AND interaction_type = 'section_view'
            """, (chapter_id,))
            total_views = cursor.fetchone()[0]

            # Average rating
            cursor = conn.execute("""
                SELECT AVG(CAST(json_extract(data, '$.rating') AS REAL))
                FROM chapter_interactions
                WHERE chapter_id = ? AND interaction_type = 'rating'
            """, (chapter_id,))
            avg_rating = cursor.fetchone()[0]

            # Feedback count by type
            cursor = conn.execute("""
                SELECT
                    json_extract(data, '$.feedback_type') as feedback_type,
                    COUNT(*) as count
                FROM chapter_interactions
                WHERE chapter_id = ? AND interaction_type = 'feedback'
                GROUP BY feedback_type
            """, (chapter_id,))
            feedback_counts = {row[0]: row[1] for row in cursor.fetchall()}

            return {
                'total_views': total_views,
                'average_rating': round(avg_rating, 2) if avg_rating else None,
                'feedback_counts': feedback_counts
            }
```

#### 7.3.3 Evolution Tracker (`alive_chapters/evolution_tracker.py`)

```python
"""
Track chapter evolution over time
"""

from typing import Dict, Any, List
from datetime import datetime

from ..generation.chapter_storage import ChapterStorage
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EvolutionTracker:
    """
    Track how chapters evolve over time

    Metrics:
    - Version history
    - Section regeneration frequency
    - Improvement sources (new papers, feedback, etc.)
    - Quality progression
    """

    def __init__(self, chapter_storage: ChapterStorage):
        self.storage = chapter_storage

    def track_evolution_event(
        self,
        chapter_id: str,
        event_type: str,
        details: Dict[str, Any]
    ):
        """
        Track evolution event

        Event types:
        - 'section_regenerated': Section was regenerated
        - 'new_papers_added': New research incorporated
        - 'feedback_applied': User feedback addressed
        - 'quality_improved': Quality metrics improved
        """
        # Store in chapter metadata
        chapter = self.storage.load_chapter(chapter_id)

        if not chapter:
            return

        evolution_events = chapter.get('evolution_events', [])

        evolution_events.append({
            'event_type': event_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

        # Update chapter with evolution history
        # (Implementation depends on chapter_storage schema)

        logger.info(f"Tracked evolution event for {chapter_id}: {event_type}")

    def get_evolution_summary(self, chapter_id: str) -> Dict[str, Any]:
        """Get summary of chapter evolution"""
        chapter = self.storage.load_chapter(chapter_id)

        if not chapter:
            return {}

        evolution_events = chapter.get('evolution_events', [])

        # Count events by type
        event_counts = {}
        for event in evolution_events:
            event_type = event['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            'chapter_id': chapter_id,
            'created_at': chapter['created_at'],
            'current_version': chapter['version'],
            'total_evolution_events': len(evolution_events),
            'event_counts': event_counts,
            'last_updated': chapter.get('updated_at')
        }
```

### 7.4 CLI Integration

```bash
# Add to quickstart.sh

alive_chapter_check() {
    echo "Check for Chapter Updates"
    echo "========================"

    read -p "Enter chapter ID: " chapter_id

    python3 -c "
import asyncio
from alive_chapters.monitor import UpdateMonitor
from generation.chapter_storage import ChapterStorage
from research.external_research import ExternalResearch
from reference_library.database import DatabaseManager

async def main():
    db = DatabaseManager()
    storage = ChapterStorage(db)
    research = ExternalResearch(pubmed_email='user@domain.com')
    monitor = UpdateMonitor(storage, research)

    result = await monitor.check_for_updates('$chapter_id')

    print(f\"New papers found: {result['total_new_papers']}\")
    print(f\"Update recommended: {result['update_recommended']}\")
    print(f\"Affected sections: {result['affected_sections']}\")

asyncio.run(main())
    "
}
```

### 7.5 Configuration

```yaml
# Alive chapter settings
alive_chapters:
  enabled: true

  # Monitoring
  monitor:
    check_interval_days: 7
    pubmed_lookback_days: 30
    relevance_threshold: 0.7

  # Auto-update
  auto_update:
    enabled: false  # Require manual approval
    notify_on_updates: true

  # Interaction tracking
  tracking:
    enabled: true
    anonymize: true
```

### 7.6 Deliverables

- [ ] `alive_chapters/monitor.py` - Update detection
- [ ] `alive_chapters/interaction_logger.py` - User feedback
- [ ] `alive_chapters/evolution_tracker.py` - Change tracking
- [ ] CLI integration for monitoring
- [ ] `tests/test_alive_chapters.py` - Tests
- [ ] Documentation: `ALIVE_CHAPTERS_GUIDE.md`

### 7.7 Success Criteria

✅ Can detect new relevant research
✅ Identifies affected sections accurately
✅ Logs user interactions
✅ Tracks chapter evolution over time
✅ Provides actionable update notifications
✅ All tests pass

---

## Testing Strategy

### Unit Tests

```bash
tests/
├── test_reference_library.py
│   ├── test_database_operations
│   ├── test_pdf_indexing
│   ├── test_embedding_generation
│   └── test_duplicate_detection
│
├── test_hybrid_search.py
│   ├── test_keyword_search
│   ├── test_semantic_search
│   ├── test_hybrid_ranking
│   └── test_recency_scoring
│
├── test_research.py
│   ├── test_parallel_execution
│   ├── test_pubmed_cache
│   ├── test_internal_research
│   └── test_external_research
│
├── test_image_recommendations.py
│   ├── test_diversity_boosting
│   ├── test_similarity_scoring
│   └── test_image_selection
│
├── test_section_regeneration.py
│   ├── test_chapter_storage
│   ├── test_section_update
│   └── test_research_reuse
│
├── test_ai_providers.py
│   ├── test_provider_routing
│   ├── test_circuit_breaker
│   └── test_cost_tracking
│
└── test_alive_chapters.py
    ├── test_update_monitoring
    ├── test_interaction_logging
    └── test_evolution_tracking
```

### Integration Tests

```python
"""
test_integration.py - End-to-end integration tests
"""

import pytest
import asyncio

@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_chapter_generation_with_library():
    """Test complete chapter generation using reference library"""
    # 1. Index reference PDFs
    # 2. Configure chapter
    # 3. Generate chapter with hybrid search
    # 4. Verify images included
    # 5. Check metrics
    pass

@pytest.mark.integration
@pytest.mark.asyncio
async def test_section_regeneration_workflow():
    """Test section regeneration saves cost"""
    # 1. Generate full chapter
    # 2. Regenerate one section
    # 3. Verify cost savings
    # 4. Verify quality maintained
    pass

@pytest.mark.integration
def test_alive_chapter_monitoring():
    """Test monitoring and update detection"""
    # 1. Create chapter
    # 2. Simulate new research
    # 3. Check for updates
    # 4. Verify recommendations
    pass
```

### Performance Tests

```python
"""
test_performance.py - Performance benchmarks
"""

import pytest
import time

@pytest.mark.performance
@pytest.mark.asyncio
async def test_parallel_research_speedup():
    """Verify 40% speedup from parallel execution"""
    # Sequential baseline
    start = time.time()
    # ... sequential research
    sequential_time = time.time() - start

    # Parallel version
    start = time.time()
    # ... parallel research
    parallel_time = time.time() - start

    speedup = (sequential_time - parallel_time) / sequential_time
    assert speedup >= 0.35  # At least 35% faster

@pytest.mark.performance
@pytest.mark.asyncio
async def test_pubmed_cache_speedup():
    """Verify 300x speedup from caching"""
    # First call (no cache)
    start = time.time()
    # ... pubmed search
    uncached_time = time.time() - start

    # Second call (cached)
    start = time.time()
    # ... pubmed search (cached)
    cached_time = time.time() - start

    speedup = uncached_time / cached_time
    assert speedup >= 100  # At least 100x faster
```

---

## Migration Guide

### From Current System to Enhanced System

**Step 1: Backup existing work**
```bash
cp -r "files (4) 3" "files (4) 3_backup"
cd "files (4) 3"
```

**Step 2: Install new dependencies**
```bash
pip install redis biopython google-generativeai sqlalchemy numpy pillow
```

**Step 3: Build reference library**
```bash
# Index your reference materials
python3 -c "
import asyncio
from reference_library.library_manager import ReferenceLibraryManager

async def main():
    library = ReferenceLibraryManager()
    result = await library.add_directory(
        '/Users/ramihatoum/Desktop/Neurosurgery /reference library',
        recursive=True
    )
    print(f'Indexed {result[\"indexed\"]} PDFs')

asyncio.run(main())
"
```

**Step 4: Update configs to use library**
```yaml
# In your chapter configs, add:
use_reference_library: true
library_db_path: "neurosurgery_library.db"
```

**Step 5: Test new features incrementally**
```bash
# Test hybrid search
pytest tests/test_hybrid_search.py

# Test parallel research
pytest tests/test_research.py

# Test full integration
pytest tests/test_integration.py
```

**Step 6: Migrate existing chapters (optional)**
```bash
# Import existing chapters into storage for regeneration capability
python3 scripts/migrate_existing_chapters.py
```

---

## Timeline & Milestones

### Week 1-2: Foundation
- ✅ Phase 1: Reference Library (Week 1-2)
  - Day 1-2: Database schema and management
  - Day 3-5: PDF indexer with AI chapter detection
  - Day 6-7: Library manager and CLI integration
  - Testing and documentation

**Milestone 1: Can index and search reference library**

### Week 3: Search Enhancement
- ✅ Phase 2: Hybrid Search (Week 3)
  - Day 1-2: Keyword and semantic search
  - Day 3-4: Hybrid ranking algorithm
  - Day 5: Integration with chapter generator
  - Testing and documentation

**Milestone 2: Professional-grade search working**

### Week 4: Research Optimization
- ✅ Phase 3: Parallel Research & Caching (Week 4)
  - Day 1-2: Cache manager and PubMed client
  - Day 3-4: Parallel orchestration
  - Day 5-6: Integration and testing
  - Performance benchmarking

**Milestone 3: 40% faster research with 300x cache speedup**

### Week 5: Image Intelligence
- ✅ Phase 4: Image Recommendations (Week 5)
  - Day 1-2: Embedding service
  - Day 3: Diversity boosting
  - Day 4-5: Integration and testing

**Milestone 4: Smart image selection working**

### Week 6: Cost Optimization
- ✅ Phase 5: Section Regeneration (Week 6)
  - Day 1-2: Chapter storage
  - Day 3-4: Section regenerator
  - Day 5: Testing and validation

**Milestone 5: 84% cost savings on updates**

- ✅ Phase 6: Dual AI Providers (Week 6)
  - Day 1: Provider interfaces
  - Day 2-3: Provider implementations
  - Day 4-5: Router and circuit breaker
  - Testing

**Milestone 6: Multi-provider system with failover**

### Week 7: Future Foundation
- ✅ Phase 7: Alive Chapters (Week 7)
  - Day 1-2: Update monitor
  - Day 3: Interaction logger
  - Day 4-5: Evolution tracker
  - Documentation

**Milestone 7: Foundation for continuous evolution complete**

### Total Timeline: 7 weeks

**Quick Win Path (Prioritize value/effort):**
If time is limited, implement in this order:
1. Phase 1: Reference Library (Essential)
2. Phase 3: Parallel Research + Caching (High impact, medium effort)
3. Phase 6: Dual AI Providers (Cost savings, low effort)
4. Phase 2: Hybrid Search (Quality improvement)
5. Phase 5: Section Regeneration (Cost savings)
6. Phase 4: Image Recommendations (Nice to have)
7. Phase 7: Alive Chapters (Future proofing)

---

## Conclusion

This implementation plan transforms your simple chapter generator into a sophisticated, enterprise-grade system while maintaining:

✅ **Modularity**: Each phase is independent and can be implemented separately
✅ **Simplicity**: Clear interfaces, well-documented code
✅ **Power**: Professional features adapted from Neurocore
✅ **Guaranteed Functionality**: Battle-tested patterns
✅ **Cost Efficiency**: 84% savings on updates, 96% savings with Gemini
✅ **Performance**: 40% faster research, 300x cache speedup
✅ **Quality**: Hybrid search, smart image selection
✅ **Future-Ready**: Foundation for "alive chapters"

### Key Achievements:

**Performance Gains:**
- 40% faster research (parallel execution)
- 300x speedup on repeated queries (caching)
- 84% cost reduction on section updates

**Quality Improvements:**
- Professional hybrid search (keyword + semantic + recency)
- Smart image recommendations with diversity boosting
- Multi-provider AI with automatic failover

**Long-Term Value:**
- Reference library grows over time
- Cached research benefits all future chapters
- Foundation for continuously improving chapters

### Next Steps:

1. Review this plan
2. Prioritize phases based on your needs
3. Start with Phase 1 (Reference Library)
4. Implement incrementally, testing each phase
5. Enjoy your enhanced system!

**Questions or clarifications needed? Let me know and I'll provide more detailed guidance on any specific phase.**