#!/usr/bin/env python3
"""
Index any PDF from the test_books directory
"""

import asyncio
import sys
from pathlib import Path
from reference_library.database import DatabaseManager
from reference_library.pdf_indexer import PDFIndexer
from reference_library.library_manager import LibraryManager


async def index_pdf(pdf_path: str):
    """Index a PDF and show results."""

    print("\n" + "="*80)
    print(f"INDEXING: {Path(pdf_path).name}")
    print("="*80 + "\n")

    # Initialize database
    db_manager = DatabaseManager("sqlite:///real_library.db")
    print("✓ Database initialized\n")

    with db_manager.get_session() as session:
        indexer = PDFIndexer(session)

        try:
            print("Processing PDF (may take a minute for large files)...")
            book = await indexer.index_pdf(
                file_path=pdf_path,
                extract_images=False,
                ai_chapter_detection=False
            )

            print("\n" + "="*80)
            print("SUCCESS!")
            print("="*80 + "\n")

            print(f"Title: {book.title}")
            print(f"Authors: {', '.join(book.authors)}")
            print(f"Pages: {book.page_count}")
            print(f"Size: {book.file_size / 1024 / 1024:.2f} MB")
            print(f"Chapters detected: {len(book.chapters)}\n")

            if book.chapters:
                print("="*80)
                print("CHAPTERS")
                print("="*80 + "\n")
                for i, chapter in enumerate(book.chapters[:15], 1):
                    conf = f" [{chapter.confidence_score:.0%}]" if chapter.confidence_score else ""
                    print(f"{i:2}. {chapter.title} (p.{chapter.start_page}-{chapter.end_page}){conf}")

                if len(book.chapters) > 15:
                    print(f"\n... and {len(book.chapters) - 15} more chapters")

            # Quick search test
            print("\n" + "="*80)
            print("SEARCH TEST")
            print("="*80 + "\n")

            manager = LibraryManager(session)
            for term in ["approach", "surgery", "craniotomy"]:
                results = manager.search_chapters(term, limit=3)
                if results:
                    print(f"'{term}' → {len(results)} chapters")

            print(f"\n✓ Book stored in: real_library.db")
            print(f"✓ Book ID: {book.id}\n")

        except FileNotFoundError:
            print(f"\n✗ File not found: {pdf_path}")
            print("\nMake sure the file is in the project directory.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        # Check test_books directory
        test_books = Path("/home/user/studdybuddy-/test_books")
        pdfs = list(test_books.glob("*.pdf"))

        if pdfs:
            pdf_path = str(pdfs[0])
            print(f"Found PDF: {pdfs[0].name}")
        else:
            print("No PDF files found in test_books/")
            print("\nUsage: python index_pdf.py <path-to-pdf>")
            print("   or: Copy PDF to test_books/ directory")
            sys.exit(1)

    asyncio.run(index_pdf(pdf_path))
