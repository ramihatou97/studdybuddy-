#!/usr/bin/env python3
"""
Phase 1 Demo: PDF Indexing and Library Management

This script demonstrates:
1. Creating a sample medical PDF
2. Indexing it into the database
3. Retrieving and displaying the indexed content
4. Searching through the library
"""

import asyncio
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reference_library.database import DatabaseManager
from reference_library.pdf_indexer import PDFIndexer
from reference_library.library_manager import LibraryManager


def create_sample_medical_pdf(output_path: str) -> None:
    """Create a sample medical textbook PDF with multiple chapters."""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Page 1: Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Neurosurgery Fundamentals")
    c.setFont("Helvetica", 14)
    c.drawString(100, height - 150, "A Comprehensive Guide to Brain Surgery")
    c.drawString(100, height - 180, "Dr. Jane Smith, MD, PhD")
    c.showPage()

    # Page 2: Chapter 1
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Chapter 1: Cranial Anatomy")
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 120, "The human skull consists of 22 bones that protect the brain.")
    c.drawString(72, height - 140, "The cranium is divided into the neurocranium and viscerocranium.")
    c.drawString(72, height - 160, "Key anatomical landmarks include:")
    c.drawString(90, height - 180, "- Frontal bone: Forms the forehead and roof of the orbits")
    c.drawString(90, height - 200, "- Parietal bones: Form the sides and roof of the cranium")
    c.drawString(90, height - 220, "- Temporal bones: House the middle and inner ear structures")
    c.drawString(90, height - 240, "- Occipital bone: Forms the back and base of the skull")
    c.showPage()

    # Page 3: More Chapter 1 content
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 72, "Understanding cranial anatomy is essential for surgical planning.")
    c.drawString(72, height - 92, "The brain is protected by three meningeal layers:")
    c.drawString(90, height - 112, "1. Dura mater (outermost, tough layer)")
    c.drawString(90, height - 132, "2. Arachnoid mater (middle layer)")
    c.drawString(90, height - 152, "3. Pia mater (innermost, delicate layer)")
    c.showPage()

    # Page 4: Chapter 2
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Chapter 2: Surgical Approaches")
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 120, "Multiple surgical approaches exist for accessing the brain.")
    c.drawString(72, height - 140, "The choice depends on the pathology location and surgeon preference.")
    c.drawString(72, height - 180, "Pterional Approach:")
    c.drawString(90, height - 200, "- Most common approach for supratentorial lesions")
    c.drawString(90, height - 220, "- Provides excellent access to the temporal lobe")
    c.drawString(90, height - 240, "- Minimizes brain retraction")
    c.drawString(72, height - 280, "Retrosigmoid Approach:")
    c.drawString(90, height - 300, "- Used for posterior fossa lesions")
    c.drawString(90, height - 320, "- Provides access to cerebellopontine angle")
    c.showPage()

    # Page 5: Chapter 3
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Chapter 3: Postoperative Care")
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 120, "Postoperative management is crucial for patient outcomes.")
    c.drawString(72, height - 160, "Key monitoring parameters:")
    c.drawString(90, height - 180, "- Neurological status (GCS score)")
    c.drawString(90, height - 200, "- Intracranial pressure (ICP)")
    c.drawString(90, height - 220, "- Vital signs and hemodynamic stability")
    c.drawString(90, height - 240, "- Wound healing and infection signs")
    c.drawString(72, height - 280, "Common complications to watch for:")
    c.drawString(90, height - 300, "- Cerebral edema")
    c.drawString(90, height - 320, "- Hemorrhage")
    c.drawString(90, height - 340, "- Infection")
    c.drawString(90, height - 360, "- Seizures")
    c.showPage()

    c.save()
    print(f"✓ Created sample PDF: {output_path}")


async def demo_pdf_indexing():
    """Demonstrate the PDF indexing workflow."""

    print("\n" + "="*80)
    print("PHASE 1 DEMO: PDF INDEXING AND LIBRARY MANAGEMENT")
    print("="*80 + "\n")

    # Step 1: Create sample PDF
    print("STEP 1: Creating Sample Medical PDF")
    print("-" * 80)
    pdf_path = "/tmp/neurosurgery_fundamentals.pdf"
    create_sample_medical_pdf(pdf_path)

    # Step 2: Initialize database and indexer
    print("\nSTEP 2: Initializing Database")
    print("-" * 80)
    db_manager = DatabaseManager("sqlite:///demo_library.db")
    # Tables are created automatically during initialization
    print("✓ Database initialized: demo_library.db")

    # Use session context manager for all database operations
    with db_manager.get_session() as session:
        # Step 3: Index the PDF
        print("\nSTEP 3: Indexing PDF into Database")
        print("-" * 80)

        indexer = PDFIndexer(session)
        book = await indexer.index_pdf(
            file_path=pdf_path,
            extract_images=True,
            ai_chapter_detection=False  # Using heuristic detection
        )

        print(f"✓ Indexed book: {book.title}")
        print(f"  - Book ID: {book.id}")
        print(f"  - File hash: {book.file_hash[:16]}...")
        print(f"  - Pages: {book.page_count}")
        print(f"  - Authors: {', '.join(book.authors)}")
        print(f"  - Chapters detected: {len(book.chapters)}")

        # Step 4: Display chapter information
        print("\nSTEP 4: Chapter Detection Results")
        print("-" * 80)
        for i, chapter in enumerate(book.chapters, 1):
            print(f"\nChapter {i}:")
            print(f"  Title: {chapter.title}")
            print(f"  Pages: {chapter.start_page}-{chapter.end_page}")
            print(f"  Confidence: {chapter.confidence_score:.2%}" if chapter.confidence_score else "  Confidence: N/A")
            print(f"  Sections: {len(chapter.sections)}")
            # Show abstract or summary if available
            if chapter.abstract:
                print(f"  Abstract: {chapter.abstract[:150]}...")
            elif chapter.ai_summary:
                print(f"  AI Summary: {chapter.ai_summary[:150]}...")

        # Step 5: Use LibraryManager to query the library
        print("\n\nSTEP 5: Library Management Operations")
        print("-" * 80)

        manager = LibraryManager(session)

        # Get library statistics
        stats = manager.get_library_stats()
        print("\nLibrary Statistics:")
        print(f"  Total books: {stats['total_books']}")
        print(f"  Total chapters: {stats['total_chapters']}")
        print(f"  Total images: {stats['total_images']}")
        if stats['detection_methods']:
            print("\n  Chapter Detection Methods:")
            for method_stats in stats['detection_methods']:
                print(f"    - {method_stats['method']}: {method_stats['count']} chapters " +
                      f"(avg confidence: {method_stats['avg_confidence']:.0%})" if method_stats['avg_confidence'] else "")

        # List all books
        print("\nAll Books in Library:")
        books = manager.list_books()
        for book_item in books:
            print(f"  - {book_item.title} ({book_item.page_count} pages, {len(book_item.chapters)} chapters)")

        # Search for specific content
        print("\nSTEP 6: Simple Text Search")
        print("-" * 80)
        search_terms = ["temporal", "approach", "meningeal"]

        for term in search_terms:
            results = manager.search_chapters(term, limit=3)
            print(f"\nSearch results for '{term}': {len(results)} chapters found")
            for result in results[:2]:  # Show first 2 results
                print(f"  - {result.title} (pages {result.start_page}-{result.end_page})")
                # Show section count and summary info
                print(f"    Sections: {len(result.sections)}")
                if result.abstract:
                    print(f"    Abstract: {result.abstract[:100]}...")

        # Step 7: Demonstrate duplicate detection
        print("\n\nSTEP 7: Duplicate Detection")
        print("-" * 80)
        print("Attempting to index the same PDF again...")
        duplicate_book = await indexer.index_pdf(pdf_path)
        if duplicate_book.id == book.id:
            print(f"✓ Duplicate detected! Returned existing book (ID: {duplicate_book.id})")
            print(f"  Original book ID: {book.id}")
            print(f"  Both IDs match - no duplicate created!")
        else:
            print(f"✗ Warning: Different book created (this shouldn't happen)")

    # Summary
    print("\n" + "="*80)
    print("DEMO COMPLETE!")
    print("="*80)
    print("\nPhase 1 Features Demonstrated:")
    print("  ✓ PDF metadata extraction (title, authors, pages)")
    print("  ✓ Heuristic chapter detection with confidence scores")
    print("  ✓ Database storage with relationships (books → chapters → sections)")
    print("  ✓ SHA-256 file hashing for duplicate detection")
    print("  ✓ Library management (stats, listing, searching)")
    print("  ✓ Simple text-based chapter search")
    print("\nDatabase file: demo_library.db")
    print("You can inspect it with: sqlite3 demo_library.db")
    print("\n")


if __name__ == "__main__":
    asyncio.run(demo_pdf_indexing())
