"""
🔄 DocuLite Converters Module

Document format converters for various file types.
"""

from .base import BaseConverter
from .pdf import PDFConverter
from .docx import DocxConverter
from .xlsx import XlsxConverter
from .html import HTMLConverter
from .image import ImageConverter
from .text import TextConverter

__all__ = [
    "BaseConverter",
    "PDFConverter",
    "DocxConverter",
    "XlsxConverter",
    "HTMLConverter",
    "ImageConverter",
    "TextConverter",
]

# Converter registry
CONVERTER_MAP = {
    "pdf": PDFConverter,
    "docx": DocxConverter,
    "doc": DocxConverter,
    "xlsx": XlsxConverter,
    "xls": XlsxConverter,
    "html": HTMLConverter,
    "htm": HTMLConverter,
    "txt": TextConverter,
    "csv": TextConverter,
    "json": TextConverter,
    "xml": TextConverter,
    "md": TextConverter,
    "markdown": TextConverter,
    "png": ImageConverter,
    "jpg": ImageConverter,
    "jpeg": ImageConverter,
    "gif": ImageConverter,
    "bmp": ImageConverter,
    "tiff": ImageConverter,
    "webp": ImageConverter,
}


def get_converter(file_type: str) -> type:
    """Get the appropriate converter for a file type."""
    file_type = file_type.lower().lstrip('.')
    if file_type not in CONVERTER_MAP:
        raise ValueError(f"No converter available for file type: {file_type}")
    return CONVERTER_MAP[file_type]
