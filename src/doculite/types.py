"""
📋 DocuLite Types Module

Type definitions and data models for DocuLite.
"""

from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class OutputFormat(Enum):
    """Supported output formats."""
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"
    HTML = "html"


class DocumentType(Enum):
    """Supported document types."""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    XLSX = "xlsx"
    XLS = "xls"
    PPTX = "pptx"
    PPT = "ppt"
    HTML = "html"
    HTM = "htm"
    TXT = "txt"
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    MD = "md"
    MARKDOWN = "markdown"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"
    WEBP = "webp"
    EPUB = "epub"
    ZIP = "zip"


@dataclass
class TextBlock:
    """Represents a block of text with metadata."""
    text: str
    page_number: Optional[int] = None
    bbox: Optional[Dict[str, float]] = None  # bounding box: {x, y, width, height}
    font_size: Optional[float] = None
    font_name: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False
    is_header: bool = False
    level: int = 0  # header level (1-6) or 0 for normal text


@dataclass
class ConversionResult:
    """Result of document conversion."""
    markdown: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    pages: List[Dict[str, Any]] = field(default_factory=list)
    images: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, Any]] = field(default_factory=list)
    
    def __repr__(self) -> str:
        return f"ConversionResult(markdown_length={len(self.markdown)}, pages={len(self.pages)})"


@dataclass
class DocumentInfo:
    """Information about a document."""
    file_path: Path
    file_size: int
    file_type: DocumentType
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    author: Optional[str] = None
    title: Optional[str] = None
    subject: Optional[str] = None


@dataclass
class AIAnalysisResult:
    """Result of AI content analysis."""
    summary: str
    keywords: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    sentiment: Optional[str] = None
    language: Optional[str] = None
    reading_time: Optional[int] = None  # in minutes
    difficulty_score: Optional[float] = None  # 0.0 - 1.0
    entities: List[Dict[str, Any]] = field(default_factory=list)
