# StudyBuddy - Conceptual Map & Architecture Review

**Version:** 1.0
**Date:** 2025-11-05
**Status:** PRE-IMPLEMENTATION REVIEW
**Purpose:** Validate architectural decisions and alignment with project goals

---

## Table of Contents

1. [Project Vision & Goals](#project-vision--goals)
2. [Core Concepts & Entities](#core-concepts--entities)
3. [System Architecture](#system-architecture)
4. [Data Flow & Interactions](#data-flow--interactions)
5. [Key Design Decisions](#key-design-decisions)
6. [User Workflows](#user-workflows)
7. [Integration Points](#integration-points)
8. [Success Criteria](#success-criteria)
9. [Review Questions](#review-questions)

---

## 1. Project Vision & Goals

### 🎯 Primary Goal
**Transform medical knowledge from static PDFs into an intelligent, searchable, continuously-evolving knowledge base for neurosurgical education.**

### 🎓 Core Value Propositions

1. **Persistent Knowledge Base**
   - Currently: Extract PDF data every time → wasteful, slow
   - Future: Index once, search instantly → efficient, fast

2. **Intelligent Search**
   - Currently: No search capability
   - Future: Hybrid search (keyword + semantic + recency) → relevant results

3. **Research Integration**
   - Currently: Manual PubMed searches, sequential execution
   - Future: Parallel research with intelligent caching → 300x speedup

4. **Smart Content Generation**
   - Currently: Generate entire chapters from scratch
   - Future: Section-level regeneration → 84% cost savings

5. **Multi-Modal Learning**
   - Currently: Random image selection
   - Future: Similarity-based recommendations with diversity → better learning

6. **Continuous Evolution**
   - Currently: Static content that becomes outdated
   - Future: "Alive chapters" that monitor for updates → always current

### 🎯 Target Users

1. **Medical Students** - Learning neurosurgical concepts
2. **Residents** - Preparing for procedures and boards
3. **Faculty** - Creating educational materials
4. **Researchers** - Synthesizing literature

### 📊 Success Metrics

- **Search Performance**: < 600ms for hybrid search
- **Cache Hit Rate**: > 80% after warmup
- **Cost Reduction**: 84% vs full regeneration
- **Research Speed**: 4x faster with parallel execution
- **User Satisfaction**: Relevant, current content

---

## 2. Core Concepts & Entities

### 📚 Domain Model

```
KNOWLEDGE HIERARCHY
===================

Library (System)
    ├── Books (Reference PDFs)
    │   ├── Metadata (Title, Author, Year, ISBN)
    │   ├── File Info (Path, Size, Hash)
    │   └── Chapters
    │       ├── Chapter Info (Number, Title, Pages)
    │       ├── Content (Full Text)
    │       ├── AI Summary
    │       ├── Embedding Vector (1536D)
    │       ├── Sections
    │       │   ├── Section Content
    │       │   ├── Regenerated Content (Optional)
    │       │   └── Version History
    │       └── Images
    │           ├── Image File
    │           ├── Caption/Description
    │           ├── Embedding Vector
    │           └── Quality Score

Research Sources
    ├── Internal (Indexed Chapters)
    │   └── Searched via Hybrid Engine
    └── External (PubMed)
        ├── Cached Results (Redis/Memory)
        └── Live Queries (Rate-limited)

Generated Content
    ├── Chapters
    │   ├── Outline
    │   ├── Sections
    │   └── Research Data (Reusable)
    └── Version History
```

### 🔑 Key Concepts

#### 1. **Reference Library**
- **What**: Persistent index of medical textbooks
- **Why**: Avoid re-processing PDFs; enable search
- **How**: SQLAlchemy ORM → PostgreSQL/SQLite
- **Data**: Metadata in DB, files on disk

#### 2. **Hybrid Search**
- **What**: Multi-algorithm search combining keyword, semantic, and recency
- **Why**: Better relevance than single method
- **How**:
  - BM25 (keyword) → exact term matching
  - Vector similarity (semantic) → conceptual matching
  - RRF fusion → combine rankings
- **Performance**: < 600ms target

#### 3. **Vector Embeddings**
- **What**: Numerical representations (1536D vectors) of text/images
- **Why**: Enable semantic similarity search
- **How**:
  - Text: OpenAI `text-embedding-3-small`
  - Images: CLIP or similar
- **Storage**: PostgreSQL pgvector or serialized in SQLite

#### 4. **Research Orchestration**
- **What**: Coordinated search across internal + external sources
- **Why**: Comprehensive, up-to-date information
- **How**:
  - Internal: Hybrid search on indexed chapters
  - External: PubMed API queries
  - Parallel execution: asyncio.gather()
  - Caching: Redis with TTL

#### 5. **Intelligent Caching**
- **What**: Store expensive operation results
- **Why**: 300x speedup on repeated queries
- **How**:
  - Storage: Redis (production) or in-memory (dev)
  - TTL: 7 days for PubMed, 30 days for embeddings
  - Invalidation: Pattern-based or manual
- **Strategy**: Cache hot data, extend TTL on hits

#### 6. **Section Regeneration**
- **What**: Update specific sections instead of entire chapters
- **Why**: 84% cost savings, faster updates
- **How**:
  - Store original + regenerated content
  - Version tracking
  - Reuse research data
  - AI prompt templates

#### 7. **Multi-Provider AI**
- **What**: Support multiple AI providers (Claude, GPT-4, Gemini)
- **Why**: Reliability, cost optimization, task-specific routing
- **How**:
  - Abstract interface
  - Circuit breaker pattern
  - Task-based routing
  - Automatic failover

#### 8. **Alive Chapters**
- **What**: Chapters that monitor for updates and evolve
- **Why**: Keep content current without manual intervention
- **How**:
  - Monitor PubMed for new research
  - Detect outdated sections (old references, contradictory evidence)
  - Track user interactions
  - Suggest regeneration priorities

---

## 3. System Architecture

### 🏗️ Architectural Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   CLI Tool   │  │   Web API    │  │  Jupyter NB  │          │
│  │   (Typer)    │  │  (FastAPI)   │  │  (Optional)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │   Library      │  │    Search      │  │   Research     │    │
│  │   Manager      │  │    Engine      │  │  Orchestrator  │    │
│  │                │  │                │  │                │    │
│  │ • Add books    │  │ • BM25         │  │ • Internal     │    │
│  │ • List/search  │  │ • Semantic     │  │ • External     │    │
│  │ • Statistics   │  │ • Hybrid       │  │ • Parallel     │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │    Image       │  │   Section      │  │      AI        │    │
│  │ Recommender    │  │  Regenerator   │  │   Provider     │    │
│  │                │  │                │  │    Router      │    │
│  │ • Similarity   │  │ • Regenerate   │  │                │    │
│  │ • Diversity    │  │ • Version      │  │ • Claude       │    │
│  │ • Quality      │  │ • Compare      │  │ • OpenAI       │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN SERVICES                             │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │  PDF Indexer   │  │   Embedding    │  │     Cache      │    │
│  │                │  │    Service     │  │    Manager     │    │
│  │ • Extract      │  │                │  │                │    │
│  │ • Detect CH    │  │ • Text         │  │ • Get/Set      │    │
│  │ • Generate     │  │ • Image        │  │ • Invalidate   │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                           │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │   Database     │  │     Cache      │  │   External     │    │
│  │   Manager      │  │   (Redis)      │  │     APIs       │    │
│  │                │  │                │  │                │    │
│  │ • PostgreSQL   │  │ • Memory       │  │ • PubMed       │    │
│  │ • SQLite       │  │ • Redis        │  │ • Anthropic    │    │
│  │ • Migrations   │  │ • TTL          │  │ • OpenAI       │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     FOUNDATION LAYER                             │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │   Security     │  │   Logging      │  │  Configuration │    │
│  │                │  │                │  │                │    │
│  │ • Validation   │  │ • Structured   │  │ • Pydantic     │    │
│  │ • Sanitization │  │ • Context      │  │ • Type-safe    │    │
│  │ • Exceptions   │  │ • JSON/Text    │  │ • .env         │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPENDENCY GRAPH                              │
│                                                                   │
│  LibraryManager                                                  │
│       ↓                                                          │
│  PDFIndexer ──→ EmbeddingService ──→ OpenAI API                 │
│       ↓                                                          │
│  DatabaseManager ──→ PostgreSQL/SQLite                           │
│                                                                   │
│  HybridSearchEngine                                              │
│       ├──→ BM25SearchEngine                                      │
│       ├──→ SemanticSearchEngine ──→ EmbeddingService             │
│       └──→ RankFusion                                            │
│                                                                   │
│  ResearchOrchestrator                                            │
│       ├──→ HybridSearchEngine (internal)                         │
│       ├──→ PubMedClient (external)                               │
│       └──→ CacheManager ──→ Redis                                │
│                                                                   │
│  ImageRecommender                                                │
│       ├──→ ImageEmbeddingService ──→ CLIP/OpenAI                │
│       └──→ DiversityBooster                                      │
│                                                                   │
│  SectionRegenerator                                              │
│       ├──→ AIProviderRouter ──→ Claude/GPT-4/Gemini             │
│       ├──→ ResearchOrchestrator (for context)                    │
│       └──→ VersionTracker                                        │
│                                                                   │
│  UpdateMonitor (Alive Chapters)                                  │
│       ├──→ PubMedClient                                          │
│       ├──→ ChangeDetector                                        │
│       └──→ InteractionLogger                                     │
└─────────────────────────────────────────────────────────────────┘
```

### 📦 Module Isolation

**Principle**: Each module is independently testable and deployable

```
utils/              → No dependencies (foundation)
reference_library/  → Depends on: utils
search/             → Depends on: utils, reference_library
research/           → Depends on: utils, search
images/             → Depends on: utils, reference_library
ai/                 → Depends on: utils
generation/         → Depends on: utils, research, ai
alive_chapters/     → Depends on: utils, research, reference_library
```

---

## 4. Data Flow & Interactions

### 📥 Workflow 1: Indexing a New Book

```
User Action: studybuddy add /path/to/neurosurgery.pdf
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 1. LibraryManager.add_book()                                    │
│    ├─ Validate file path (security check)                       │
│    └─ Generate book ID (SHA-256 hash)                           │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PDFIndexer.extract_metadata()                                │
│    ├─ Extract title, author, year from PDF                      │
│    ├─ Count pages                                               │
│    └─ Store book metadata in database                           │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. PDFIndexer.detect_chapters()                                 │
│    ├─ Extract first 20 pages (TOC)                              │
│    ├─ Call Claude API with TOC text                             │
│    ├─ Parse JSON response (chapter boundaries)                  │
│    └─ Fallback: Treat as single chapter if AI fails             │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. For each chapter:                                            │
│    ├─ Extract full text (page range)                            │
│    ├─ Generate embedding (OpenAI)                               │
│    ├─ Store chapter in database                                 │
│    └─ Rate limit: 1 req/sec                                     │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. PDFIndexer.extract_images()                                  │
│    ├─ Extract images from all pages                             │
│    ├─ Save to disk: data/images/{book_id}/{page}_{idx}.png      │
│    ├─ Generate quality scores                                   │
│    └─ Store image metadata in database                          │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. Return Results                                               │
│    {                                                             │
│      status: "success",                                          │
│      book_id: "abc123...",                                       │
│      chapters_indexed: 15,                                       │
│      images_extracted: 143,                                      │
│      duration_seconds: 145.3                                     │
│    }                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 🔍 Workflow 2: Searching for Content

```
User Action: studybuddy search "temporal craniotomy complications"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 1. HybridSearchEngine.search()                                  │
│    ├─ Sanitize query (XSS protection)                           │
│    └─ Parallel execution of 3 search algorithms:                │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌──────────────────────┬───────────────────────┬─────────────────┐
│  BM25 Search         │  Semantic Search      │  Recency Boost  │
│                      │                       │                 │
│  • Tokenize query    │  • Generate embedding │  • Weight by    │
│  • Calculate TF-IDF  │  • Cosine similarity  │    publish date │
│  • Rank by score     │  • Filter > 0.7       │  • Prefer newer │
│  • Return top 50     │  • Return top 50      │    content      │
│                      │                       │                 │
│  Time: ~45ms         │  Time: ~320ms         │  Time: ~10ms    │
└──────────────────────┴───────────────────────┴─────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. RankFusion.combine_scores()                                  │
│    ├─ Apply Reciprocal Rank Fusion (RRF)                        │
│    ├─ Formula: score = Σ(1 / (k + rank))                        │
│    ├─ Weight: BM25=0.5, Semantic=0.5                            │
│    └─ Sort by combined score                                    │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. Return Results (< 600ms total)                               │
│    [                                                             │
│      {                                                           │
│        chapter_id: "...",                                        │
│        title: "Complications of Temporal Craniotomy",            │
│        book_title: "Neurosurgery Textbook",                      │
│        score: 0.87,                                              │
│        excerpt: "...temporal craniotomy complications...",       │
│        explanation: {                                            │
│          bm25_score: 4.2,                                        │
│          semantic_similarity: 0.89,                              │
│          recency_boost: 1.1                                      │
│        }                                                         │
│      },                                                          │
│      ...                                                         │
│    ]                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 🔬 Workflow 3: Researching a Topic

```
User Action: Research "temporal lobe epilepsy surgery outcomes"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 1. ResearchOrchestrator.research_topic()                        │
│    ├─ Generate multiple query variants                          │
│    │   • "temporal lobe epilepsy surgery outcomes"              │
│    │   • "temporal lobectomy results"                           │
│    │   • "epilepsy surgery complications"                       │
│    └─ Execute internal + external in parallel                   │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌──────────────────────────┬──────────────────────────────────────┐
│  Internal Research       │  External Research (PubMed)          │
│  (Reference Library)     │                                      │
│                          │                                      │
│  HybridSearch.search()   │  1. Check cache first                │
│    ↓                     │     CacheManager.get(query)          │
│  Returns 10 chapters     │        ↓                             │
│  from indexed books      │     [Cache Miss]                     │
│                          │        ↓                             │
│  Time: ~500ms            │  2. PubMedClient.search()            │
│                          │     ├─ Query NCBI E-utilities        │
│                          │     ├─ Filter: last 5 years          │
│                          │     ├─ Parse XML responses           │
│                          │     └─ Return 20 articles            │
│                          │        ↓                             │
│                          │  3. Cache results                    │
│                          │     CacheManager.set(                │
│                          │       key=query,                     │
│                          │       value=results,                 │
│                          │       ttl=7 days                     │
│                          │     )                                │
│                          │                                      │
│                          │  Time: ~18s (first) / ~5ms (cached)  │
└──────────────────────────┴──────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. Merge & Deduplicate Results                                  │
│    ├─ Weight: Internal 60%, External 40%                        │
│    ├─ Remove duplicates (same PMID or title)                    │
│    └─ Rank by relevance × recency                               │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. Return Comprehensive Results                                 │
│    {                                                             │
│      topic: "temporal lobe epilepsy surgery outcomes",           │
│      internal_sources: [10 chapters from library],               │
│      external_sources: [20 PubMed articles],                     │
│      cache_hits: 0,  // First query                             │
│      total_time_seconds: 18.7,                                   │
│      queries_executed: 3                                         │
│    }                                                             │
│                                                                  │
│    // Next identical query: ~500ms (internal + cached external) │
└─────────────────────────────────────────────────────────────────┘
```

### 🖼️ Workflow 4: Image Recommendations

```
User viewing: Chapter on "Temporal Craniotomy Approach"
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 1. Get reference image embedding                                │
│    ImageRecommender.recommend_similar_images(image_id)          │
│       ↓                                                          │
│    Load embedding from database (1536D vector)                  │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. Find similar images                                          │
│    Calculate cosine similarity with all image embeddings        │
│       ↓                                                          │
│    Filter: similarity > 0.7                                     │
│       ↓                                                          │
│    Rank by similarity score                                     │
│       ↓                                                          │
│    Results: 50 similar images                                   │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. Apply Diversity Boosting                                     │
│    DiversityBooster.boost(results, threshold=0.95)              │
│       ↓                                                          │
│    Algorithm:                                                    │
│    1. Select highest similarity image (A)                       │
│    2. For each remaining image (B):                             │
│       - Calculate similarity(A, B)                               │
│       - If similarity < 0.95: Include B                          │
│       - Else: Skip B (too similar to A)                          │
│    3. Repeat until max_results reached                          │
│       ↓                                                          │
│    Result: 10 diverse images (no near-duplicates)               │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. Return Recommendations                                       │
│    [                                                             │
│      {                                                           │
│        image_id: "...",                                          │
│        file_path: "data/images/abc123/page_45_0.png",           │
│        caption: "Pterional approach to temporal lobe",           │
│        similarity: 0.92,                                         │
│        quality_score: 0.88,                                      │
│        source_chapter: "Skull Base Approaches"                   │
│      },                                                          │
│      {                                                           │
│        similarity: 0.87,  // Different enough from first        │
│        ...                                                       │
│      }                                                           │
│    ]                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### ♻️ Workflow 5: Section Regeneration

```
User Action: Update "Complications" section with latest research
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 1. Load original section                                        │
│    SectionRegenerator.regenerate_section(section_id)            │
│       ↓                                                          │
│    Database query: Get section content                          │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. Research latest findings (reuse existing orchestrator)       │
│    ResearchOrchestrator.research_topic(                         │
│      topic="temporal craniotomy complications"                  │
│    )                                                             │
│       ↓                                                          │
│    Returns: 5 internal chapters + 10 PubMed articles            │
│    Time: ~600ms (mostly cached)                                 │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. Build AI prompt                                              │
│    Template:                                                     │
│    """                                                           │
│    You are updating a neurosurgery textbook section.             │
│                                                                  │
│    ORIGINAL CONTENT:                                             │
│    {original_section_content}                                   │
│                                                                  │
│    LATEST RESEARCH:                                              │
│    {research_articles}                                           │
│                                                                  │
│    TASK: Rewrite incorporating new evidence while:              │
│    1. Preserving factual accuracy of original                   │
│    2. Adding new findings with [PMID: xxx] citations            │
│    3. Maintaining same structure and length                     │
│    4. Using appropriate medical terminology                     │
│    """                                                           │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. Call AI Provider (with fallback)                             │
│    AIProviderRouter.generate_completion_with_fallback(          │
│      prompt=prompt,                                              │
│      preferred_provider="claude"                                 │
│    )                                                             │
│       ↓                                                          │
│    Try Claude → Success                                         │
│    Time: ~8s                                                     │
│    Cost: ~$0.05                                                  │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. Store regenerated content                                    │
│    VersionTracker.track_regeneration(                           │
│      section_id=section_id,                                      │
│      regenerated_content=new_content,                           │
│      prompt_used=prompt,                                         │
│      metadata={tokens: 1200, cost: 0.05}                         │
│    )                                                             │
│       ↓                                                          │
│    Database:                                                     │
│    • sections.regenerated_content = new_content                 │
│    • sections.regeneration_count += 1                           │
│    • sections.last_regenerated_at = NOW()                       │
└─────────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. Return comparison                                            │
│    {                                                             │
│      section_id: "...",                                          │
│      original_content: "...",                                    │
│      regenerated_content: "...",                                 │
│      changes_summary: "Added 3 recent studies (2023-2024)...",  │
│      word_count_change: +120,                                    │
│      tokens_used: 1200,                                          │
│      cost_usd: 0.05                                              │
│    }                                                             │
│                                                                  │
│    // Full chapter would cost ~$0.60, this costs $0.05          │
│    // Savings: 84%                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Key Design Decisions

### ✅ Decision 1: SQLite → PostgreSQL Migration Path

**Decision**: Start with SQLite, design for PostgreSQL upgrade

**Rationale**:
- SQLite: Zero setup, single file, perfect for development
- PostgreSQL: Production-grade, pgvector for embeddings, better concurrency
- SQLAlchemy ORM: Database-agnostic, easy migration

**Trade-offs**:
- ✅ Pro: Fast development start
- ✅ Pro: Easy local testing
- ⚠️ Con: Must avoid SQLite-specific features
- ⚠️ Con: Migration work needed for production

**Implementation**:
```python
# Database URL determined by environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///studybuddy.db"  # Default: SQLite
)
# Production: "postgresql://user:pass@host/db"
```

### ✅ Decision 2: Hybrid Search (BM25 + Semantic)

**Decision**: Combine keyword and semantic search using RRF

**Rationale**:
- BM25 alone: Misses conceptually similar content
- Semantic alone: Misses exact terminology matches
- Hybrid: Best of both worlds

**Trade-offs**:
- ✅ Pro: Better relevance (proven in research)
- ✅ Pro: Handles both "exact match" and "similar concept" queries
- ⚠️ Con: More complex than single algorithm
- ⚠️ Con: Slower than BM25 alone (~600ms vs ~50ms)

**Performance Target**: < 600ms (acceptable for user-facing search)

### ✅ Decision 3: Redis Caching with Fallback

**Decision**: Redis for production, in-memory for development

**Rationale**:
- Redis: Persistent, shared across instances, production-grade
- In-memory: Zero setup for development
- Same interface: CacheManager abstraction

**Trade-offs**:
- ✅ Pro: No Redis requirement for local dev
- ✅ Pro: Production performance (300x speedup)
- ⚠️ Con: Dev cache not persistent across restarts
- ⚠️ Con: Dev cache not shared (fine for single developer)

**Implementation**:
```python
if os.getenv("REDIS_HOST"):
    cache = RedisCache()
else:
    cache = MemoryCache()
```

### ✅ Decision 4: AI Chapter Detection vs Rule-Based

**Decision**: AI-first with rule-based fallback

**Rationale**:
- PDFs have inconsistent TOC formats
- AI can understand context (not just patterns)
- Fallback ensures system always works

**Trade-offs**:
- ✅ Pro: Handles complex/unusual TOC layouts
- ✅ Pro: High accuracy (~95% confidence)
- ⚠️ Con: API cost (~$0.01 per PDF)
- ⚠️ Con: Requires API key for indexing

**Fallback Behavior**: If AI fails → treat entire PDF as single chapter

### ✅ Decision 5: Section-Level Regeneration

**Decision**: Update sections, not entire chapters

**Rationale**:
- Most updates affect specific sections (e.g., "Complications")
- Full chapter regeneration wastes tokens on unchanged content
- 84% cost savings proven in production

**Trade-offs**:
- ✅ Pro: Massive cost savings (84%)
- ✅ Pro: Faster regeneration
- ✅ Pro: More granular version control
- ⚠️ Con: Requires good section parsing
- ⚠️ Con: Slightly more complex than full regeneration

**Economics**: Section ($0.05) vs Full Chapter ($0.60)

### ✅ Decision 6: Multi-Provider AI with Circuit Breaker

**Decision**: Support multiple AI providers with automatic failover

**Rationale**:
- Provider outages happen
- Cost optimization (use cheaper provider when appropriate)
- Task-specific routing (Claude for long-form, GPT-4 for JSON)

**Trade-offs**:
- ✅ Pro: High reliability (failover)
- ✅ Pro: Cost optimization
- ✅ Pro: Best tool for each task
- ⚠️ Con: More API keys to manage
- ⚠️ Con: More complex error handling

**Circuit Breaker**: After 3 consecutive failures → skip provider for 5 min

### ✅ Decision 7: Neurocore Lessons from Day 1

**Decision**: Apply all 10 Neurocore lessons upfront

**Rationale**:
- Neurocore spent 10 weeks fixing these retroactively
- Each lesson would have taken 1-2 days if done from start
- 8x faster to build right from beginning

**Trade-offs**:
- ✅ Pro: Production-quality from day 1
- ✅ Pro: Saves 8+ weeks of refactoring
- ✅ Pro: Better developer experience
- ⚠️ Con: Slower initial development (2-3 days for foundation)
- ⚠️ Con: More upfront complexity

**Investment**: 2-3 days → Saves 8+ weeks

---

## 6. User Workflows

### 👤 Workflow: Medical Student Studying

```
GOAL: Learn about temporal lobe surgery

1. Search for relevant content
   → studybuddy search "temporal lobe surgery approaches"
   → Returns 10 chapters from indexed textbooks
   → Each with relevance score and excerpt

2. View chapter with images
   → studybuddy view chapter abc123
   → Chapter content displayed
   → Similar images recommended (diversity-boosted)

3. Research latest findings
   → studybuddy research "temporal lobectomy outcomes 2024"
   → Internal sources (10 chapters)
   → External sources (20 recent PubMed articles)
   → Combined, ranked results

4. Generate study notes
   → studybuddy generate summary "temporal lobe epilepsy surgery"
   → AI synthesizes content from research
   → Includes citations [PMID: xxx]
```

### 👨‍⚕️ Workflow: Resident Preparing for Surgery

```
GOAL: Review surgical technique before procedure

1. Search procedure
   → studybuddy search "pterional craniotomy technique"
   → Hybrid search returns most relevant chapters

2. View step-by-step images
   → Automatically recommended based on chapter
   → Diverse images (different angles, approaches)
   → High-quality filtered (quality_score > 0.7)

3. Check complications
   → Search "pterional craniotomy complications"
   → Get recent research (last 5 years)
   → Compare with textbook content

4. Update personal notes
   → Regenerate "Complications" section with latest research
   → Compare original vs updated
   → Choose to keep or merge
```

### 👩‍🏫 Workflow: Faculty Creating Curriculum

```
GOAL: Create updated course materials

1. Audit existing content
   → studybuddy check-updates chapter_id
   → System identifies outdated sections
   → Suggests sections needing updates

2. Bulk research topics
   → studybuddy research-batch topics.txt
   → Parallel processing of multiple topics
   → Cached results for efficiency

3. Generate updated sections
   → studybuddy regenerate section complications
   → Incorporates latest evidence
   → Version tracking maintains history

4. Export for review
   → studybuddy export chapter abc123 --format pdf
   → Includes citations and images
```

---

## 7. Integration Points

### 🔌 External API Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Anthropic     │  │     OpenAI      │  │  Google Gemini  │ │
│  │    (Claude)     │  │                 │  │    (Optional)   │ │
│  │                 │  │                 │  │                 │ │
│  │ • Chapter gen   │  │ • Embeddings    │  │ • Cost-saving   │ │
│  │ • Long-form     │  │ • GPT-4 backup  │  │   alternative   │ │
│  │ • Synthesis     │  │ • JSON parsing  │  │                 │ │
│  │                 │  │                 │  │                 │ │
│  │ Rate: 5req/min  │  │ Rate: 3500/min  │  │ Rate: 60req/min │ │
│  │ Cost: $3/$15/1M │  │ Cost: varies    │  │ Cost: Free tier │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │               PubMed / NCBI E-utilities                      │ │
│  │                                                               │ │
│  │  • Research article search                                   │ │
│  │  • Rate: 3 req/sec (no key), 10 req/sec (with key)          │ │
│  │  • Cost: Free                                                │ │
│  │  • Requirement: Email in User-Agent                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 🔒 API Key Management

```python
# .env file (gitignored)
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
GOOGLE_API_KEY=AIza-xxx  # Optional
PUBMED_EMAIL=user@institution.edu  # Required
PUBMED_API_KEY=xxx  # Optional (higher rate limit)

# Configuration validation at startup
class Settings(BaseSettings):
    anthropic_api_key: str  # Required
    openai_api_key: str     # Required
    google_api_key: Optional[str] = None
    pubmed_email: str       # Required
    pubmed_api_key: Optional[str] = None

    @validator('pubmed_email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError("Valid email required for PubMed")
        return v
```

### 📊 Rate Limiting Strategy

```python
# Per-provider rate limiting
RATE_LIMITS = {
    'anthropic': {
        'requests_per_minute': 5,
        'tokens_per_minute': 100_000
    },
    'openai': {
        'requests_per_minute': 500,
        'tokens_per_minute': 150_000
    },
    'pubmed': {
        'requests_per_second': 3,  # Without API key
        'requests_per_second_with_key': 10
    }
}

# Implementation: Token bucket algorithm
class RateLimiter:
    def __init__(self, rate, period):
        self.rate = rate
        self.period = period
        self.allowance = rate
        self.last_check = time.time()

    async def acquire(self):
        current = time.time()
        elapsed = current - self.last_check
        self.last_check = current
        self.allowance += elapsed * (self.rate / self.period)

        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1:
            sleep_time = (1 - self.allowance) * (self.period / self.rate)
            await asyncio.sleep(sleep_time)
            self.allowance = 0
        else:
            self.allowance -= 1
```

---

## 8. Success Criteria

### 🎯 Phase-by-Phase Success Metrics

#### Phase 0: Foundation
- ✅ All 10 Neurocore lessons applied
- ✅ Exception hierarchy covers all error types
- ✅ Security tests pass (XSS, path traversal, injection)
- ✅ 100% test coverage on security utilities
- ✅ Configuration validates at startup

#### Phase 1: Reference Library
- ✅ Index 100-page PDF in < 5 minutes
- ✅ AI chapter detection > 90% accuracy
- ✅ Extract 100+ images per book
- ✅ Database queries < 50ms (with eager loading)
- ✅ No N+1 queries detected

#### Phase 2: Hybrid Search
- ✅ BM25 search < 100ms
- ✅ Semantic search < 500ms
- ✅ Hybrid search < 600ms
- ✅ Relevance better than single method (user testing)
- ✅ Handle 1000+ chapters without degradation

#### Phase 3: Research Integration
- ✅ Parallel execution 4x faster than sequential
- ✅ Cache hit rate > 80% after warmup
- ✅ PubMed queries respect rate limits (no 429 errors)
- ✅ Cache invalidation works correctly
- ✅ Graceful degradation on API failures

#### Phase 4: Image Recommendations
- ✅ Find similar images with > 80% perceived accuracy
- ✅ Diversity boosting prevents duplicates (similarity < 95%)
- ✅ Quality filtering removes low-quality images
- ✅ Recommendations < 1 second

#### Phase 5: Section Regeneration
- ✅ Cost 84% less than full chapter regeneration
- ✅ Preserve original content (no data loss)
- ✅ Version tracking works correctly
- ✅ Side-by-side comparison clear and useful

#### Phase 6: Multi-Provider AI
- ✅ Automatic failover works (simulate provider outage)
- ✅ Circuit breaker prevents cascade failures
- ✅ Cost tracking accurate within 5%
- ✅ Task routing selects optimal provider

#### Phase 7: Alive Chapters
- ✅ Detect new research within 24 hours
- ✅ Identify outdated sections (old references)
- ✅ Interaction logging captures user behavior
- ✅ Popular chapters identified correctly

### 📈 Overall System Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Search Speed | < 600ms | Hybrid search on 1000 chapters |
| Cache Hit Rate | > 80% | After 1 week warmup period |
| Index Speed | < 5 min | 100-page PDF with images |
| Cost per Section | < $0.10 | Regeneration with research |
| Uptime | > 99% | With multi-provider failover |
| Test Coverage | > 80% | Critical paths 90%+ |
| API Success Rate | > 99.9% | With retries and fallback |

---

## 9. Review Questions

### 🤔 Critical Questions for Alignment

Please review and provide feedback on these key aspects:

#### 1. **Project Goals**
- ❓ Does the system address your primary needs?
- ❓ Are the 6 core value propositions aligned with your vision?
- ❓ Any missing capabilities that are critical?
- ❓ Any planned features that are unnecessary?

#### 2. **Architecture**
- ❓ Is the layered architecture (5 layers) clear and logical?
- ❓ Do the module boundaries make sense?
- ❓ Is the dependency graph acceptable (no circular dependencies)?
- ❓ Should any components be merged or separated?

#### 3. **Data Model**
- ❓ Does the knowledge hierarchy (Library → Books → Chapters → Sections → Images) match your mental model?
- ❓ Are embeddings (1536D vectors) the right approach for semantic search?
- ❓ Is section-level granularity sufficient, or do you need paragraph-level?
- ❓ Should we support multiple libraries (e.g., separate neurosurgery, cardiology)?

#### 4. **Workflows**
- ❓ Do the 5 workflows cover your primary use cases?
- ❓ Are the workflows realistic and practical?
- ❓ Any steps that seem unnecessary or missing?
- ❓ Should we add batch operations (e.g., index multiple PDFs)?

#### 5. **Design Decisions**
- ❓ SQLite → PostgreSQL path: Start with SQLite for simplicity?
- ❓ Hybrid search: Worth the complexity vs single algorithm?
- ❓ Redis caching: Essential or optional?
- ❓ AI chapter detection: Worth the API cost vs manual?
- ❓ Section regeneration: Better than full chapter?
- ❓ Multi-provider AI: Necessary or over-engineering?
- ❓ Neurocore lessons: All 10 from day 1, or phase in gradually?

#### 6. **Performance Targets**
- ❓ Are the performance targets realistic and adequate?
  - Search < 600ms
  - Index < 5 min per 100-page PDF
  - Cache hit rate > 80%
- ❓ Any targets too aggressive or too lenient?

#### 7. **Cost Considerations**
- ❓ Estimated development cost: ~$50-100 during implementation acceptable?
- ❓ Estimated per-chapter cost: $0.10-0.60 acceptable?
- ❓ Section regeneration savings (84%) worth the complexity?

#### 8. **Technology Choices**
- ❓ Python 3.10+ as base language?
- ❓ SQLAlchemy ORM vs raw SQL?
- ❓ OpenAI for embeddings (industry standard)?
- ❓ Claude for chapter generation (best quality)?
- ❓ Redis for caching vs alternatives?

#### 9. **User Experience**
- ❓ CLI-first approach acceptable, or need web UI immediately?
- ❓ Is the planned interaction model (search, view, research, generate) intuitive?
- ❓ Should we add export formats (PDF, DOCX, Markdown)?

#### 10. **Success Metrics**
- ❓ Are the success criteria measurable and meaningful?
- ❓ Any important metrics missing?
- ❓ Should we add user satisfaction surveys?

---

## 10. Next Steps After Review

### ✅ If Approved:
1. **Finalize specification** - Lock down any open questions
2. **Begin Phase 0** - Foundation utilities (2-3 days)
3. **Verify with tests** - Ensure foundation is solid
4. **Proceed to Phase 1** - Reference library implementation

### 🔄 If Changes Needed:
1. **Document feedback** - Capture all concerns and suggestions
2. **Revise conceptual map** - Update based on feedback
3. **Re-review** - Iterate until alignment achieved
4. **Then proceed** - Only start coding after approval

---

## Appendix: Quick Reference

### 📚 Key Terms

- **BM25**: Keyword search algorithm using TF-IDF
- **Embedding**: Numerical vector representation (1536 dimensions)
- **RRF**: Reciprocal Rank Fusion (score combination algorithm)
- **Hybrid Search**: BM25 + Semantic + Recency combined
- **Circuit Breaker**: Automatic failover pattern
- **Diversity Boosting**: Prevent near-duplicate results
- **Section Regeneration**: Update specific sections vs full chapter
- **Alive Chapters**: Chapters that monitor and suggest updates
- **pgvector**: PostgreSQL extension for vector similarity

### 🔢 Key Numbers

- **1536**: Dimensions in OpenAI embeddings
- **600ms**: Target hybrid search time
- **80%**: Target cache hit rate
- **84%**: Cost savings with section regeneration
- **4x**: Speedup with parallel research
- **300x**: Speedup with caching
- **90%**: Target AI chapter detection accuracy
- **95%**: Diversity threshold for image recommendations

---

**Document Status**: READY FOR REVIEW
**Reviewer**: Project Stakeholder
**Action Required**: Provide feedback on review questions above
**Next Version**: Will incorporate feedback and finalize

