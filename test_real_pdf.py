#!/usr/bin/env python3
"""
Test Phase 1 with a real neurosurgery textbook
"""

import asyncio
from reference_library.database import DatabaseManager
from reference_library.pdf_indexer import PDFIndexer
from reference_library.library_manager import LibraryManager


async def index_real_pdf():
    """Index a real neurosurgery textbook."""

    pdf_path = '/Users/ramihatoum/Desktop/Neurosurgery /reference library /Entire books/Keyhole Approaches in Neurosurgery - Volume 1 (2008) - Perneczky.pdf'

    print("\n" + "="*80)
    print("INDEXING REAL NEUROSURGERY TEXTBOOK")
    print("="*80 + "\n")

    print(f"PDF: {pdf_path.split('/')[-1]}")
    print("-" * 80)

    # Initialize database
    db_manager = DatabaseManager("sqlite:///real_library.db")
    print("✓ Database initialized: real_library.db\n")

    # Use session context manager
    with db_manager.get_session() as session:
        # Index the PDF
        print("Indexing PDF (this may take a moment for large files)...")
        print("-" * 80)

        indexer = PDFIndexer(session)

        try:
            book = await indexer.index_pdf(
                file_path=pdf_path,
                extract_images=False,  # Skip images for speed
                ai_chapter_detection=False  # Using heuristic detection
            )

            print("\n" + "="*80)
            print("EXTRACTION RESULTS")
            print("="*80 + "\n")

            print(f"Title: {book.title}")
            print(f"Authors: {', '.join(book.authors)}")
            if book.edition:
                print(f"Edition: {book.edition}")
            if book.year:
                print(f"Year: {book.year}")
            if book.publisher:
                print(f"Publisher: {book.publisher}")
            print(f"Pages: {book.page_count}")
            print(f"File Size: {book.file_size:,} bytes ({book.file_size / 1024 / 1024:.2f} MB)")
            print(f"Book ID: {book.id}")
            print(f"File Hash: {book.file_hash[:32]}...")

            print("\n" + "="*80)
            print(f"CHAPTER DETECTION RESULTS ({len(book.chapters)} chapters found)")
            print("="*80 + "\n")

            if book.chapters:
                # Show first 10 chapters
                for i, chapter in enumerate(book.chapters[:10], 1):
                    print(f"\n{i}. {chapter.title}")
                    print(f"   Pages: {chapter.start_page}-{chapter.end_page}")
                    print(f"   Detection: {chapter.detection_method}")
                    if chapter.confidence_score:
                        print(f"   Confidence: {chapter.confidence_score:.0%}")
                    if chapter.chapter_number:
                        print(f"   Number: {chapter.chapter_number}")

                if len(book.chapters) > 10:
                    print(f"\n... and {len(book.chapters) - 10} more chapters")
            else:
                print("No chapters detected (book may not have clear chapter markers)")

            # Library statistics
            print("\n" + "="*80)
            print("LIBRARY STATISTICS")
            print("="*80 + "\n")

            manager = LibraryManager(session)
            stats = manager.get_library_stats()

            print(f"Total books in library: {stats['total_books']}")
            print(f"Total chapters: {stats['total_chapters']}")
            print(f"Total images: {stats['total_images']}")

            if stats['detection_methods']:
                print("\nChapter Detection Methods:")
                for method_stats in stats['detection_methods']:
                    conf = f" (avg confidence: {method_stats['avg_confidence']:.0%})" if method_stats['avg_confidence'] else ""
                    print(f"  - {method_stats['method']}: {method_stats['count']} chapters{conf}")

            # Try searching
            print("\n" + "="*80)
            print("SEARCH TEST")
            print("="*80 + "\n")

            search_terms = ["keyhole", "approach", "craniotomy", "microscope", "pterional"]

            for term in search_terms[:3]:  # Test first 3 terms
                results = manager.search_chapters(term, limit=5)
                if results:
                    print(f"\n'{term}' → {len(results)} chapters found:")
                    for result in results[:3]:
                        print(f"  - {result.title} (pages {result.start_page}-{result.end_page})")

            print("\n" + "="*80)
            print("SUCCESS!")
            print("="*80)
            print(f"\n✓ Successfully indexed: {book.title}")
            print(f"✓ Detected {len(book.chapters)} chapters")
            print(f"✓ Stored in: real_library.db")
            print("\nYou can query this database using:")
            print("  sqlite3 real_library.db")
            print("  SELECT * FROM books;")
            print("  SELECT title, start_page, end_page FROM chapters;")
            print()

        except FileNotFoundError:
            print(f"\n✗ ERROR: File not found")
            print(f"  Path: {pdf_path}")
            print("\nPlease check:")
            print("  1. The file exists at this location")
            print("  2. The path is correct (note the spaces in directory names)")
            print("  3. You have read permissions for the file")
        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            print(f"\nError type: {type(e).__name__}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(index_real_pdf())
