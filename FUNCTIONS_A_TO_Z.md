# StudyBuddy - Complete Function Reference (A to Z)

**Version:** 1.0
**Date:** 2025-11-05
**Status:** Planned Implementation

This document provides a comprehensive alphabetical reference of all functions planned for the StudyBuddy AI-Powered Medical Knowledge Base System across all 7 implementation phases.

---

## Table of Contents

- [Phase 0: Foundation](#phase-0-foundation)
- [Phase 1: Reference Library](#phase-1-reference-library)
- [Phase 2: Hybrid Search](#phase-2-hybrid-search)
- [Phase 3: Research Integration](#phase-3-research-integration)
- [Phase 4: Image Recommendations](#phase-4-image-recommendations)
- [Phase 5: Section Regeneration](#phase-5-section-regeneration)
- [Phase 6: Multi-Provider AI](#phase-6-multi-provider-ai)
- [Phase 7: Alive Chapters](#phase-7-alive-chapters)
- [Alphabetical Index](#alphabetical-index)

---

## Phase 0: Foundation

### Exception Hierarchy (`utils/exceptions.py`)

#### `to_dict()`
**Class:** `NeurosurgicalKBException`
**Purpose:** Serialize exception for logging/API responses
**Parameters:** None
**Returns:** `Dict[str, Any]` - Serialized exception data
**Example:**
```python
error = DatabaseConnectionError(context={'host': 'localhost'})
error_dict = error.to_dict()
# {'error_type': 'DatabaseConnectionError', 'message': '...', 'error_code': 'DB_001'}
```

---

### Security Utilities (`utils/security.py`)

#### `generate_secure_id()`
**Class:** `SecurityUtils`
**Purpose:** Generate cryptographically secure unique ID
**Parameters:**
- `prefix: str = ""` - Optional prefix for the ID
**Returns:** `str` - Secure unique identifier
**Example:**
```python
id = SecurityUtils.generate_secure_id("chapter")
# "chapter_a1b2c3d4e5f6..."
```

#### `hash_password()`
**Class:** `SecurityUtils`
**Purpose:** Hash password securely using PBKDF2
**Parameters:**
- `password: str` - Plain text password
- `salt: Optional[str] = None` - Optional salt (generated if not provided)
**Returns:** `tuple[str, str]` - (hashed_password, salt)
**Example:**
```python
hashed, salt = SecurityUtils.hash_password("SecurePassword123!")
```

#### `sanitize_filename()`
**Class:** `InputValidator`
**Purpose:** Sanitize filename to prevent injection and filesystem issues
**Parameters:**
- `filename: str` - Filename to sanitize
- `max_length: int = 255` - Maximum filename length
**Returns:** `str` - Sanitized filename
**Example:**
```python
safe = InputValidator.sanitize_filename("../../../etc/passwd")
# "etc_passwd"
```

#### `sanitize_text()`
**Class:** `InputValidator`
**Purpose:** Sanitize text input for safe storage and display
**Parameters:**
- `text: str` - Input text to sanitize
- `max_length: int = 1000` - Maximum allowed length
- `allow_newlines: bool = True` - Whether to preserve newline characters
**Returns:** `str` - Sanitized text
**Protections:** XSS, HTML injection, control characters
**Example:**
```python
clean = InputValidator.sanitize_text("<script>alert('XSS')</script>Hello")
# "alert('XSS')Hello"
```

#### `validate_email()`
**Class:** `InputValidator`
**Purpose:** Validate email format
**Parameters:**
- `email: str` - Email address to validate
**Returns:** `str` - Normalized email address
**Raises:** `InvalidFormatError` if invalid
**Example:**
```python
email = InputValidator.validate_email("  TEST@EXAMPLE.COM  ")
# "test@example.com"
```

#### `validate_file_path()`
**Class:** `InputValidator`
**Purpose:** Validate file path to prevent path traversal attacks
**Parameters:**
- `path: str` - File path to validate
- `allowed_dirs: List[str]` - List of allowed parent directories
- `must_exist: bool = False` - Whether file must exist
**Returns:** `Path` - Validated Path object
**Raises:** `PathTraversalError` if path traversal detected
**Example:**
```python
safe_path = InputValidator.validate_file_path(
    "/safe/dir/file.pdf",
    allowed_dirs=["/safe/dir"]
)
```

#### `validate_file_size()`
**Class:** `InputValidator`
**Purpose:** Validate file size doesn't exceed limit
**Parameters:**
- `file_path: Path` - Path to file
- `max_size_mb: float = 100` - Maximum size in megabytes
**Returns:** `Path` - Validated file path
**Raises:** `FileTooLargeError` if file too large

#### `validate_float_range()`
**Class:** `InputValidator`
**Purpose:** Validate float is within acceptable range
**Parameters:**
- `value: float` - Value to validate
- `field: str` - Field name for error messages
- `min_val: Optional[float] = None` - Minimum acceptable value
- `max_val: Optional[float] = None` - Maximum acceptable value
**Returns:** `float` - Validated value
**Raises:** `InvalidRangeError` if outside range

#### `validate_integer_range()`
**Class:** `InputValidator`
**Purpose:** Validate integer is within acceptable range
**Parameters:**
- `value: int` - Value to validate
- `field: str` - Field name for error messages
- `min_val: Optional[int] = None` - Minimum acceptable value
- `max_val: Optional[int] = None` - Maximum acceptable value
**Returns:** `int` - Validated value
**Raises:** `InvalidRangeError` if outside range
**Example:**
```python
value = InputValidator.validate_integer_range(10, "page_count", 1, 1000)
```

#### `verify_password()`
**Class:** `SecurityUtils`
**Purpose:** Verify password against hash
**Parameters:**
- `password: str` - Plain text password to verify
- `hashed: str` - Stored hash
- `salt: str` - Salt used during hashing
**Returns:** `bool` - True if password matches

---

### Logging (`utils/logger.py`)

#### `format()`
**Class:** `StructuredFormatter`
**Purpose:** Format log record as JSON
**Parameters:**
- `record: logging.LogRecord` - Log record to format
**Returns:** `str` - JSON formatted log string

#### `get_logger()`
**Module:** `utils.logger`
**Purpose:** Get configured logger instance
**Parameters:**
- `name: str` - Logger name (usually `__name__`)
- `log_level: Optional[str] = None` - Override log level
- `log_format: Optional[str] = None` - Format type (json or text)
- `log_file: Optional[str] = None` - Optional log file path
**Returns:** `logging.Logger` - Configured logger
**Example:**
```python
logger = get_logger(__name__)
logger.info("Starting process", extra={'context': {'user_id': 123}})
```

#### `process()`
**Class:** `LoggerAdapter`
**Purpose:** Add extra context to log record
**Parameters:**
- `msg` - Log message
- `kwargs` - Keyword arguments
**Returns:** Tuple of (msg, kwargs) with merged context

---

### Configuration (`utils/config.py`)

#### `get_settings()`
**Module:** `utils.config`
**Purpose:** Get application settings (singleton)
**Parameters:** None
**Returns:** `Settings` - Settings instance
**Example:**
```python
settings = get_settings()
print(settings.ai.default_provider)  # 'claude'
```

#### `reload_settings()`
**Module:** `utils.config`
**Purpose:** Reload settings from environment (useful for testing)
**Parameters:** None
**Returns:** `Settings` - Fresh settings instance

---

## Phase 1: Reference Library

### Database Management (`reference_library/database.py`)

#### `create_all_tables()`
**Class:** `DatabaseManager`
**Purpose:** Create all database tables
**Parameters:** None
**Returns:** None
**Side Effects:** Creates tables in database

#### `get_connection()`
**Class:** `DatabaseManager`
**Purpose:** Context manager for database connections
**Parameters:** None
**Returns:** Database connection with row factory
**Example:**
```python
with db.get_connection() as conn:
    cursor = conn.execute("SELECT * FROM books")
```

#### `get_session()`
**Class:** `DatabaseManager`
**Purpose:** Get SQLAlchemy session (context manager)
**Parameters:** None
**Returns:** `Generator[Session, None, None]` - Database session
**Example:**
```python
with db.get_session() as session:
    books = session.query(Book).all()
```

---

### Library Management (`reference_library/library_manager.py`)

#### `add_book()`
**Class:** `LibraryManager`
**Purpose:** Add a book to the reference library
**Parameters:**
- `file_path: str` - Path to PDF file
- `ai_chapter_detection: bool = True` - Use AI for chapter detection
- `extract_images: bool = True` - Extract images from PDF
**Returns:** `Dict[str, Any]` - Indexing results with book ID and statistics
**Example:**
```python
result = await manager.add_book(
    file_path="/path/to/neurosurgery.pdf",
    ai_chapter_detection=True
)
# {'book_id': '...', 'chapters_detected': 15, 'images_extracted': 143}
```

#### `delete_book()`
**Class:** `LibraryManager`
**Purpose:** Delete a book and all related data
**Parameters:**
- `book_id: str` - Book UUID
**Returns:** `bool` - True if deleted successfully
**Side Effects:** Cascades delete to chapters, sections, images

#### `get_book_statistics()`
**Class:** `LibraryManager`
**Purpose:** Get statistics for a specific book
**Parameters:**
- `book_id: str` - Book UUID
**Returns:** `Dict[str, Any]` - Book statistics
**Example:**
```python
stats = manager.get_book_statistics(book_id)
# {'chapters': 15, 'images': 143, 'total_pages': 850, 'size_mb': 45.2}
```

#### `list_books()`
**Class:** `LibraryManager`
**Purpose:** List all books in the library
**Parameters:**
- `include_chapters: bool = False` - Include chapter details
- `limit: Optional[int] = None` - Limit number of results
**Returns:** `List[Dict[str, Any]]` - List of books with metadata
**Example:**
```python
books = manager.list_books(include_chapters=True, limit=10)
```

#### `search_books()`
**Class:** `LibraryManager`
**Purpose:** Search books by title, author, or keywords
**Parameters:**
- `query: str` - Search query
- `filters: Optional[Dict] = None` - Additional filters
**Returns:** `List[Dict[str, Any]]` - Matching books

#### `verify_integrity()`
**Class:** `LibraryManager`
**Purpose:** Verify database and file system integrity
**Parameters:** None
**Returns:** `Dict[str, Any]` - Verification results with any issues found

---

### PDF Indexing (`reference_library/pdf_indexer.py`)

#### `detect_chapters()`
**Class:** `PDFIndexer`
**Purpose:** Detect chapter boundaries using AI analysis of TOC
**Parameters:**
- `pdf_path: Path` - Path to PDF file
- `method: str = "ai"` - Detection method (ai, toc, header, manual)
**Returns:** `List[Dict[str, Any]]` - List of detected chapters with boundaries
**Example:**
```python
chapters = await indexer.detect_chapters(pdf_path, method="ai")
# [{'title': 'Chapter 1', 'start_page': 1, 'end_page': 25, 'confidence': 0.95}]
```

#### `extract_chapter_text()`
**Class:** `PDFIndexer`
**Purpose:** Extract text content from chapter page range
**Parameters:**
- `pdf_path: Path` - Path to PDF
- `start_page: int` - Starting page number
- `end_page: int` - Ending page number
**Returns:** `str` - Extracted text content

#### `extract_images()`
**Class:** `PDFIndexer`
**Purpose:** Extract images from PDF pages
**Parameters:**
- `pdf_path: Path` - Path to PDF
- `output_dir: Path` - Directory to save images
- `page_range: Optional[Tuple[int, int]] = None` - Page range to extract from
**Returns:** `List[Dict[str, Any]]` - List of extracted images with metadata

#### `extract_metadata()`
**Class:** `PDFIndexer`
**Purpose:** Extract PDF metadata (title, author, year, etc.)
**Parameters:**
- `pdf_path: Path` - Path to PDF file
**Returns:** `Dict[str, Any]` - PDF metadata
**Example:**
```python
metadata = indexer.extract_metadata(pdf_path)
# {'title': '...', 'author': '...', 'year': 2023, 'page_count': 850}
```

#### `generate_chapter_embeddings()`
**Class:** `PDFIndexer`
**Purpose:** Generate vector embeddings for chapter content
**Parameters:**
- `chapter_text: str` - Chapter text content
- `model: str = "text-embedding-3-small"` - Embedding model to use
**Returns:** `List[float]` - Vector embedding (1536 dimensions)

#### `index_pdf()`
**Class:** `PDFIndexer`
**Purpose:** Complete PDF indexing pipeline
**Parameters:**
- `pdf_path: str` - Path to PDF file
- `extract_chapters: bool = True` - Attempt chapter detection
- `extract_images: bool = True` - Extract and process images
**Returns:** `Dict[str, Any]` - Indexing results and statistics
**Example:**
```python
result = await indexer.index_pdf("/path/to/book.pdf")
# {'status': 'success', 'pdf_id': '...', 'chapters_indexed': 15, 'duration_seconds': 145.3}
```

---

## Phase 2: Hybrid Search

### BM25 Search (`search/bm25_search.py`)

#### `build_index()`
**Class:** `BM25SearchEngine`
**Purpose:** Build BM25 index from all chapters
**Parameters:** None
**Returns:** `Dict[str, Any]` - Indexing statistics
**Side Effects:** Creates in-memory BM25 index

#### `calculate_idf()`
**Class:** `BM25SearchEngine`
**Purpose:** Calculate Inverse Document Frequency for terms
**Parameters:**
- `term: str` - Term to calculate IDF for
**Returns:** `float` - IDF score

#### `get_stats()`
**Class:** `BM25SearchEngine`
**Purpose:** Get search engine statistics
**Parameters:** None
**Returns:** `Dict[str, Any]` - Statistics (document count, index size, etc.)

#### `search()`
**Class:** `BM25SearchEngine`
**Purpose:** Execute BM25 keyword search
**Parameters:**
- `query: str` - Search query
- `limit: int = 20` - Maximum results
- `filters: Optional[Dict] = None` - Additional filters
**Returns:** `List[Dict[str, Any]]` - Ranked search results
**Performance:** < 100ms for 1000 documents
**Example:**
```python
results = bm25.search("temporal craniotomy surgical approach", limit=10)
# [{'chapter_id': '...', 'title': '...', 'score': 4.52, 'excerpt': '...'}]
```

---

### Semantic Search (`search/semantic_search.py`)

#### `find_similar_chapters()`
**Class:** `SemanticSearchEngine`
**Purpose:** Find chapters similar to a given chapter
**Parameters:**
- `chapter_id: str` - Reference chapter ID
- `limit: int = 10` - Maximum results
- `min_similarity: float = 0.7` - Minimum cosine similarity
**Returns:** `List[Dict[str, Any]]` - Similar chapters

#### `generate_query_embedding()`
**Class:** `SemanticSearchEngine`
**Purpose:** Generate embedding for search query
**Parameters:**
- `query: str` - Search query text
**Returns:** `List[float]` - Query embedding vector

#### `search()`
**Class:** `SemanticSearchEngine`
**Purpose:** Execute semantic vector search
**Parameters:**
- `query: str` - Search query
- `limit: int = 20` - Maximum results
- `min_similarity: float = 0.7` - Minimum cosine similarity threshold
**Returns:** `List[Dict[str, Any]]` - Ranked results by similarity
**Performance:** < 500ms with pgvector
**Example:**
```python
results = await semantic.search("brain surgery techniques", limit=10)
# [{'chapter_id': '...', 'similarity': 0.89, 'title': '...'}]
```

---

### Hybrid Search (`search/hybrid_search.py`)

#### `combine_scores()`
**Class:** `HybridSearchEngine`
**Purpose:** Combine BM25 and semantic scores using RRF (Reciprocal Rank Fusion)
**Parameters:**
- `bm25_results: List[Dict]` - BM25 search results
- `semantic_results: List[Dict]` - Semantic search results
- `k: int = 60` - RRF parameter
**Returns:** `List[Dict[str, Any]]` - Fused and re-ranked results

#### `explain_score()`
**Class:** `HybridSearchEngine`
**Purpose:** Explain how a search score was calculated
**Parameters:**
- `result: Dict` - Search result
**Returns:** `Dict[str, Any]` - Score breakdown and explanation

#### `search()`
**Class:** `HybridSearchEngine`
**Purpose:** Execute hybrid search (BM25 + semantic + recency)
**Parameters:**
- `query: str` - Search query
- `limit: int = 20` - Maximum results
- `bm25_weight: float = 0.5` - Weight for BM25 component
- `semantic_weight: float = 0.5` - Weight for semantic component
- `include_explanations: bool = False` - Include score explanations
**Returns:** `List[Dict[str, Any]]` - Hybrid ranked results
**Performance:** < 600ms target
**Example:**
```python
results = await hybrid.search(
    "temporal craniotomy complications",
    limit=10,
    include_explanations=True
)
```

---

## Phase 3: Research Integration

### PubMed Client (`research/pubmed_client.py`)

#### `fetch_article_details()`
**Class:** `PubMedClient`
**Purpose:** Fetch full details for a PubMed article
**Parameters:**
- `pmid: str` - PubMed ID
**Returns:** `Dict[str, Any]` - Article details

#### `search()`
**Class:** `PubMedClient`
**Purpose:** Search PubMed for articles
**Parameters:**
- `query: str` - Search query
- `max_results: int = 10` - Maximum results
- `filters: Optional[Dict] = None` - Filters (date range, article type, etc.)
**Returns:** `List[Dict[str, Any]]` - Article list
**Performance:** 15-30 seconds (first call), < 10ms (cached)
**Example:**
```python
articles = await pubmed.search(
    "temporal lobe epilepsy surgery",
    max_results=20,
    filters={'recent_years': 5}
)
```

#### `search_batch()`
**Class:** `PubMedClient`
**Purpose:** Execute multiple PubMed searches in parallel
**Parameters:**
- `queries: List[str]` - List of search queries
- `max_results_per_query: int = 5` - Results per query
**Returns:** `Dict[str, List[Dict]]` - Results grouped by query
**Performance:** 4x speedup vs sequential

---

### Cache Manager (`research/cache_manager.py`)

#### `get()`
**Class:** `CacheManager`
**Purpose:** Get cached value
**Parameters:**
- `key: str` - Cache key
- `namespace: str = 'default'` - Cache namespace
**Returns:** `Optional[Any]` - Cached value or None
**Performance:** < 10ms

#### `get_stats()`
**Class:** `CacheManager`
**Purpose:** Get cache statistics
**Parameters:** None
**Returns:** `Dict[str, Any]` - Hit rate, size, entries, etc.

#### `invalidate()`
**Class:** `CacheManager`
**Purpose:** Invalidate cache entries by pattern
**Parameters:**
- `pattern: str` - Pattern to match keys (supports wildcards)
- `namespace: str = 'default'` - Cache namespace
**Returns:** `int` - Number of entries invalidated
**Example:**
```python
cache.invalidate("pubmed:temporal*")
```

#### `set()`
**Class:** `CacheManager`
**Purpose:** Set cached value
**Parameters:**
- `key: str` - Cache key
- `value: Any` - Value to cache
- `ttl: int = 604800` - Time to live in seconds (default 7 days)
- `namespace: str = 'default'` - Cache namespace
**Returns:** `bool` - True if successfully cached

---

### Research Orchestrator (`research/research_orchestrator.py`)

#### `research_topic()`
**Class:** `ResearchOrchestrator`
**Purpose:** Research a topic using internal library + PubMed
**Parameters:**
- `topic: str` - Research topic
- `max_results: int = 20` - Maximum total results
- `use_cache: bool = True` - Use cached results if available
- `internal_weight: float = 0.6` - Weight for internal sources
- `external_weight: float = 0.4` - Weight for PubMed sources
**Returns:** `Dict[str, Any]` - Combined research results
**Example:**
```python
research = await orchestrator.research_topic(
    topic="temporal craniotomy surgical technique",
    max_results=20
)
# {
#   'topic': '...',
#   'internal_sources': [...],
#   'external_sources': [...],
#   'cache_hits': 3,
#   'total_time_seconds': 2.4
# }
```

---

## Phase 4: Image Recommendations

### Image Embedding Service (`images/image_embedding_service.py`)

#### `calculate_quality_score()`
**Class:** `ImageEmbeddingService`
**Purpose:** Calculate quality score for an image
**Parameters:**
- `image_path: str` - Path to image file
**Returns:** `float` - Quality score (0.0-1.0)
**Factors:** Resolution, sharpness, contrast

#### `generate_embedding()`
**Class:** `ImageEmbeddingService`
**Purpose:** Generate embedding for a single image
**Parameters:**
- `image_path: str` - Path to image file
- `model: str = 'clip'` - Embedding model
**Returns:** `np.ndarray` - Image embedding vector

#### `generate_embeddings_batch()`
**Class:** `ImageEmbeddingService`
**Purpose:** Generate embeddings for multiple images
**Parameters:**
- `image_paths: List[str]` - List of image paths
- `batch_size: int = 32` - Batch size for processing
**Returns:** `List[np.ndarray]` - List of embeddings

---

### Image Recommendation Service (`images/image_recommendation_service.py`)

#### `apply_diversity_boosting()`
**Class:** `ImageRecommendationService`
**Purpose:** Apply diversity boosting to prevent near-duplicates
**Parameters:**
- `results: List[Tuple[Image, float]]` - Ranked results
- `max_results: int` - Maximum results to return
- `diversity_threshold: float = 0.95` - Similarity threshold
**Returns:** `List[Tuple[Image, float]]` - Diverse recommendations
**Algorithm:** Greedy selection to ensure results are dissimilar

#### `recommend_by_query()`
**Class:** `ImageRecommendationService`
**Purpose:** Recommend images based on text query
**Parameters:**
- `query: str` - Text description
- `max_results: int = 10` - Maximum results
- `min_similarity: float = 0.7` - Minimum similarity threshold
- `diversity_threshold: float = 0.95` - Diversity threshold
**Returns:** `List[Dict[str, Any]]` - Recommended images
**Example:**
```python
images = await service.recommend_by_query(
    "surgical approach to temporal lobe",
    max_results=10
)
```

#### `recommend_similar_images()`
**Class:** `ImageRecommendationService`
**Purpose:** Recommend images similar to a reference image
**Parameters:**
- `image_id: str` - Reference image ID
- `max_results: int = 10` - Maximum results
- `min_similarity: float = 0.7` - Minimum similarity
- `diversity_threshold: float = 0.95` - Diversity threshold
**Returns:** `List[Dict[str, Any]]` - Similar images with scores
**Example:**
```python
similar = await service.recommend_similar_images(
    image_id=reference_id,
    max_results=5,
    diversity_threshold=0.95
)
```

---

## Phase 5: Section Regeneration

### Section Regenerator (`generation/section_regenerator.py`)

#### `regenerate_chapter()`
**Class:** `SectionRegenerator`
**Purpose:** Regenerate multiple sections in a chapter
**Parameters:**
- `chapter_id: str` - Chapter UUID
- `sections_to_regenerate: Optional[List[str]] = None` - Section IDs (None = all)
**Returns:** `Dict[str, Any]` - Regeneration results for all sections
**Cost Savings:** 84% vs full chapter regeneration

#### `regenerate_section()`
**Class:** `SectionRegenerator`
**Purpose:** Regenerate a single section with AI
**Parameters:**
- `section_id: str` - Section UUID
- `prompt_template: str` - Template for AI prompt
- `research_context: Optional[List[Dict]] = None` - Research articles to incorporate
- `preserve_structure: bool = True` - Maintain original structure
**Returns:** `Dict[str, Any]` - Original and regenerated content
**Example:**
```python
result = await regenerator.regenerate_section(
    section_id="section_123",
    research_context=recent_articles[:3],
    preserve_structure=True
)
# {
#   'section_id': '...',
#   'original_content': '...',
#   'regenerated_content': '...',
#   'changes_summary': '...',
#   'tokens_used': 1240
# }
```

---

### Version Tracker (`generation/version_tracker.py`)

#### `get_version_history()`
**Class:** `VersionTracker`
**Purpose:** Get regeneration history for a section
**Parameters:**
- `section_id: str` - Section UUID
**Returns:** `List[Dict[str, Any]]` - Version history

#### `track_regeneration()`
**Class:** `VersionTracker`
**Purpose:** Track a section regeneration event
**Parameters:**
- `section_id: str` - Section UUID
- `regenerated_content: str` - New content
- `prompt_used: str` - Prompt template used
- `metadata: Dict` - Additional metadata
**Returns:** `str` - Version ID

---

## Phase 6: Multi-Provider AI

### AI Provider Interface (`ai/provider_interface.py`)

#### `generate_completion()`
**Class:** `AIProvider` (abstract)
**Purpose:** Generate text completion
**Parameters:**
- `prompt: str` - Input prompt
- `max_tokens: int` - Maximum tokens to generate
- `temperature: float` - Sampling temperature
- `**kwargs` - Provider-specific parameters
**Returns:** `Dict[str, Any]` - Completion response

#### `generate_embedding()`
**Class:** `AIProvider` (abstract)
**Purpose:** Generate text embedding
**Parameters:**
- `text: str` - Input text
- `**kwargs` - Provider-specific parameters
**Returns:** `Dict[str, Any]` - Embedding response

#### `get_cost_estimate()`
**Class:** `AIProvider` (abstract)
**Purpose:** Estimate cost for an operation
**Parameters:**
- `tokens: int` - Number of tokens
- `operation: str` - Operation type (completion, embedding)
**Returns:** `float` - Estimated cost in USD

---

### Provider Router (`ai/provider_router.py`)

#### `generate_completion_with_fallback()`
**Class:** `ProviderRouter`
**Purpose:** Generate completion with automatic provider fallback
**Parameters:**
- `prompt: str` - Input prompt
- `preferred_provider: str = 'claude'` - Preferred provider
- `fallback_providers: List[str] = ['gpt4', 'gemini']` - Fallback order
- `**kwargs` - Completion parameters
**Returns:** `Dict[str, Any]` - Completion response
**Resilience:** Circuit breaker pattern with automatic failover
**Example:**
```python
response = await router.generate_completion_with_fallback(
    prompt="Generate chapter summary...",
    preferred_provider="claude",
    fallback_providers=["gpt4"]
)
```

#### `get_circuit_breaker_stats()`
**Class:** `ProviderRouter`
**Purpose:** Get circuit breaker status for all providers
**Parameters:** None
**Returns:** `Dict[str, Any]` - Provider health status

#### `route_by_task()`
**Class:** `ProviderRouter`
**Purpose:** Route request to optimal provider based on task type
**Parameters:**
- `task_type: str` - Task type (chapter_generation, search_query, etc.)
- `**kwargs` - Task parameters
**Returns:** Provider instance
**Routing Strategy:**
```python
{
    'chapter_generation': 'claude',
    'search_query': 'gpt4',
    'image_description': 'gpt4-vision',
    'embedding': 'openai-ada',
    'research_summary': 'claude'
}
```

---

## Phase 7: Alive Chapters

### Update Monitor (`alive_chapters/update_monitor.py`)

#### `check_for_updates()`
**Class:** `UpdateMonitor`
**Purpose:** Check if new research is available for a chapter
**Parameters:**
- `chapter_id: str` - Chapter UUID
- `check_interval_days: int = 7` - Days since last check
**Returns:** `Dict[str, Any]` - Update availability and score
**Example:**
```python
updates = await monitor.check_for_updates(chapter_id)
# {
#   'update_available': True,
#   'update_score': 0.85,
#   'new_papers_count': 12,
#   'suggested_sections': ['complications', 'outcomes'],
#   'last_checked': datetime
# }
```

---

### Change Detector (`alive_chapters/change_detector.py`)

#### `detect_outdated_sections()`
**Class:** `ChangeDetector`
**Purpose:** Identify sections that may be outdated
**Parameters:**
- `chapter_id: str` - Chapter UUID
- `recency_threshold_years: int = 5` - Age threshold for sources
**Returns:** `List[Dict[str, Any]]` - Outdated sections with reasons
**Heuristics:**
- References older than threshold
- Contradictory recent evidence
- Deprecated techniques
- Significantly changed statistics

---

### Interaction Logger (`alive_chapters/interaction_logger.py`)

#### `get_popular_chapters()`
**Class:** `InteractionLogger`
**Purpose:** Get most-accessed chapters
**Parameters:**
- `timeframe_days: int = 30` - Timeframe for analysis
- `limit: int = 10` - Maximum results
**Returns:** `List[Dict[str, Any]]` - Popular chapters with metrics

#### `log_chapter_view()`
**Class:** `InteractionLogger`
**Purpose:** Log chapter access
**Parameters:**
- `chapter_id: str` - Chapter UUID
- `user_id: str` - User identifier
- `duration_seconds: int` - View duration
**Returns:** None

#### `log_search_query()`
**Class:** `InteractionLogger`
**Purpose:** Log search interactions
**Parameters:**
- `query: str` - Search query
- `results_count: int` - Number of results
- `clicked_chapter_ids: List[str]` - Chapters clicked
**Returns:** None

---

## Alphabetical Index

### A
- `add_book()` - Phase 1, LibraryManager
- `apply_diversity_boosting()` - Phase 4, ImageRecommendationService

### B
- `build_index()` - Phase 2, BM25SearchEngine

### C
- `calculate_idf()` - Phase 2, BM25SearchEngine
- `calculate_quality_score()` - Phase 4, ImageEmbeddingService
- `check_for_updates()` - Phase 7, UpdateMonitor
- `combine_scores()` - Phase 2, HybridSearchEngine
- `create_all_tables()` - Phase 1, DatabaseManager

### D
- `delete_book()` - Phase 1, LibraryManager
- `detect_chapters()` - Phase 1, PDFIndexer
- `detect_outdated_sections()` - Phase 7, ChangeDetector

### E
- `explain_score()` - Phase 2, HybridSearchEngine
- `extract_chapter_text()` - Phase 1, PDFIndexer
- `extract_images()` - Phase 1, PDFIndexer
- `extract_metadata()` - Phase 1, PDFIndexer

### F
- `fetch_article_details()` - Phase 3, PubMedClient
- `find_similar_chapters()` - Phase 2, SemanticSearchEngine
- `format()` - Phase 0, StructuredFormatter

### G
- `generate_chapter_embeddings()` - Phase 1, PDFIndexer
- `generate_completion()` - Phase 6, AIProvider
- `generate_completion_with_fallback()` - Phase 6, ProviderRouter
- `generate_embedding()` - Phase 4, ImageEmbeddingService
- `generate_embeddings_batch()` - Phase 4, ImageEmbeddingService
- `generate_query_embedding()` - Phase 2, SemanticSearchEngine
- `generate_secure_id()` - Phase 0, SecurityUtils
- `get()` - Phase 3, CacheManager
- `get_book_statistics()` - Phase 1, LibraryManager
- `get_circuit_breaker_stats()` - Phase 6, ProviderRouter
- `get_connection()` - Phase 1, DatabaseManager
- `get_cost_estimate()` - Phase 6, AIProvider
- `get_logger()` - Phase 0, utils.logger
- `get_popular_chapters()` - Phase 7, InteractionLogger
- `get_session()` - Phase 1, DatabaseManager
- `get_settings()` - Phase 0, utils.config
- `get_stats()` - Phase 2, BM25SearchEngine
- `get_stats()` - Phase 3, CacheManager
- `get_version_history()` - Phase 5, VersionTracker

### H
- `hash_password()` - Phase 0, SecurityUtils

### I
- `index_pdf()` - Phase 1, PDFIndexer
- `invalidate()` - Phase 3, CacheManager

### L
- `list_books()` - Phase 1, LibraryManager
- `log_chapter_view()` - Phase 7, InteractionLogger
- `log_search_query()` - Phase 7, InteractionLogger

### P
- `process()` - Phase 0, LoggerAdapter

### R
- `recommend_by_query()` - Phase 4, ImageRecommendationService
- `recommend_similar_images()` - Phase 4, ImageRecommendationService
- `regenerate_chapter()` - Phase 5, SectionRegenerator
- `regenerate_section()` - Phase 5, SectionRegenerator
- `reload_settings()` - Phase 0, utils.config
- `research_topic()` - Phase 3, ResearchOrchestrator
- `route_by_task()` - Phase 6, ProviderRouter

### S
- `sanitize_filename()` - Phase 0, InputValidator
- `sanitize_text()` - Phase 0, InputValidator
- `search()` - Phase 2, BM25SearchEngine
- `search()` - Phase 2, HybridSearchEngine
- `search()` - Phase 2, SemanticSearchEngine
- `search()` - Phase 3, PubMedClient
- `search_batch()` - Phase 3, PubMedClient
- `search_books()` - Phase 1, LibraryManager
- `set()` - Phase 3, CacheManager

### T
- `to_dict()` - Phase 0, NeurosurgicalKBException
- `track_regeneration()` - Phase 5, VersionTracker

### V
- `validate_email()` - Phase 0, InputValidator
- `validate_file_path()` - Phase 0, InputValidator
- `validate_file_size()` - Phase 0, InputValidator
- `validate_float_range()` - Phase 0, InputValidator
- `validate_integer_range()` - Phase 0, InputValidator
- `verify_integrity()` - Phase 1, LibraryManager
- `verify_password()` - Phase 0, SecurityUtils

---

## Summary Statistics

**Total Functions Documented:** 92+
**Phases Covered:** 7 (Phase 0 through Phase 7)
**Core Modules:** 25+
**Lines of Code (Estimated):** ~10,500 when fully implemented

---

## Implementation Status

| Phase | Status | Functions | Completion |
|-------|--------|-----------|------------|
| Phase 0: Foundation | Not Started | 20 | 0% |
| Phase 1: Reference Library | Not Started | 18 | 0% |
| Phase 2: Hybrid Search | Not Started | 10 | 0% |
| Phase 3: Research Integration | Not Started | 10 | 0% |
| Phase 4: Image Recommendations | Not Started | 6 | 0% |
| Phase 5: Section Regeneration | Not Started | 4 | 0% |
| Phase 6: Multi-Provider AI | Not Started | 5 | 0% |
| Phase 7: Alive Chapters | Not Started | 5 | 0% |
| **Total** | **Ready to Start** | **78+** | **0%** |

---

## Next Steps

1. **Start with Phase 0** - Implement foundation utilities (2-3 days)
2. **Verify with tests** - Run test suite after each function
3. **Follow sequential order** - Each phase builds on previous
4. **Track progress** - Update this document as functions are implemented

---

**Document Version:** 1.0
**Last Updated:** 2025-11-05
**Maintained By:** StudyBuddy Development Team
