# LLM vs Traditional Code: Side-by-Side Implementation Examples

**Purpose:** Concrete code examples comparing LLM-driven vs traditional approaches

---

## Example 1: Search Functionality

### Scenario
User searches for: "temporal craniotomy surgical approach"

### LLM-Driven Approach

```python
"""
LLM-driven search implementation
"""
import anthropic
from typing import List, Dict
import json

class LLMSearch:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def search(self, query: str, documents: List[Dict]) -> List[Dict]:
        """
        Use LLM to search and rank documents
        """
        # Prepare document data for LLM
        doc_text = json.dumps(documents, indent=2)
        
        prompt = f"""You are a medical search engine. Given the following query and documents, 
        return the most relevant documents ranked by relevance.

Query: {query}

Documents:
{doc_text}

Instructions:
1. Analyze the query for medical context
2. Rank documents by relevance considering:
   - Exact keyword matches
   - Semantic similarity
   - Medical accuracy
   - Recency
3. Return a JSON array of document IDs in order of relevance

Format: {{"results": [doc_id1, doc_id2, ...]}}
"""
        
        # Call LLM
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        result = json.loads(response.content[0].text)
        
        # Map IDs back to documents
        ranked_docs = []
        for doc_id in result["results"]:
            doc = next((d for d in documents if d["id"] == doc_id), None)
            if doc:
                ranked_docs.append(doc)
        
        return ranked_docs

# Usage
searcher = LLMSearch(api_key="sk-...")
results = searcher.search(
    "temporal craniotomy surgical approach",
    documents=[
        {"id": 1, "title": "Temporal Craniotomy Techniques", "content": "..."},
        {"id": 2, "title": "Surgical Approaches to Brain", "content": "..."},
        # ... potentially hundreds of documents
    ]
)

# Performance:
# - Latency: 2-5 seconds
# - Cost: $0.05-0.10 per search
# - Accuracy: High (good semantic understanding)
# - Determinism: Low (results vary between runs)
# - Debuggability: Low (black box)
# - Context Limit: ~200 documents max
```

### Traditional Approach (Current StudyBuddy Architecture)

```python
"""
Traditional hybrid search implementation
Combines BM25 keyword search + semantic vector search
"""
from typing import List, Dict, Optional
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import faiss

class HybridSearch:
    def __init__(self, documents: List[Dict]):
        self.documents = documents
        
        # BM25 keyword index
        self.corpus = [doc["content"] for doc in documents]
        self.tokenized_corpus = [doc.split() for doc in self.corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        
        # Semantic vector index
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = self.encoder.encode(self.corpus)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Hybrid search combining BM25 and semantic search
        """
        # BM25 keyword search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_top_k = np.argsort(bm25_scores)[-top_k:][::-1]
        
        # Semantic search
        query_embedding = self.encoder.encode([query])
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            top_k
        )
        semantic_top_k = indices[0]
        
        # Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        k = 60  # RRF parameter
        
        for rank, idx in enumerate(bm25_top_k):
            rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank + 1)
        
        for rank, idx in enumerate(semantic_top_k):
            rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (k + rank + 1)
        
        # Sort by RRF score
        ranked_indices = sorted(
            rrf_scores.keys(), 
            key=lambda x: rrf_scores[x], 
            reverse=True
        )[:top_k]
        
        return [self.documents[i] for i in ranked_indices]

# Usage
searcher = HybridSearch(documents=[
    {"id": 1, "title": "Temporal Craniotomy Techniques", "content": "..."},
    {"id": 2, "title": "Surgical Approaches to Brain", "content": "..."},
    # ... thousands of documents supported
])

results = searcher.search("temporal craniotomy surgical approach")

# Performance:
# - Latency: 45-480ms (10-100x faster)
# - Cost: $0 (after initial embedding generation)
# - Accuracy: High (proven algorithms)
# - Determinism: 100% (same query = same results)
# - Debuggability: High (can trace each component)
# - Context Limit: Unlimited (scales to millions of documents)
```

### Comparison

| Metric | LLM Approach | Traditional Approach | Winner |
|--------|--------------|---------------------|--------|
| **Latency** | 2-5 seconds | 45-480ms | ✅ Traditional (10x faster) |
| **Cost per Search** | $0.05-0.10 | $0 | ✅ Traditional |
| **Monthly Cost (1000 searches/day)** | $1,500-3,000 | $0 | ✅ Traditional |
| **Accuracy** | High | High | 🟡 Tie |
| **Determinism** | No | Yes | ✅ Traditional |
| **Debuggability** | Low | High | ✅ Traditional |
| **Scale Limit** | ~200 docs | Millions | ✅ Traditional |
| **Testing** | Difficult | Easy | ✅ Traditional |
| **NLP Understanding** | Excellent | Good | ✅ LLM |
| **Setup Complexity** | Low | Medium | ✅ LLM |

**Recommendation:** Traditional approach (current architecture) ✅

---

## Example 2: Content Generation

### Scenario
Generate a chapter section on "Temporal Lobe Epilepsy Surgery"

### LLM-Driven Approach (Current Architecture) ✅

```python
"""
LLM-driven content generation
"""
import anthropic
from typing import List, Dict

class ContentGenerator:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_section(
        self, 
        topic: str, 
        research_papers: List[Dict],
        style_guide: str = "formal medical textbook"
    ) -> str:
        """
        Generate a comprehensive section using LLM
        """
        # Prepare research context
        research_context = "\n\n".join([
            f"Study: {p['title']}\n"
            f"Authors: {p['authors']}\n"
            f"Year: {p['year']}\n"
            f"Abstract: {p['abstract']}\n"
            f"Key Findings: {p['findings']}"
            for p in research_papers
        ])
        
        prompt = f"""You are a neurosurgical textbook author. Generate a comprehensive 
section on the following topic, incorporating the latest research.

Topic: {topic}

Recent Research:
{research_context}

Requirements:
1. Write in {style_guide} style
2. Include relevant anatomy
3. Describe surgical techniques with precision
4. Cite research papers appropriately
5. Discuss complications and outcomes
6. Include evidence-based recommendations
7. Length: 1500-2000 words

Format with proper markdown headers and structure.
"""
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            temperature=0.3,  # Lower temperature for factual content
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text

# Usage
generator = ContentGenerator(api_key="sk-...")
section = generator.generate_section(
    topic="Temporal Lobe Epilepsy Surgery: Selective Amygdalohippocampectomy",
    research_papers=[
        {
            "title": "Long-term outcomes of selective amygdalohippocampectomy",
            "authors": "Smith et al.",
            "year": 2023,
            "abstract": "...",
            "findings": "..."
        },
        # ... more papers
    ]
)

# Performance:
# - Latency: 10-30 seconds (acceptable for on-demand generation)
# - Cost: $0.50-1.00 per section
# - Quality: Excellent (coherent, well-structured)
# - Determinism: Low (each generation slightly different)
# - Value: HIGH - would take hours to write manually
```

### Traditional Approach (Template-Based)

```python
"""
Traditional template-based content generation
"""
from typing import List, Dict
import re

class TemplateGenerator:
    def __init__(self):
        self.template = """
# {topic}

## Anatomical Considerations

{anatomy_section}

## Surgical Technique

{technique_section}

## Outcomes

{outcomes_section}

## Complications

{complications_section}

## References

{references_section}
"""
    
    def generate_section(
        self, 
        topic: str, 
        research_papers: List[Dict]
    ) -> str:
        """
        Generate section using templates and extracted data
        """
        # Extract relevant information
        anatomy = self._extract_anatomy(research_papers)
        technique = self._extract_technique(research_papers)
        outcomes = self._extract_outcomes(research_papers)
        complications = self._extract_complications(research_papers)
        references = self._format_references(research_papers)
        
        return self.template.format(
            topic=topic,
            anatomy_section=anatomy,
            technique_section=technique,
            outcomes_section=outcomes,
            complications_section=complications,
            references_section=references
        )
    
    def _extract_anatomy(self, papers: List[Dict]) -> str:
        """Extract anatomical descriptions"""
        # Simple keyword extraction
        anatomy_keywords = ["anatomy", "structure", "location", "hippocampus", "amygdala"]
        relevant = []
        
        for paper in papers:
            text = paper["abstract"]
            for keyword in anatomy_keywords:
                if keyword in text.lower():
                    relevant.append(text)
                    break
        
        return "\n\n".join(relevant)
    
    def _extract_technique(self, papers: List[Dict]) -> str:
        """Extract surgical techniques"""
        # ... similar keyword extraction
        pass
    
    def _extract_outcomes(self, papers: List[Dict]) -> str:
        """Extract outcome data"""
        # ... similar extraction
        pass
    
    def _extract_complications(self, papers: List[Dict]) -> str:
        """Extract complication data"""
        # ... similar extraction
        pass
    
    def _format_references(self, papers: List[Dict]) -> str:
        """Format reference list"""
        return "\n".join([
            f"[{i+1}] {p['authors']} ({p['year']}). {p['title']}. {p['journal']}."
            for i, p in enumerate(papers)
        ])

# Usage
generator = TemplateGenerator()
section = generator.generate_section(
    topic="Temporal Lobe Epilepsy Surgery",
    research_papers=[...]
)

# Performance:
# - Latency: 50-200ms (fast)
# - Cost: $0
# - Quality: Poor (choppy, lacks coherence, just extracted quotes)
# - Determinism: 100%
# - Value: LOW - not readable as a textbook section
```

### Comparison

| Metric | LLM Approach | Traditional Approach | Winner |
|--------|--------------|---------------------|--------|
| **Latency** | 10-30 seconds | 50-200ms | ✅ Traditional |
| **Cost per Section** | $0.50-1.00 | $0 | ✅ Traditional |
| **Quality** | Excellent | Poor | ✅ LLM |
| **Coherence** | High | Low | ✅ LLM |
| **Readability** | High | Low | ✅ LLM |
| **Manual Effort Saved** | 2-3 hours | 0 hours | ✅ LLM |
| **Value** | Very High | Low | ✅ LLM |
| **Frequency** | Low (on-demand) | - | ✅ LLM |

**Recommendation:** LLM approach (current architecture) ✅

**Rationale:** This is exactly what LLMs excel at - creative content generation. 
The traditional approach cannot produce readable, coherent text. The cost ($0.50-1.00) 
is justified by the value (saves 2-3 hours of manual writing).

---

## Example 3: Database Query

### Scenario
Get all chapters with images published after 2020

### LLM-Driven Approach

```python
"""
LLM-driven database queries
"""
import anthropic
import json

class LLMDatabase:
    def __init__(self, api_key: str, db_schema: Dict):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.db_schema = db_schema
        self.database = []  # In-memory database for example
    
    def query(self, natural_language_query: str) -> List[Dict]:
        """
        Use LLM to understand query and retrieve data
        """
        prompt = f"""You are a database query assistant. Given a natural language query 
and database schema, retrieve the matching records.

Database Schema:
{json.dumps(self.db_schema, indent=2)}

Current Data:
{json.dumps(self.database, indent=2)}

User Query: {natural_language_query}

Instructions:
1. Understand the query intent
2. Identify relevant filters and conditions
3. Return matching records as JSON array

Output only the JSON array, no explanation.
"""
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content[0].text)

# Usage
db = LLMDatabase(
    api_key="sk-...",
    db_schema={
        "chapters": {
            "id": "integer",
            "title": "string",
            "publication_year": "integer",
            "has_images": "boolean"
        }
    }
)

results = db.query("Get all chapters with images published after 2020")

# Performance:
# - Latency: 1-3 seconds
# - Cost: $0.02-0.05 per query
# - Accuracy: Medium (may misinterpret)
# - Determinism: Low
# - Scale: Limited (context window limits number of records)
```

### Traditional Approach (Current Architecture) ✅

```python
"""
Traditional database query with SQLAlchemy ORM
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class Chapter(Base):
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publication_year = Column(Integer)
    has_images = Column(Boolean)

class Database:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_chapters_with_images_after_year(self, year: int) -> List[Chapter]:
        """
        Get chapters with images published after specified year
        """
        return self.session.query(Chapter).filter(
            Chapter.has_images == True,
            Chapter.publication_year > year
        ).all()

# Usage
db = Database("postgresql://localhost/studybuddy")
results = db.get_chapters_with_images_after_year(2020)

# Performance:
# - Latency: 5-20ms (200x faster)
# - Cost: $0
# - Accuracy: 100% (exact query)
# - Determinism: 100%
# - Scale: Millions of records
```

### Comparison

| Metric | LLM Approach | Traditional Approach | Winner |
|--------|--------------|---------------------|--------|
| **Latency** | 1-3 seconds | 5-20ms | ✅ Traditional (100x faster) |
| **Cost per Query** | $0.02-0.05 | $0 | ✅ Traditional |
| **Cost at Scale (10k queries/day)** | $600/month | $0 | ✅ Traditional |
| **Accuracy** | ~90% | 100% | ✅ Traditional |
| **Determinism** | No | Yes | ✅ Traditional |
| **Scale** | Limited | Unlimited | ✅ Traditional |
| **Natural Language** | Yes | No | ✅ LLM |
| **Type Safety** | No | Yes | ✅ Traditional |
| **Testing** | Hard | Easy | ✅ Traditional |

**Recommendation:** Traditional approach (current architecture) ✅

**Rationale:** Database queries are deterministic operations that need to be fast, 
reliable, and testable. LLMs add no value here and introduce significant costs and risks.

---

## Example 4: PDF Chapter Detection

### Scenario
Parse PDF table of contents and extract chapter structure

### LLM-Driven Approach (Current Architecture) ✅

```python
"""
LLM-driven PDF chapter detection
"""
import anthropic
import PyPDF2
from typing import List, Dict

class LLMChapterDetector:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def detect_chapters(self, pdf_path: str) -> List[Dict]:
        """
        Use LLM to parse table of contents and extract chapters
        """
        # Extract text from PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract first 20 pages (likely contains TOC)
            toc_text = ""
            for page_num in range(min(20, len(reader.pages))):
                toc_text += reader.pages[page_num].extract_text()
        
        prompt = f"""You are a medical textbook parser. Extract the chapter structure 
from this table of contents.

Table of Contents:
{toc_text}

Instructions:
1. Identify chapter titles and page numbers
2. Detect hierarchical structure (chapters, sections, subsections)
3. Return as JSON array with structure:
[
  {{
    "chapter_number": 1,
    "title": "Chapter Title",
    "page_start": 15,
    "sections": [
      {{"title": "Section Title", "page": 20}}
    ]
  }}
]

Output only valid JSON, no explanation.
"""
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.content[0].text)

# Usage
detector = LLMChapterDetector(api_key="sk-...")
chapters = detector.detect_chapters("neurosurgery_textbook.pdf")

# Performance:
# - Latency: 5-15 seconds (acceptable, one-time per PDF)
# - Cost: $0.01-0.05 per PDF (acceptable)
# - Accuracy: High (90-95%)
# - Flexibility: Handles various TOC formats
# - Value: HIGH - saves manual parsing effort
```

### Traditional Approach (Regex/Rules-Based)

```python
"""
Traditional regex-based chapter detection
"""
import PyPDF2
import re
from typing import List, Dict

class RegexChapterDetector:
    def __init__(self):
        # Various TOC patterns to match
        self.patterns = [
            r'Chapter\s+(\d+)[:.]\s+([A-Za-z\s]+)\s+\.+\s*(\d+)',
            r'(\d+)\.\s+([A-Za-z\s]+)\s+\.+\s*(\d+)',
            r'([IVX]+)\.\s+([A-Za-z\s]+)\s+(\d+)',
        ]
    
    def detect_chapters(self, pdf_path: str) -> List[Dict]:
        """
        Use regex patterns to extract chapters
        """
        # Extract TOC text
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            toc_text = ""
            for page_num in range(min(20, len(reader.pages))):
                toc_text += reader.pages[page_num].extract_text()
        
        chapters = []
        
        # Try each pattern
        for pattern in self.patterns:
            matches = re.findall(pattern, toc_text)
            if matches:
                for match in matches:
                    chapters.append({
                        "chapter_number": self._parse_number(match[0]),
                        "title": match[1].strip(),
                        "page_start": int(match[2])
                    })
                break  # Use first matching pattern
        
        return chapters
    
    def _parse_number(self, num_str: str) -> int:
        """Convert Roman numerals or regular numbers"""
        # Simple conversion (incomplete)
        if num_str.isdigit():
            return int(num_str)
        # Roman numeral conversion...
        return 0

# Usage
detector = RegexChapterDetector()
chapters = detector.detect_chapters("neurosurgery_textbook.pdf")

# Performance:
# - Latency: 100-500ms (faster)
# - Cost: $0
# - Accuracy: Low-Medium (60-70%)
#   - Breaks on non-standard formats
#   - Misses hierarchical structure
#   - Cannot handle multi-line titles
#   - Fails on varied TOC styles
# - Maintainability: Poor (brittle, needs constant updates)
```

### Comparison

| Metric | LLM Approach | Traditional Approach | Winner |
|--------|--------------|---------------------|--------|
| **Latency** | 5-15 seconds | 100-500ms | ✅ Traditional |
| **Cost per PDF** | $0.01-0.05 | $0 | ✅ Traditional |
| **Accuracy** | 90-95% | 60-70% | ✅ LLM |
| **Flexibility** | High (handles any format) | Low (breaks easily) | ✅ LLM |
| **Maintenance** | Low | High (brittle regex) | ✅ LLM |
| **Hierarchical Structure** | Yes | Partial | ✅ LLM |
| **Frequency** | Low (one-time) | - | ✅ LLM |
| **Value** | High | Medium | ✅ LLM |

**Recommendation:** LLM approach (current architecture) ✅

**Rationale:** PDF parsing is notoriously fragile and format-dependent. LLMs excel 
at understanding structure in unstructured text. The one-time cost ($0.01-0.05 per PDF) 
is justified by higher accuracy and lower maintenance burden.

---

## Summary Matrix

| Use Case | Recommended Approach | Rationale |
|----------|---------------------|-----------|
| **Search Ranking** | ✅ Traditional | High frequency, speed critical, proven algorithms |
| **Content Generation** | ✅ LLM | Creative task, high value, acceptable latency |
| **Database Queries** | ✅ Traditional | Deterministic, high frequency, no value from LLM |
| **PDF Chapter Detection** | ✅ LLM | Complex parsing, one-time cost, fragile alternatives |
| **Caching Decisions** | ✅ Traditional | Ultra high frequency, must be instant |
| **Input Validation** | ✅ Traditional | Security critical, deterministic required |
| **Research Synthesis** | ✅ LLM | Complex reasoning, low frequency |
| **API Routing** | ✅ Traditional | Reliability critical, deterministic |
| **Text Summarization** | ✅ LLM | NLP task, creative, moderate frequency OK |
| **Data Sorting/Filtering** | ✅ Traditional | Simple algorithm, high frequency |

---

## Key Takeaway

**Use the right tool for the job:**
- **LLMs:** Creative, NLP, complex reasoning, low-frequency tasks
- **Traditional Code:** Infrastructure, high-frequency, deterministic operations

**StudyBuddy's current architecture already implements this optimal balance.**

---

**Last Updated:** November 9, 2024  
**Version:** 1.0
