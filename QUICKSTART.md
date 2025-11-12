# StudyBuddy Quick Start 🧠

A simple, personal neurosurgical study companion focused on what matters:
- 📚 Managing your medical textbooks
- 📝 Taking organized study notes
- 🗂️ Creating flashcards with spaced repetition
- 📊 Tracking your study progress

## Installation

```bash
# Install required dependencies
pip install sqlalchemy pydantic python-dotenv click rich PyPDF2 pytest

# Clone and navigate to the repository
cd studdybuddy-
```

## Quick Start

### 1. Add a Book to Your Library

```bash
python3 cli/main.py library add path/to/medical_textbook.pdf --title "Neurosurgery Fundamentals"
```

### 2. List Your Books

```bash
python3 cli/main.py library list
```

### 3. Create Study Notes

```bash
python3 cli/main.py notes add "Craniotomy Techniques" "Standard pterional approach involves..." --tags "surgery,techniques"
```

### 4. List Your Notes

```bash
python3 cli/main.py notes list
```

### 5. Search Notes

```bash
python3 cli/main.py notes search "craniotomy"
```

### 6. Create Flashcards

```bash
python3 cli/main.py flashcards add "What is the Circle of Willis?" "An arterial circle at the base of the brain" --topic "Neuroanatomy"
```

### 7. Review Flashcards (Spaced Repetition)

```bash
python3 cli/main.py flashcards review
```

Rate each card:
- 0-2: Forgot (resets the card)
- 3: Hard (shorter interval)
- 4: Good (standard interval)
- 5: Easy (longer interval)

### 8. Check Flashcard Stats

```bash
python3 cli/main.py flashcards stats
```

### 9. View Study Statistics

```bash
python3 cli/main.py study stats --days 7
```

## Key Features

### 📚 Library Management
- Add PDF textbooks to your personal library
- Automatically extracts page count
- Search by title or author
- Organized storage in `data/books/`

### 📝 Smart Note-Taking
- Link notes to specific books and pages
- Tag notes for easy organization
- Full-text search across all notes
- Track creation and modification dates

### 🗂️ Spaced Repetition Flashcards
- Uses SM-2 algorithm for optimal learning
- Automatically schedules reviews
- Tracks your progress with ease factor
- Filter by topic or book

### 📊 Progress Tracking
- Track study sessions
- Monitor time spent per topic
- Count notes created and flashcards reviewed
- View statistics for any time period

## File Structure

```
studdybuddy-/
├── cli/
│   └── main.py              # Command-line interface
├── reference_library/
│   ├── models.py            # Database models
│   ├── library_manager.py  # Book management
│   ├── notes_manager.py    # Note management
│   ├── flashcard_manager.py # Flashcard with spaced repetition
│   └── study_tracker.py    # Progress tracking
├── utils/
│   ├── config.py           # Configuration
│   ├── exceptions.py       # Custom exceptions
│   └── logger.py           # Logging
├── tests/
│   └── test_smoke.py       # Basic tests
└── data/
    ├── books/              # Your PDF library
    ├── database/           # SQLite database
    └── images/             # Extracted images
```

## Design Philosophy

Following lessons from the Neurocore project, StudyBuddy is built with:

1. **Simplicity First**: No over-engineering, just what you need
2. **Modularity**: Each component is independent (<500 lines per file)
3. **Type Safety**: Pydantic models for configuration
4. **Structured Errors**: Clear error messages with error codes
5. **Single User Focus**: Optimized for personal study, not multi-user
6. **Offline First**: Works without internet connection

## Running Tests

```bash
python3 -m pytest tests/test_smoke.py -v --override-ini="addopts="
```

## Database

StudyBuddy uses SQLite for simplicity:
- Database location: `data/database/studybuddy.db`
- Automatic schema creation
- No setup required

## Tips for Effective Study

1. **Review flashcards daily** - Even 5-10 minutes helps retention
2. **Tag your notes** - Makes searching easier later
3. **Link notes to books** - Keep track of sources
4. **Track your sessions** - See your progress over time
5. **Use the search** - Find information quickly when you need it

## Future Enhancements (Simple & Practical)

- PDF text extraction for better search
- Export notes to Markdown
- Study session timer
- Daily study reminders
- Basic statistics visualization

## Support

For issues or questions, check the GitHub repository or create an issue.

---

**Remember**: Consistency beats intensity. Study a little every day! 🧠📚
