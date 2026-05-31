"""
📄 DocuLite Base Converter Module

Abstract base class for all document converters.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import io

from ..types import ConversionResult, DocumentType, TextBlock
from ..exceptions import ConversionError, FileNotFoundError
from ..utils import detect_file_type, get_file_info, clean_text


class BaseConverter(ABC):
    """Abstract base class for document converters."""
    
    SUPPORTED_TYPES: List[DocumentType] = []
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the converter.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.enable_ocr = self.config.get('enable_ocr', False)
        self.ocr_language = self.config.get('ocr_language', 'eng')
        self.preserve_formatting = self.config.get('preserve_formatting', True)
        self.extract_images = self.config.get('extract_images', False)
        self.extract_tables = self.config.get('extract_tables', True)
    
    @abstractmethod
    def convert(self, file_path: Union[str, Path, io.BytesIO], **kwargs) -> ConversionResult:
        """
        Convert a document to markdown.
        
        Args:
            file_path: Path to the file or file-like object
            **kwargs: Additional conversion options
            
        Returns:
            ConversionResult with markdown and metadata
            
        Raises:
            ConversionError: If conversion fails
        """
        pass
    
    def convert_stream(self, stream: io.BytesIO, file_type: DocumentType, **kwargs) -> ConversionResult:
        """
        Convert a document from a stream.
        
        Args:
            stream: File-like object containing the document
            file_type: Type of the document
            **kwargs: Additional conversion options
            
        Returns:
            ConversionResult with markdown and metadata
        """
        raise NotImplementedError("Stream conversion not implemented for this converter")
    
    def validate_file(self, file_path: Union[str, Path]) -> Path:
        """
        Validate that a file exists and is readable.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Validated Path object
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not path.is_file():
            raise FileNotFoundError(f"Path is not a file: {file_path}")
        
        return path
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Extract metadata from a document.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with metadata
        """
        return get_file_info(file_path)
    
    def post_process_markdown(self, markdown: str) -> str:
        """
        Post-process markdown content.
        
        Args:
            markdown: Raw markdown content
            
        Returns:
            Cleaned markdown content
        """
        # Clean text
        markdown = clean_text(markdown)
        
        # Fix common markdown issues
        markdown = self._fix_markdown_issues(markdown)
        
        return markdown
    
    def _fix_markdown_issues(self, markdown: str) -> str:
        """Fix common markdown formatting issues."""
        import re
        
        # Ensure headers have space after #
        markdown = re.sub(r'^(#{1,6})([^\s#])', r'\1 \2', markdown, flags=re.MULTILINE)
        
        # Fix multiple consecutive blank lines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Ensure code blocks have proper line breaks
        markdown = re.sub(r'```\n\n+', '```\n', markdown)
        markdown = re.sub(r'\n\n+```', '\n```', markdown)
        
        # Fix list formatting
        markdown = re.sub(r'^\s*[-*+]\s+', lambda m: m.group().rstrip() + ' ', markdown, flags=re.MULTILINE)
        
        return markdown.strip()
    
    def _text_blocks_to_markdown(self, blocks: List[TextBlock]) -> str:
        """Convert text blocks to markdown."""
        sections = []
        current_section = []
        
        for block in blocks:
            text = block.text.strip()
            if not text:
                continue
            
            if block.is_header:
                # Flush current section
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
                
                # Add header with proper level
                prefix = '#' * min(block.level, 6) if block.level > 0 else '#'
                sections.append(f"{prefix} {text}")
            else:
                current_section.append(text)
        
        # Flush remaining section
        if current_section:
            sections.append('\n'.join(current_section))
        
        return '\n\n'.join(sections)
