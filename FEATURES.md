# StudyBuddy - Neurosurgical Study Companion 🧠

A simple, personal study app for neurosurgical expertise development. Focused on what matters: organized notes, effective flashcard learning, and progress tracking.

## Why StudyBuddy?

Built with lessons learned from the Neurocore project - **simple but fully functional**:

✅ **No over-engineering** - Just what you need, nothing more  
✅ **Single-user focused** - Optimized for your personal study  
✅ **Offline-first** - Works without internet  
✅ **Proven patterns** - Follows Neurocore's 10 critical lessons  

## Features

### 📚 Library Management
- Store and organize your medical textbooks (PDF)
- Automatic page count extraction
- Search by title or author

### 📝 Smart Note-Taking
- Create organized notes for any topic
- Link notes to specific books and pages
- Tag for easy organization
- Full-text search across all notes

### 🗂️ Spaced Repetition Flashcards
- **SM-2 algorithm** for optimal retention
- Automatic scheduling based on your recall quality
- Track your progress with ease factors
- Filter by topic or book

### 🔍 Universal Search
- Search across all your content at once
- Find books, notes, and flashcards instantly
- Results grouped by type

### 📊 Progress Tracking
- Monitor study time per topic
- Count notes created and flashcards reviewed
- View statistics for any time period

## Quick Start

### Installation

```bash
# Install dependencies
pip install sqlalchemy pydantic python-dotenv click rich PyPDF2 pytest

# Navigate to the project
cd studdybuddy-
```

### Run the Demo

```bash
./demo.sh
```

This creates sample notes and flashcards to show you how it works!

### Common Commands

```bash
# Set Python path (needed for now)
export PYTHONPATH=/path/to/studdybuddy-

# Add a book
python3 cli/main.py library add textbook.pdf --title "Neurosurgery Basics"

# Create a note
python3 cli/main.py notes add "Cranial Nerves" "CN III, IV, VI control eye movement..." --tags "anatomy,nerves"

# Create a flashcard
python3 cli/main.py flashcards add "What does CN VII innervate?" "Muscles of facial expression" --topic "Anatomy"

# Review flashcards (spaced repetition)
python3 cli/main.py flashcards review

# Search everything
python3 cli/main.py search "aneurysm"

# View statistics
python3 cli/main.py study stats --days 7
python3 cli/main.py flashcards stats
```

## How It Works

### Spaced Repetition (SM-2 Algorithm)

When you review a flashcard, rate your recall:
- **0-2**: Forgot → Card resets to day 1
- **3**: Hard → Shorter interval
- **4**: Good → Standard interval  
- **5**: Easy → Longer interval

The algorithm automatically schedules your next review for optimal retention.

### File Structure

```
data/
├── books/          # Your PDF library
├── database/       # SQLite database (auto-created)
└── images/         # Extracted images (future)

logs/               # Application logs
```

## Architecture

Following Neurocore lessons, StudyBuddy uses:

1. **Modular design** - Each file < 500 lines
2. **Type safety** - Pydantic for configuration
3. **Structured exceptions** - Error codes for debugging
4. **SQLite database** - Simple, no setup required
5. **Dependency injection** - Easy to test

### Code Organization

```
utils/              # Foundation (config, logging, exceptions)
reference_library/  # Core models and managers
search/            # Search service
cli/               # Command-line interface
tests/             # Test suite
```

## Development

### Run Tests

```bash
python3 -m pytest tests/test_smoke.py -v --override-ini="addopts="
```

All tests should pass ✅

### Design Principles

- **Simplicity over features** - Do one thing well
- **User-focused** - Single user, not multi-tenant
- **Battle-tested patterns** - From Neurocore's experience
- **No magic** - Clear, readable code

## Inspired by Neurocore

StudyBuddy applies 10 critical lessons learned from Neurocore's 10-week refactoring:

1. ✅ **Modular from day 1** - Files stay small
2. ✅ **Security first** - Input validation everywhere
3. ✅ **Avoid N+1 queries** - Eager loading patterns
4. ✅ **Structured exceptions** - Error codes and context
5. ✅ **Testing infrastructure** - Tests written alongside features
6. ✅ **Type-safe config** - Pydantic validation
7. ✅ **Dependency injection** - Testable services

But we kept it **simple** - no over-engineering!

## Future Ideas (Keep It Simple)

- [ ] PDF text extraction for better search
- [ ] Export notes to Markdown
- [ ] Study session timer
- [ ] Daily study streak tracking
- [ ] Basic progress charts

## Tips for Effective Study

1. **Review flashcards daily** - Even 5 minutes helps
2. **Use tags generously** - Makes searching easier
3. **Take notes as you study** - Active learning works
4. **Track your sessions** - See your progress
5. **Search often** - Reinforce connections

## Contributing

This is a personal study tool, but suggestions welcome! Keep the philosophy:
- Simple over complex
- Functional over fancy
- User-focused over feature-bloated

## License

MIT License - Use it for your studies!

---

**Study smart, not hard.** 🧠📚

Built with ❤️ for neurosurgical education.
