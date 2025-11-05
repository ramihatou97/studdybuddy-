"""
PDF content extractor for medical reference materials.
Extracts text, images, figures, and annotations from PDFs.
"""
import io
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from PIL import Image
import pdfplumber
from pypdf import PdfReader

from utils.logger import logger
from utils.exceptions import FileError, InvalidFileFormatError


class PDFContentExtractor:
    """Extracts comprehensive content from PDF files including text, images, and figures."""
    
    def __init__(self, images_dir: Path):
        """
        Initialize PDF content extractor.
        
        Args:
            images_dir: Directory to save extracted images
        """
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_all_content(self, pdf_path: str, book_id: int) -> Dict[str, Any]:
        """
        Extract all content from a PDF: text, images, and metadata.
        
        Args:
            pdf_path: Path to PDF file
            book_id: Book ID for organizing extracted content
        
        Returns:
            Dictionary with extracted content
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileError(str(pdf_path), {"reason": "File not found"})
        
        logger.info(f"Extracting content from: {pdf_path.name}")
        
        # Extract text content
        text_content = self._extract_text(pdf_path)
        
        # Extract images and figures
        images = self._extract_images(pdf_path, book_id)
        
        # Extract metadata
        metadata = self._extract_metadata(pdf_path)
        
        result = {
            "text_content": text_content,
            "images": images,
            "metadata": metadata,
            "total_pages": len(text_content),
            "total_images": len(images),
            "pdf_path": str(pdf_path)
        }
        
        logger.info(f"Extracted {len(text_content)} pages and {len(images)} images")
        
        return result
    
    def _extract_text(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Extract text content from all pages using pdfplumber.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of dictionaries with page text and metadata
        """
        pages_content = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text
                    text = page.extract_text() or ""
                    
                    # Extract tables
                    tables = page.extract_tables()
                    
                    # Get page dimensions
                    width = page.width
                    height = page.height
                    
                    pages_content.append({
                        "page_number": page_num,
                        "text": text,
                        "tables": tables,
                        "width": width,
                        "height": height,
                        "word_count": len(text.split()) if text else 0
                    })
                    
                    if page_num % 10 == 0:
                        logger.debug(f"Processed {page_num} pages")
        
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            raise InvalidFileFormatError(str(pdf_path), "Valid PDF with readable text")
        
        return pages_content
    
    def _extract_images(self, pdf_path: Path, book_id: int) -> List[Dict[str, Any]]:
        """
        Extract all images and figures from the PDF.
        
        Args:
            pdf_path: Path to PDF file
            book_id: Book ID for organizing images
        
        Returns:
            List of dictionaries with image metadata and paths
        """
        images = []
        book_images_dir = self.images_dir / f"book_{book_id}"
        book_images_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Use pdfplumber for image extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract images from page
                    page_images = page.images
                    
                    for img_idx, img_info in enumerate(page_images):
                        try:
                            # Get image coordinates and dimensions
                            x0, y0 = img_info.get('x0', 0), img_info.get('top', 0)
                            x1, y1 = img_info.get('x1', 0), img_info.get('bottom', 0)
                            width = x1 - x0
                            height = y1 - y0
                            
                            # Save image information
                            image_filename = f"page_{page_num}_img_{img_idx + 1}.png"
                            image_path = book_images_dir / image_filename
                            
                            # Try to extract the image
                            try:
                                # Crop the image from the page
                                im = page.crop((x0, y0, x1, y1))
                                img_obj = im.to_image(resolution=150)
                                img_obj.save(str(image_path), format="PNG")
                                
                                images.append({
                                    "page_number": page_num,
                                    "image_index": img_idx + 1,
                                    "filename": image_filename,
                                    "path": str(image_path),
                                    "x0": x0,
                                    "y0": y0,
                                    "width": width,
                                    "height": height,
                                    "size_kb": image_path.stat().st_size / 1024 if image_path.exists() else 0
                                })
                                
                                logger.debug(f"Extracted image from page {page_num}")
                            
                            except Exception as img_err:
                                logger.warning(f"Could not extract image from page {page_num}: {img_err}")
                        
                        except Exception as e:
                            logger.warning(f"Error processing image on page {page_num}: {e}")
                            continue
        
        except Exception as e:
            logger.error(f"Error extracting images from {pdf_path}: {e}")
        
        return images
    
    def _extract_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract PDF metadata.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Dictionary with metadata
        """
        metadata = {}
        
        try:
            reader = PdfReader(str(pdf_path))
            
            # Basic metadata
            if reader.metadata:
                metadata = {
                    "title": reader.metadata.get("/Title", ""),
                    "author": reader.metadata.get("/Author", ""),
                    "subject": reader.metadata.get("/Subject", ""),
                    "creator": reader.metadata.get("/Creator", ""),
                    "producer": reader.metadata.get("/Producer", ""),
                    "creation_date": str(reader.metadata.get("/CreationDate", "")),
                    "modification_date": str(reader.metadata.get("/ModDate", ""))
                }
            
            # Page count
            metadata["page_count"] = len(reader.pages)
        
        except Exception as e:
            logger.warning(f"Could not extract metadata: {e}")
            metadata = {"error": str(e)}
        
        return metadata
    
    def search_in_extracted_content(self, text_content: List[Dict[str, Any]], 
                                    query: str) -> List[Dict[str, Any]]:
        """
        Search for text in extracted content.
        
        Args:
            text_content: List of page content dictionaries
            query: Search query
        
        Returns:
            List of matching pages with context
        """
        results = []
        query_lower = query.lower()
        
        for page in text_content:
            text = page.get("text", "").lower()
            
            if query_lower in text:
                # Find context around the match
                idx = text.find(query_lower)
                start = max(0, idx - 100)
                end = min(len(text), idx + len(query) + 100)
                context = page["text"][start:end]
                
                results.append({
                    "page_number": page["page_number"],
                    "context": context,
                    "full_text": page["text"]
                })
        
        return results
