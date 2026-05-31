"""
🛠️ DocuLite Utilities Module

Utility functions for file handling, format detection, and text processing.
"""

import os
import re
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
from urllib.parse import urlparse

from .types import DocumentType
from .exceptions import FileNotFoundError, UnsupportedFormatError


# File extension to DocumentType mapping
EXTENSION_MAP = {
    '.pdf': DocumentType.PDF,
    '.docx': DocumentType.DOCX,
    '.doc': DocumentType.DOC,
    '.xlsx': DocumentType.XLSX,
    '.xls': DocumentType.XLS,
    '.pptx': DocumentType.PPTX,
    '.ppt': DocumentType.PPT,
    '.html': DocumentType.HTML,
    '.htm': DocumentType.HTM,
    '.txt': DocumentType.TXT,
    '.csv': DocumentType.CSV,
    '.json': DocumentType.JSON,
    '.xml': DocumentType.XML,
    '.md': DocumentType.MARKDOWN,
    '.markdown': DocumentType.MARKDOWN,
    '.png': DocumentType.PNG,
    '.jpg': DocumentType.JPG,
    '.jpeg': DocumentType.JPEG,
    '.gif': DocumentType.GIF,
    '.bmp': DocumentType.BMP,
    '.tiff': DocumentType.TIFF,
    '.webp': DocumentType.WEBP,
    '.epub': DocumentType.EPUB,
    '.zip': DocumentType.ZIP,
}


def detect_file_type(file_path: Union[str, Path]) -> DocumentType:
    """
    Detect the document type from file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        DocumentType enum value
        
    Raises:
        FileNotFoundError: If file doesn't exist
        UnsupportedFormatError: If format is not supported
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    ext = path.suffix.lower()
    
    if ext not in EXTENSION_MAP:
        # Try to detect by mimetype
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type:
            mime_to_ext = {
                'application/pdf': '.pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
                'application/msword': '.doc',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
                'application/vnd.ms-excel': '.xls',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
                'application/vnd.ms-powerpoint': '.ppt',
                'text/html': '.html',
                'text/plain': '.txt',
                'text/csv': '.csv',
                'application/json': '.json',
                'application/xml': '.xml',
                'text/markdown': '.md',
                'image/png': '.png',
                'image/jpeg': '.jpg',
                'image/gif': '.gif',
                'image/bmp': '.bmp',
                'image/tiff': '.tiff',
                'image/webp': '.webp',
                'application/epub+zip': '.epub',
                'application/zip': '.zip',
            }
            if mime_type in mime_to_ext:
                ext = mime_to_ext[mime_type]
    
    if ext not in EXTENSION_MAP:
        raise UnsupportedFormatError(
            f"Unsupported file format: {ext}",
            {"file_path": str(file_path), "detected_extension": ext}
        )
    
    return EXTENSION_MAP[ext]


def get_file_info(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Get basic file information.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    path = Path(file_path)
    stat = path.stat()
    
    return {
        "file_path": str(path.absolute()),
        "file_name": path.name,
        "file_size": stat.st_size,
        "file_size_human": format_file_size(stat.st_size),
        "extension": path.suffix.lower(),
        "modified_time": stat.st_mtime,
        "created_time": stat.st_ctime,
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext
    return filename.strip()


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove zero-width characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.findall(text)


def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text."""
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return email_pattern.findall(text)


def is_url(string: str) -> bool:
    """Check if string is a valid URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_words(text: str) -> int:
    """Count words in text (supports multiple languages)."""
    # Remove punctuation and split
    cleaned = re.sub(r'[^\w\s]', '', text)
    words = cleaned.split()
    return len(words)


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes."""
    word_count = count_words(text)
    return max(1, round(word_count / words_per_minute))


def format_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """Format data as a Markdown table."""
    if not headers or not rows:
        return ""
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header row
    header_cells = [h.ljust(col_widths[i]) for i, h in enumerate(headers)]
    lines.append("| " + " | ".join(header_cells) + " |")
    
    # Separator
    sep_cells = ["-" * col_widths[i] for i in range(len(headers))]
    lines.append("| " + " | ".join(sep_cells) + " |")
    
    # Data rows
    for row in rows:
        row_cells = [str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)]
        lines.append("| " + " | ".join(row_cells) + " |")
    
    return "\n".join(lines)


def merge_markdown_sections(sections: List[str]) -> str:
    """Merge multiple markdown sections with proper spacing."""
    cleaned_sections = []
    for section in sections:
        section = section.strip()
        if section:
            cleaned_sections.append(section)
    
    return "\n\n".join(cleaned_sections)
