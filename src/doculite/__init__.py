"""
🚀 DocuLite - Lightweight Intelligent Document Conversion & Content Extraction Engine

A zero-dependency-first Python library for converting various document formats to Markdown
with optional AI-powered content analysis.

Basic Usage:
    >>> from doculite import DocuLite
    >>> converter = DocuLite()
    >>> result = converter.convert("document.pdf")
    >>> print(result.markdown)

Author: DocuLite Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "DocuLite Team"
__license__ = "MIT"

from .core import DocuLite, ConversionResult
from .exceptions import (
    DocuLiteError,
    UnsupportedFormatError,
    ConversionError,
    FileNotFoundError,
    OCRError,
)

__all__ = [
    "DocuLite",
    "ConversionResult",
    "DocuLiteError",
    "UnsupportedFormatError",
    "ConversionError",
    "FileNotFoundError",
    "OCRError",
]
