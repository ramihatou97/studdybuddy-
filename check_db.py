#!/usr/bin/env python3
"""Quick check of the demo database"""

from reference_library.database import DatabaseManager
from reference_library.library_manager import LibraryManager

db_manager = DatabaseManager("sqlite:///demo_library.db")

with db_manager.get_session() as session:
    manager = LibraryManager(session)

    print("\n=== Library Contents ===\n")
    books = manager.list_books()

    if books:
        for book in books:
            print(f"Book: {book.title}")
            print(f"  Pages: {book.page_count}")
            print(f"  Chapters: {len(book.chapters)}")
            print(f"  Hash: {book.file_hash[:16]}...")
            print()

            for i, chapter in enumerate(book.chapters, 1):
                print(f"  {i}. {chapter.title} (pages {chapter.start_page}-{chapter.end_page})")
    else:
        print("No books in database yet")

    print("\n=== Statistics ===\n")
    stats = manager.get_library_stats()
    print(f"Total books: {stats['total_books']}")
    print(f"Total chapters: {stats['total_chapters']}")
    print()
