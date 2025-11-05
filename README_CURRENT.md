# StudyBuddy 🧠

**Your Personal Neurosurgical Study Companion**

A simple, focused study app for neurosurgical education. No over-engineering, just what you need to learn effectively.

## What's Implemented

✅ **Library Management** - Organize your medical textbooks (PDF)  
✅ **Smart Notes** - Take organized notes with tags and search  
✅ **Flashcards** - Spaced repetition learning (SM-2 algorithm)  
✅ **Universal Search** - Find anything across all your content  
✅ **Progress Tracking** - Monitor your study time and activities  

## Quick Start

```bash
# Install dependencies
pip install sqlalchemy pydantic python-dotenv click rich PyPDF2 pytest

# Run the demo
./demo.sh

# Or try it yourself
export PYTHONPATH=.
python3 cli/main.py notes add "Your Topic" "Your note content" --tags "neurosurgery"
python3 cli/main.py flashcards add "Question?" "Answer!" --topic "Anatomy"
python3 cli/main.py search "your query"
```

## Documentation

- **[FEATURES.md](FEATURES.md)** - Complete feature overview and usage guide
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed command reference
- **[docs/](docs/)** - Original implementation plans (for reference)

## Design Philosophy

Inspired by Neurocore's lessons but kept **simple and functional**:

- ✅ Single-user focused (not multi-tenant)
- ✅ Offline-first (no API dependencies)
- ✅ Modular code (<500 lines per file)
- ✅ Type-safe configuration
- ✅ Structured error handling
- ✅ Comprehensive tests

**No AI dependencies required** - This is a pure study management tool.

## What's Different from the Docs?

The original docs describe an ambitious AI-powered system with:
- Vector embeddings
- PubMed integration  
- Multi-provider AI
- Redis caching
- Image recommendations

**We implemented the essentials instead:**
- Simple SQLite database
- Clean note-taking
- Proven spaced repetition
- Fast local search
- Progress tracking

This is a **personal study tool**, not an enterprise knowledge base. It works, it's simple, and it's yours.

## Run Tests

```bash
python3 -m pytest tests/test_smoke.py -v --override-ini="addopts="
```

All 5 tests pass ✅

## File Structure

```
cli/                    # Command-line interface
reference_library/      # Core models and managers  
search/                # Simple search service
utils/                 # Config, logging, exceptions
tests/                 # Test suite
data/                  # Your books, database, images
```

## Study Smart

1. Add your textbooks
2. Take notes as you learn
3. Create flashcards for key concepts
4. Review daily (5-10 minutes)
5. Track your progress

**Simple. Effective. Yours.** 🧠📚

---

See [FEATURES.md](FEATURES.md) for complete documentation.
