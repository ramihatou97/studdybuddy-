"""
Command-line interface for StudyBuddy.
Simple, intuitive commands for neurosurgical study management.
"""
import sys

import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from reference_library.models import DatabaseManager
from reference_library.library_manager import LibraryManager
from reference_library.notes_manager import NotesManager
from reference_library.flashcard_manager import FlashcardManager
from reference_library.study_tracker import StudyTracker
from generation.chapter_synthesizer import ChapterSynthesizer
from search.search_service import SearchService
from utils.config import get_config
from utils.logger import logger

# Initialize console for rich output
console = Console()
config = get_config()

# Initialize managers
db_manager = DatabaseManager(str(config.database.db_path))
library_manager = LibraryManager(db_manager, config.library.books_dir, config.library.images_dir)
notes_manager = NotesManager(db_manager)
flashcard_manager = FlashcardManager(db_manager)
study_tracker = StudyTracker(db_manager)
search_service = SearchService(db_manager)
chapter_synthesizer = ChapterSynthesizer(db_manager)


@click.group()
def cli():
    """StudyBuddy - Your Neurosurgical Study Companion 🧠"""
    pass


# Library commands
@cli.group()
def library():
    """Manage your medical textbook library"""
    pass


@library.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--title', help='Book title')
@click.option('--author', help='Book author')
def add(pdf_path, title, author):
    """Add a PDF book to your library"""
    try:
        book = library_manager.add_book(pdf_path, title, author)
        rprint(f"[green]✓[/green] Added: {book.title}")
        rprint(f"  Pages: {book.total_pages}")
        rprint(f"  ID: {book.id}")
    except Exception as e:
        rprint(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@library.command()
def list():
    """List all books in your library"""
    books = library_manager.list_books()
    
    if not books:
        rprint("[yellow]No books in library yet. Add one with 'library add'[/yellow]")
        return
    
    table = Table(title="📚 Your Library")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Author")
    table.add_column("Pages", justify="right")
    table.add_column("Added")
    
    for book in books:
        table.add_row(
            str(book.id),
            book.title,
            book.author or "-",
            str(book.total_pages) if book.total_pages else "-",
            book.added_at.strftime("%Y-%m-%d")
        )
    
    console.print(table)


@library.command()
@click.argument('query')
def search(query):
    """Search books by title or author"""
    books = library_manager.search_books(query)
    
    if not books:
        rprint(f"[yellow]No books found matching '{query}'[/yellow]")
        return
    
    for book in books:
        rprint(f"[green]#{book.id}[/green] {book.title}")
        if book.author:
            rprint(f"  Author: {book.author}")


# Notes commands
@cli.group()
def notes():
    """Manage your study notes"""
    pass


@notes.command()
@click.argument('topic')
@click.argument('content')
@click.option('--book-id', type=int, help='Related book ID')
@click.option('--page', type=int, help='Page number')
@click.option('--tags', help='Comma-separated tags')
def add(topic, content, book_id, page, tags):
    """Create a new study note"""
    try:
        note = notes_manager.create_note(topic, content, book_id, page, tags)
        rprint(f"[green]✓[/green] Created note: {note.topic}")
        rprint(f"  ID: {note.id}")
    except Exception as e:
        rprint(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@notes.command()
@click.option('--book-id', type=int, help='Filter by book ID')
def list(book_id):
    """List all your notes"""
    notes_list = notes_manager.list_notes(book_id)
    
    if not notes_list:
        rprint("[yellow]No notes yet. Create one with 'notes add'[/yellow]")
        return
    
    table = Table(title="📝 Your Notes")
    table.add_column("ID", style="cyan")
    table.add_column("Topic", style="green")
    table.add_column("Content")
    table.add_column("Tags")
    table.add_column("Created")
    
    for note in notes_list:
        content_preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
        table.add_row(
            str(note.id),
            note.topic,
            content_preview,
            note.tags or "-",
            note.created_at.strftime("%Y-%m-%d")
        )
    
    console.print(table)


@notes.command()
@click.argument('query')
def search(query):
    """Search notes by topic, content, or tags"""
    notes_list = notes_manager.search_notes(query)
    
    if not notes_list:
        rprint(f"[yellow]No notes found matching '{query}'[/yellow]")
        return
    
    for note in notes_list:
        rprint(f"[green]#{note.id}[/green] {note.topic}")
        rprint(f"  {note.content[:100]}...")


# Flashcards commands
@cli.group()
def flashcards():
    """Manage flashcards with spaced repetition"""
    pass


@flashcards.command()
@click.argument('question')
@click.argument('answer')
@click.option('--topic', help='Topic/category')
@click.option('--book-id', type=int, help='Related book ID')
def add(question, answer, topic, book_id):
    """Create a new flashcard"""
    try:
        card = flashcard_manager.create_flashcard(question, answer, topic, book_id)
        rprint(f"[green]✓[/green] Created flashcard")
        rprint(f"  Topic: {topic or 'General'}")
        rprint(f"  ID: {card.id}")
    except Exception as e:
        rprint(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@flashcards.command()
@click.option('--topic', help='Filter by topic')
@click.option('--limit', default=20, help='Number of cards to review')
def review(topic, limit):
    """Review due flashcards"""
    cards = flashcard_manager.get_due_flashcards(topic, limit)
    
    if not cards:
        rprint("[green]🎉 No flashcards due! Great job![/green]")
        return
    
    rprint(f"[cyan]Review {len(cards)} flashcard(s)[/cyan]\n")
    
    reviewed = 0
    for i, card in enumerate(cards, 1):
        rprint(f"[bold]Card {i}/{len(cards)}[/bold]")
        rprint(f"[yellow]Q:[/yellow] {card.question}")
        input("Press Enter to see answer...")
        rprint(f"[green]A:[/green] {card.answer}\n")
        
        quality = click.prompt(
            "Rate your recall (0=forgot, 3=hard, 4=good, 5=easy)",
            type=click.IntRange(0, 5)
        )
        
        flashcard_manager.review_flashcard(card.id, quality)
        reviewed += 1
        rprint("")
    
    rprint(f"[green]✓[/green] Reviewed {reviewed} flashcard(s)")


@flashcards.command()
def stats():
    """Show flashcard statistics"""
    stats = flashcard_manager.get_stats()
    rprint(f"[cyan]📊 Flashcard Statistics[/cyan]")
    rprint(f"  Total: {stats['total']}")
    rprint(f"  Due for review: {stats['due']}")
    rprint(f"  Mastered: {stats['mastered']}")


# Study commands
@cli.group()
def study():
    """Track your study sessions"""
    pass


@study.command()
@click.option('--days', default=7, help='Number of days to show')
def stats(days):
    """Show study statistics"""
    stats = study_tracker.get_stats(days)
    
    rprint(f"[cyan]📈 Study Stats (Last {days} days)[/cyan]")
    rprint(f"  Total sessions: {stats['total_sessions']}")
    rprint(f"  Total time: {stats['total_hours']} hours ({stats['total_minutes']} min)")
    rprint(f"  Average session: {stats['avg_session_minutes']} min")
    rprint(f"  Notes created: {stats['total_notes']}")
    rprint(f"  Flashcards reviewed: {stats['total_flashcards_reviewed']}")
    rprint(f"  Topics covered: {stats['unique_topics']}")
    
    if stats['topics']:
        rprint("\n[cyan]Topics:[/cyan]")
        for topic in stats['topics']:
            rprint(f"  • {topic}")


# Search command
@cli.command()
@click.argument('query')
def search(query):
    """Search across all your content (books, notes, flashcards)"""
    results = search_service.search_all(query)
    
    if results['total'] == 0:
        rprint(f"[yellow]No results found for '{query}'[/yellow]")
        return
    
    rprint(f"[cyan]🔍 Found {results['total']} result(s) for '{query}'[/cyan]\n")
    
    # Show books
    if results['books']:
        rprint("[bold green]📚 Books:[/bold green]")
        for book in results['books']:
            rprint(f"  #{book.id} {book.title}")
            if book.author:
                rprint(f"      by {book.author}")
        rprint("")
    
    # Show notes
    if results['notes']:
        rprint("[bold green]📝 Notes:[/bold green]")
        for note in results['notes']:
            rprint(f"  #{note.id} {note.topic}")
            content_preview = note.content[:80] + "..." if len(note.content) > 80 else note.content
            rprint(f"      {content_preview}")
        rprint("")
    
    # Show flashcards
    if results['flashcards']:
        rprint("[bold green]🗂️  Flashcards:[/bold green]")
        for card in results['flashcards']:
            rprint(f"  #{card.id} {card.topic or 'General'}")
            rprint(f"      Q: {card.question[:60]}...")


# Dashboard command
@cli.command()
def dashboard():
    """Show your complete study dashboard"""
    from reference_library.models import Book, Note, Flashcard, StudySession, ExtractedPage, ExtractedImage, Chapter
    
    console.print("\n[bold cyan]📊 StudyBuddy Dashboard[/bold cyan]\n")
    
    # Library stats
    session = db_manager.get_session()
    try:
        book_count = session.query(Book).count()
        note_count = session.query(Note).count()
        flashcard_count = session.query(Flashcard).count()
        session_count = session.query(StudySession).count()
        extracted_pages = session.query(ExtractedPage).count()
        extracted_images = session.query(ExtractedImage).count()
        chapter_count = session.query(Chapter).count()
        
        # Create stats table
        table = Table(title="📈 Your Progress", show_header=True)
        table.add_column("Category", style="cyan", width=25)
        table.add_column("Count", justify="right", style="green", width=10)
        table.add_column("Status", style="yellow", width=35)
        
        table.add_row("Books", str(book_count), "📚 Textbooks in library")
        table.add_row("Extracted Pages", str(extracted_pages), "📄 Pages with extracted text")
        table.add_row("Extracted Images", str(extracted_images), "🖼️  Figures and diagrams")
        table.add_row("Generated Chapters", str(chapter_count), "📖 AI-synthesized chapters")
        table.add_row("Notes", str(note_count), "📝 Study notes created")
        table.add_row("Flashcards", str(flashcard_count), "🗂️  Cards for review")
        table.add_row("Study Sessions", str(session_count), "⏱️  Tracked sessions")
        
        console.print(table)
        
        # Content extraction status
        books_with_text = session.query(Book).filter(Book.text_extracted == True).count()
        books_with_images = session.query(Book).filter(Book.images_extracted == True).count()
        
        console.print(f"\n[cyan]Content Extraction:[/cyan]")
        console.print(f"  Books with extracted text: [green]{books_with_text}/{book_count}[/green]")
        console.print(f"  Books with extracted images: [green]{books_with_images}/{book_count}[/green]")
        
        # Flashcard stats
        flashcard_stats = flashcard_manager.get_stats()
        console.print(f"\n[cyan]Flashcards:[/cyan]")
        console.print(f"  Due for review: [yellow]{flashcard_stats['due']}[/yellow]")
        console.print(f"  Mastered: [green]{flashcard_stats['mastered']}[/green]")
        
        # Recent activity
        study_stats = study_tracker.get_stats(7)
        console.print(f"\n[cyan]Last 7 Days:[/cyan]")
        console.print(f"  Study time: [green]{study_stats['total_hours']} hours[/green]")
        console.print(f"  Topics: [yellow]{study_stats['unique_topics']}[/yellow]")
        
        if extracted_pages > 0:
            console.print(f"\n[green]✅ Content extracted! Ready to generate chapters.[/green]")
            console.print(f"   Run: [cyan]python3 cli/main.py chapter generate 'Subject' --book-ids 1[/cyan]")
        
        console.print("")
        
    finally:
        session.close()


# Chapter generation commands
@cli.group()
def chapter():
    """Generate comprehensive medical chapters from extracted content"""
    pass


@chapter.command()
@click.argument('subject')
@click.option('--book-ids', help='Comma-separated book IDs to use as sources', required=True)
@click.option('--search-terms', help='Additional search terms (comma-separated)')
def generate(subject, book_ids, search_terms):
    """Generate a comprehensive chapter on a subject"""
    try:
        # Parse book IDs
        book_id_list = [int(id.strip()) for id in book_ids.split(',')]
        
        # Parse search terms
        search_term_list = None
        if search_terms:
            search_term_list = [term.strip() for term in search_terms.split(',')]
        
        rprint(f"[cyan]Generating chapter: {subject}[/cyan]")
        rprint(f"  Using books: {book_id_list}")
        if search_term_list:
            rprint(f"  Search terms: {search_term_list}")
        
        # Generate chapter
        chapter_obj = chapter_synthesizer.generate_chapter(
            subject, book_id_list, search_term_list
        )
        
        rprint(f"\n[green]✓[/green] Chapter generated successfully!")
        rprint(f"  ID: {chapter_obj.id}")
        rprint(f"  Title: {chapter_obj.title}")
        rprint(f"  Source pages: {len(chapter_obj.source_pages.split(',')) if chapter_obj.source_pages else 0}")
        rprint(f"  Source images: {len(chapter_obj.source_images.split(',')) if chapter_obj.source_images else 0}")
        rprint(f"\n[yellow]View chapter with:[/yellow] python3 cli/main.py chapter view {chapter_obj.id}")
    
    except Exception as e:
        rprint(f"[red]✗[/red] Error: {e}")
        sys.exit(1)


@chapter.command()
def list():
    """List all generated chapters"""
    chapters = chapter_synthesizer.list_chapters()
    
    if not chapters:
        rprint("[yellow]No chapters generated yet. Create one with 'chapter generate'[/yellow]")
        return
    
    table = Table(title="📖 Generated Chapters")
    table.add_column("ID", style="cyan")
    table.add_column("Subject", style="green")
    table.add_column("Sources", justify="right")
    table.add_column("Images", justify="right")
    table.add_column("Created")
    
    for ch in chapters:
        source_count = len(ch.source_pages.split(',')) if ch.source_pages else 0
        image_count = len(ch.source_images.split(',')) if ch.source_images else 0
        
        table.add_row(
            str(ch.id),
            ch.title,
            str(source_count),
            str(image_count),
            ch.created_at.strftime("%Y-%m-%d")
        )
    
    console.print(table)


@chapter.command()
@click.argument('chapter_id', type=int)
def view(chapter_id):
    """View a generated chapter"""
    chapter_obj = chapter_synthesizer.get_chapter(chapter_id)
    
    if not chapter_obj:
        rprint(f"[red]Chapter {chapter_id} not found[/red]")
        sys.exit(1)
    
    console.print(f"\n[bold cyan]Chapter: {chapter_obj.title}[/bold cyan]\n")
    console.print(f"[yellow]Created:[/yellow] {chapter_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    console.print(f"[yellow]Model:[/yellow] {chapter_obj.ai_model_used}")
    console.print("\n" + "="*80 + "\n")
    console.print(chapter_obj.content)
    console.print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    cli()
