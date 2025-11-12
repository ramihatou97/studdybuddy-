# Content Extraction & Chapter Generation Features

## Overview

Added comprehensive PDF content extraction and AI-powered chapter synthesis capabilities as requested. The system now focuses on:

1. **Text Extraction** - Extract raw text from PDF pages using pdfplumber
2. **Image Extraction** - Extract figures, diagrams, and annotations from PDFs  
3. **Deep Search** - Search across all extracted content
4. **Chapter Synthesis** - Generate comprehensive medical-grade chapters from extracted materials

## New Features

### 1. PDF Content Extractor (`reference_library/pdf_extractor.py`)

- **Text extraction** using pdfplumber (superior to PyPDF2 for medical texts)
- **Image extraction** with coordinates and metadata
- **Table detection** for structured data
- **Metadata extraction** (title, author, dates)
- **Search within extracted content**

### 2. Enhanced Database Models (`reference_library/models.py`)

New tables added:
- `ExtractedPage` - Stores text content from each PDF page
- `ExtractedImage` - Stores extracted images with annotations
- `Chapter` - AI-generated comprehensive chapters

### 3. Chapter Synthesizer (`generation/chapter_synthesizer.py`)

- **Content collection** from multiple source books
- **Relevance-based organization** of extracted materials
- **AI synthesis** (with template fallback)
- **Source tracking** (pages and images used)
- **Chapter management** (create, list, view)

### 4. Updated Library Manager

- Automatic content extraction when adding books
- Stores extracted pages and images in database
- Tracks extraction status per book

### 5. Enhanced CLI Commands

New `chapter` command group:
- `chapter generate "Subject" --book-ids 1,2` - Generate chapter from books
- `chapter list` - List all generated chapters
- `chapter view <id>` - View chapter content

Updated `dashboard`:
- Shows extracted pages count
- Shows extracted images count  
- Shows generated chapters count
- Content extraction status

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     PDF Upload                          │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│            PDF Content Extractor                        │
│   • Text extraction (pdfplumber)                        │
│   • Image extraction with coordinates                   │
│   • Table detection                                     │
│   • Metadata extraction                                 │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│              Database Storage                           │
│   • ExtractedPage (text per page)                      │
│   • ExtractedImage (figures with annotations)          │
│   • Book (extraction status flags)                     │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│           Chapter Synthesizer                           │
│   • Collect relevant content (search-based)             │
│   • Organize by relevance                               │
│   • Synthesize comprehensive chapter                    │
│   • Track source pages & images                         │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│         Generated Medical Chapter                       │
│   • Comprehensive content                               │
│   • All relevant images                                 │
│   • Source attribution                                  │
│   • AI-enhanced (when available)                        │
└─────────────────────────────────────────────────────────┘
```

## Example Usage

```bash
# 1. Add a PDF (automatically extracts content)
python3 cli/main.py library add neurosurgery_atlas.pdf --title "Neurosurgery Atlas"

# 2. Check extraction status
python3 cli/main.py dashboard

# 3. Generate a comprehensive chapter
python3 cli/main.py chapter generate "Temporal Lobe Anatomy" --book-ids 1 --search-terms "temporal,anatomy,hippocampus"

# 4. List generated chapters
python3 cli/main.py chapter list

# 5. View chapter content
python3 cli/main.py chapter view 1
```

## Key Benefits

1. **Exhaustive Content Collection** - Captures all text, images, and annotations
2. **No Detail Lost** - Everything from source materials is preserved
3. **Image-Rich** - Particularly important for neuroanatomy and surgical steps
4. **Search-Based Synthesis** - Finds all relevant content automatically
5. **Source Tracking** - Always know which page/image content came from
6. **Comprehensive Chapters** - Medical-grade synthesis of all knowledge on a subject

## Technical Details

### Text Extraction
- Uses `pdfplumber` for high-quality text extraction
- Preserves layout and formatting
- Detects and extracts tables
- Word count tracking per page

### Image Extraction  
- Extracts images with coordinates (x, y, width, height)
- Saves as PNG at 150 DPI
- Tracks file size and metadata
- Supports annotation fields

### Chapter Generation
- Searches across all extracted pages
- Collects relevant images from those pages
- Organizes content by relevance
- Synthesizes into coherent chapter structure
- Template-based (with AI enhancement ready)

## Future Enhancements

- AI provider integration (Anthropic Claude, OpenAI GPT-4)
- OCR for image-based PDFs
- Automatic figure captioning
- Citation tracking
- Export to medical publishing formats
