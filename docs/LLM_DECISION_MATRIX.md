# LLM vs Traditional Code: Decision Matrix & Evaluation Tool

**Purpose:** Help developers make informed decisions about when to use LLMs vs traditional code

---

## Quick Decision Tree

```
Is the task one of these?
├─ Content Generation (text/summaries/explanations)
│  └─ ✅ USE LLM
│
├─ Natural Language Understanding (parsing, extraction, classification)
│  ├─ High volume (>1000/day)?
│  │  ├─ YES → ❌ Use traditional NLP
│  │  └─ NO → ✅ Use LLM
│  │
│  └─ Complex/nuanced understanding needed?
│     └─ ✅ USE LLM
│
├─ Data Operations (CRUD, queries, filtering, sorting)
│  └─ ❌ Use traditional code
│
├─ Infrastructure (caching, routing, monitoring)
│  └─ ❌ Use traditional code
│
├─ Security/Validation
│  └─ ❌ Use traditional code (never trust LLM for security)
│
└─ Search/Ranking
   ├─ Semantic understanding needed?
   │  ├─ YES → ✅ Use LLM for embeddings + traditional for search
   │  └─ NO → ❌ Use traditional search (BM25)
   │
   └─ Complex ranking logic?
      └─ ❌ Use traditional algorithms (faster, cheaper, debuggable)
```

---

## Detailed Evaluation Criteria

### Score each criterion from 1-5, then calculate recommendation

| Criterion | Weight | Score | Points |
|-----------|--------|-------|--------|
| **Creativity Required** | 3x | ___ | ___ |
| **NLP/Semantic Understanding** | 3x | ___ | ___ |
| **Acceptable Latency (ms)** | 2x | ___ | ___ |
| **Low Frequency (<100/day)** | 2x | ___ | ___ |
| **Cost per Call** | 2x | ___ | ___ |
| **Non-Deterministic OK** | 2x | ___ | ___ |
| **No PII/Sensitive Data** | 3x | ___ | ___ |
| **Complex Reasoning** | 2x | ___ | ___ |
| **Traditional Solution Difficulty** | 1x | ___ | ___ |

**Scoring Guide:**
- **1:** Strongly favors traditional code
- **3:** Neutral
- **5:** Strongly favors LLM

**Total Score Calculation:**
- Sum all Points (Score × Weight)
- **< 40:** Use traditional code
- **40-60:** Hybrid or case-by-case
- **> 60:** Use LLM

---

## Detailed Scoring Guidelines

### 1. Creativity Required (Weight: 3x)

**Score 5:** Task requires generating novel content
- Examples: Writing chapter sections, generating explanations, creating summaries
- Traditional code cannot do this well

**Score 3:** Mix of creativity and structure
- Examples: Formatting structured data with descriptions

**Score 1:** No creativity needed, purely algorithmic
- Examples: Sorting data, filtering records, computing statistics

### 2. NLP/Semantic Understanding (Weight: 3x)

**Score 5:** Deep language understanding required
- Examples: Understanding medical terminology, extracting entities from unstructured text
- Traditional NLP would require significant training data

**Score 3:** Simple NLP tasks
- Examples: Keyword extraction, simple classification

**Score 1:** No NLP needed
- Examples: Numeric calculations, boolean logic

### 3. Acceptable Latency (Weight: 2x)

**Score 5:** > 2000ms acceptable
- Examples: Batch processing, background jobs, report generation

**Score 3:** 500-2000ms acceptable
- Examples: Complex user queries, research synthesis

**Score 1:** < 100ms required
- Examples: Search autocomplete, real-time filtering, cache lookups

### 4. Call Frequency (Weight: 2x)

**Score 5:** < 10 calls per day
- Examples: PDF indexing (one-time), monthly reports

**Score 3:** 10-100 calls per day
- Examples: User-initiated content generation

**Score 1:** > 1000 calls per day
- Examples: Search queries, database operations, API routing

### 5. Cost per Call (Weight: 2x)

**Score 5:** Can tolerate $1+ per call
- Examples: Complex analysis, one-time tasks with high value

**Score 3:** Can tolerate $0.10-$1 per call
- Examples: Content generation, research synthesis

**Score 1:** Must be < $0.01 per call
- Examples: Search, caching, routing

### 6. Deterministic Behavior (Weight: 2x)

**Score 5:** Non-deterministic results acceptable
- Examples: Creative writing, brainstorming, exploration

**Score 3:** Some variance OK but must meet criteria
- Examples: Summarization with quality checks

**Score 1:** Must be 100% deterministic
- Examples: Unit tests, regulatory compliance, financial calculations

### 7. Data Sensitivity (Weight: 3x)

**Score 5:** No PII or sensitive data
- Examples: Public research papers, general medical knowledge

**Score 3:** Sensitive but anonymizable
- Examples: Aggregate statistics, anonymized case studies

**Score 1:** Contains PII or highly sensitive data
- Examples: Patient records, proprietary research, credentials

### 8. Complex Reasoning (Weight: 2x)

**Score 5:** Multi-step reasoning, context integration
- Examples: Synthesizing multiple research papers, explaining complex relationships

**Score 3:** Moderate reasoning
- Examples: Simple if-then logic with context

**Score 1:** Simple logic
- Examples: Equality checks, threshold comparisons

### 9. Traditional Solution Difficulty (Weight: 1x)

**Score 5:** Traditional solution extremely difficult/fragile
- Examples: PDF table of contents parsing, medical text entity extraction

**Score 3:** Traditional solution possible but complex
- Examples: Advanced NLP tasks

**Score 1:** Traditional solution trivial
- Examples: String manipulation, list sorting

---

## Example Evaluations

### Example 1: Search Query Ranking

| Criterion | Weight | Score | Points | Rationale |
|-----------|--------|-------|--------|-----------|
| Creativity Required | 3x | 1 | 3 | Algorithmic task |
| NLP/Understanding | 3x | 2 | 6 | Some semantic understanding helpful |
| Acceptable Latency | 2x | 1 | 2 | Must be < 100ms |
| Low Frequency | 2x | 1 | 2 | 1000s per day |
| Cost per Call | 2x | 1 | 2 | Must be pennies |
| Non-Deterministic OK | 2x | 1 | 2 | Must be consistent |
| No PII | 3x | 5 | 15 | Public queries |
| Complex Reasoning | 2x | 2 | 4 | Ranking algorithms |
| Traditional Difficulty | 1x | 1 | 1 | Well-known algorithms |
| **TOTAL** | | | **37** | **Use traditional code** |

**Recommendation:** Use BM25 + semantic embeddings + RRF (current architecture)

### Example 2: Chapter Section Generation

| Criterion | Weight | Score | Points | Rationale |
|-----------|--------|-------|--------|-----------|
| Creativity Required | 3x | 5 | 15 | Must generate novel text |
| NLP/Understanding | 3x | 5 | 15 | Deep medical understanding |
| Acceptable Latency | 2x | 5 | 10 | 10s is fine |
| Low Frequency | 2x | 4 | 8 | On-demand by users |
| Cost per Call | 2x | 3 | 6 | $0.50 acceptable |
| Non-Deterministic OK | 2x | 4 | 8 | Minor variations OK |
| No PII | 3x | 5 | 15 | Public medical knowledge |
| Complex Reasoning | 2x | 5 | 10 | Multi-source synthesis |
| Traditional Difficulty | 1x | 5 | 5 | Impossible traditionally |
| **TOTAL** | | | **92** | **DEFINITELY use LLM** |

**Recommendation:** Use LLM (current architecture) ✅

### Example 3: Database Query Optimization

| Criterion | Weight | Score | Points | Rationale |
|-----------|--------|-------|--------|-----------|
| Creativity Required | 3x | 1 | 3 | Pure algorithm |
| NLP/Understanding | 3x | 1 | 3 | No NLP |
| Acceptable Latency | 2x | 1 | 2 | Must be < 10ms |
| Low Frequency | 2x | 1 | 2 | 10,000s per day |
| Cost per Call | 2x | 1 | 2 | Must be free |
| Non-Deterministic OK | 2x | 1 | 2 | Must be exact |
| No PII | 3x | 1 | 3 | May contain PII |
| Complex Reasoning | 2x | 1 | 2 | SQL is deterministic |
| Traditional Difficulty | 1x | 1 | 1 | Well-established |
| **TOTAL** | | | **20** | **NEVER use LLM** |

**Recommendation:** Use SQLAlchemy + eager loading (current architecture) ✅

### Example 4: PDF Chapter Detection

| Criterion | Weight | Score | Points | Rationale |
|-----------|--------|-------|--------|-----------|
| Creativity Required | 3x | 2 | 6 | Some interpretation |
| NLP/Understanding | 3x | 5 | 15 | Complex structure parsing |
| Acceptable Latency | 2x | 5 | 10 | One-time per PDF |
| Low Frequency | 2x | 5 | 10 | Few PDFs per day |
| Cost per Call | 2x | 5 | 10 | $0.01 is fine |
| Non-Deterministic OK | 2x | 3 | 6 | Some variance OK |
| No PII | 3x | 5 | 15 | Public textbooks |
| Complex Reasoning | 2x | 4 | 8 | Hierarchical structure |
| Traditional Difficulty | 1x | 5 | 5 | PDF parsing is fragile |
| **TOTAL** | | | **85** | **Use LLM** |

**Recommendation:** Use LLM (current architecture) ✅

### Example 5: Cache Invalidation Strategy

| Criterion | Weight | Score | Points | Rationale |
|-----------|--------|-------|--------|-----------|
| Creativity Required | 3x | 1 | 3 | Rule-based |
| NLP/Understanding | 3x | 1 | 3 | No NLP |
| Acceptable Latency | 2x | 1 | 2 | Must be instant |
| Low Frequency | 2x | 1 | 2 | Very frequent |
| Cost per Call | 2x | 1 | 2 | Must be free |
| Non-Deterministic OK | 2x | 1 | 2 | Must be exact |
| No PII | 3x | 3 | 9 | Cache keys only |
| Complex Reasoning | 2x | 2 | 4 | TTL logic |
| Traditional Difficulty | 1x | 1 | 1 | Well-known patterns |
| **TOTAL** | | | **28** | **Use traditional code** |

**Recommendation:** Use Redis + TTL (current architecture) ✅

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: "LLMs can do anything, so let's use them everywhere"
**Reality:** Just because LLMs *can* do something doesn't mean they *should*
**Example:** Using LLM to sort a list → 1000x slower, costs money, non-deterministic

### ❌ Pitfall 2: "We'll optimize LLM costs later"
**Reality:** Costs scale with usage; optimization is hard after architecture is set
**Example:** Moving from LLM-driven search to traditional requires full rewrite

### ❌ Pitfall 3: "Non-determinism isn't a problem"
**Reality:** Makes testing, debugging, and compliance nearly impossible
**Example:** Cannot write unit tests for non-deterministic functions

### ❌ Pitfall 4: "Users won't notice 2-second latency"
**Reality:** Users expect sub-second responses for interactive features
**Example:** Search taking 2s instead of 50ms → users perceive as "broken"

### ❌ Pitfall 5: "We'll cache everything"
**Reality:** Cold cache hits are unavoidable; first user pays full latency penalty
**Example:** First search of the day: 2000ms → user leaves

### ❌ Pitfall 6: "LLMs understand context better"
**Reality:** LLMs hallucinate; traditional code with domain logic is more reliable
**Example:** Medical contraindications are rule-based, not probabilistic

---

## Best Practices

### ✅ DO: Use LLMs for Core Value-Add
```python
# Good: LLM generates medical content (core value)
def generate_chapter_section(topic, research):
    return llm.complete(f"Generate section on {topic} using {research}")
```

### ✅ DO: Use Traditional Code for Infrastructure
```python
# Good: Traditional code handles infrastructure
def search(query):
    # Fast, reliable, cheap
    return bm25_index.search(query)
```

### ✅ DO: Combine Both Strategically
```python
# Good: LLM for understanding, traditional for execution
def smart_search(query):
    # LLM: Understand intent (one-time, cached)
    intent = cache.get_or_compute(query, lambda: llm.parse_intent(query))
    
    # Traditional: Execute search (fast, cheap)
    return traditional_search(intent.keywords, intent.filters)
```

### ✅ DO: Set Budgets and Monitor
```python
# Good: Track costs and set limits
@cost_monitor(max_daily_cost=10.00)
def llm_operation(prompt):
    return llm.complete(prompt)
```

### ❌ DON'T: Use LLMs for High-Frequency Operations
```python
# Bad: LLM in hot path
def get_user(user_id):
    return llm.complete(f"Find user {user_id} in database")
    # Should be: return db.query(User).get(user_id)
```

### ❌ DON'T: Use LLMs for Security Decisions
```python
# Bad: LLM for security
def is_safe(input):
    return llm.complete(f"Is this safe? {input}") == "yes"
    # Should be: return input_validator.sanitize(input)
```

---

## Cost Calculator

### Estimate monthly costs for different approaches

**Input Variables:**
- `calls_per_day`: Number of operations per day
- `tokens_per_call`: Average tokens per LLM call
- `cost_per_1k_tokens`: API pricing (e.g., $0.03 for GPT-4)

**Formula:**
```python
monthly_cost = (calls_per_day * 30) * (tokens_per_call / 1000) * cost_per_1k_tokens
```

**Example Calculations:**

| Use Case | Calls/Day | Tokens/Call | $/1k Tokens | Monthly Cost |
|----------|-----------|-------------|-------------|--------------|
| Search (LLM) | 1,000 | 1,500 | $0.03 | **$1,350** |
| Search (Traditional) | 1,000 | 0 | $0 | **$0** |
| Content Gen (LLM) | 10 | 3,000 | $0.03 | **$9** |
| Cache Decision (LLM) | 5,000 | 500 | $0.03 | **$2,250** |
| Cache Decision (Traditional) | 5,000 | 0 | $0 | **$0** |
| Chapter Detection (LLM) | 2 | 2,000 | $0.03 | **$3.60** |

**Breakeven Analysis:**
- Traditional code costs: ~$0.01/1000 calls (compute only)
- LLM becomes cost-effective when: `value_per_call > llm_cost_per_call + $0.00001`

---

## Migration Strategy

### If You've Already Maximized LLM Usage

**Phase 1: Identify Quick Wins (Week 1)**
1. Profile all LLM calls (frequency, cost, latency)
2. Identify high-frequency, low-complexity calls
3. Replace with traditional code
4. Expected savings: 50-70% of costs

**Phase 2: Extract Infrastructure (Week 2-3)**
1. Move database operations to traditional code
2. Move caching to traditional code
3. Move routing to traditional code
4. Expected savings: Additional 20-30%

**Phase 3: Optimize Remaining LLM Usage (Week 4)**
1. Implement aggressive caching
2. Use cheaper models where possible
3. Batch requests
4. Expected savings: 30-50% of remaining costs

**Total Expected Savings:** 80-90% cost reduction

---

## Summary Checklist

Before using an LLM for a task, verify:

- [ ] Traditional solution would be significantly more difficult
- [ ] Latency > 500ms is acceptable
- [ ] Cost per call < $0.50 is acceptable
- [ ] Frequency < 100 calls/day
- [ ] Non-deterministic results are acceptable
- [ ] No PII or sensitive data involved
- [ ] Task requires creativity or complex NLP
- [ ] You have monitoring and cost controls in place
- [ ] You have a fallback strategy for API outages

**If you checked < 5 boxes:** Use traditional code instead

---

## Conclusion

**The Default Should Be Traditional Code**

Only use LLMs when:
1. They provide clear value that's difficult to achieve otherwise
2. The economics make sense (cost + latency acceptable)
3. You've considered all the risks and have mitigation strategies

**StudyBuddy's Current Architecture (70-80% traditional, 20-30% LLM) is optimal.**

---

**Last Updated:** November 9, 2024  
**Version:** 1.0
