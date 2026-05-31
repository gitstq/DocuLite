"""
📑 DocuLite PDF Converter Module

Converter for PDF documents.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import io
import re

from .base import BaseConverter
from ..types import ConversionResult, DocumentType, TextBlock
from ..exceptions import ConversionError
from ..utils import clean_text


class PDFConverter(BaseConverter):
    """Converter for PDF documents."""
    
    SUPPORTED_TYPES = [DocumentType.PDF]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._fitz = None
        
    def _get_fitz(self):
        """Lazy load PyMuPDF (fitz)."""
        if self._fitz is None:
            try:
                import fitz
                self._fitz = fitz
            except ImportError:
                raise ConversionError(
                    "PyMuPDF (fitz) is required for PDF conversion. "
                    "Install with: pip install 'doculite[pdf]'"
                )
        return self._fitz
    
    def convert(self, file_path: Union[str, Path, io.BytesIO], **kwargs) -> ConversionResult:
        """
        Convert a PDF document to markdown.
        
        Args:
            file_path: Path to the PDF file or file-like object
            **kwargs: Additional options
            
        Returns:
            ConversionResult with markdown content
        """
        fitz = self._get_fitz()
        
        try:
            if isinstance(file_path, (str, Path)):
                path = self.validate_file(file_path)
                doc = fitz.open(str(path))
            else:
                file_path.seek(0)
                doc = fitz.open(stream=file_path.read(), filetype="pdf")
            
            markdown_parts = []
            metadata = {}
            pages_info = []
            images_info = []
            tables_info = []
            links_info = []
            
            # Extract document metadata
            if doc.metadata:
                metadata = {
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", ""),
                    "subject": doc.metadata.get("subject", ""),
                    "creator": doc.metadata.get("creator", ""),
                    "producer": doc.metadata.get("producer", ""),
                    "creation_date": doc.metadata.get("creationDate", ""),
                    "modification_date": doc.metadata.get("modDate", ""),
                    "page_count": len(doc),
                }
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text()
                
                # Get page dimensions
                rect = page.rect
                page_info = {
                    "page_number": page_num + 1,
                    "width": rect.width,
                    "height": rect.height,
                    "rotation": page.rotation,
                }
                pages_info.append(page_info)
                
                # Extract links
                page_links = page.get_links()
                for link in page_links:
                    if "uri" in link:
                        links_info.append({
                            "page": page_num + 1,
                            "url": link["uri"],
                            "rect": link.get("from", None),
                        })
                
                # Extract images if enabled
                if self.extract_images:
                    image_list = page.get_images()
                    for img_index, img in enumerate(image_list, start=1):
                        images_info.append({
                            "page": page_num + 1,
                            "index": img_index,
                            "xref": img[0],
                            "width": img[2],
                            "height": img[3],
                        })
                
                # Process text content
                if text.strip():
                    processed_text = self._process_page_text(text, page_num + 1)
                    markdown_parts.append(processed_text)
            
            doc.close()
            
            # Combine all parts
            markdown = "\n\n".join(markdown_parts)
            markdown = self.post_process_markdown(markdown)
            
            # Generate plain text version
            text = re.sub(r'[#*_`\[\]]', '', markdown)
            text = clean_text(text)
            
            return ConversionResult(
                markdown=markdown,
                text=text,
                metadata=metadata,
                pages=pages_info,
                images=images_info,
                tables=tables_info,
                links=links_info,
            )
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert PDF: {str(e)}",
                {"file_path": str(file_path) if isinstance(file_path, (str, Path)) else "stream"}
            )
    
    def _process_page_text(self, text: str, page_number: int) -> str:
        """Process text from a single page."""
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect headers based on formatting
            line = self._detect_headers(line)
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _detect_headers(self, line: str) -> str:
        """Detect and format headers."""
        # All caps short lines might be headers
        if line.isupper() and len(line) < 100 and len(line) > 3:
            return f"## {line}"
        
        # Lines ending with numbers might be section headers
        if re.match(r'^[\d\.]+\s+', line) and len(line) < 200:
            level = line.count('.') + 1
            level = min(level, 6)
            prefix = '#' * level
            return f"{prefix} {line}"
        
        return line
    
    def extract_text_blocks(self, file_path: Union[str, Path]) -> List[TextBlock]:
        """
        Extract text blocks with positional information.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of TextBlock objects
        """
        fitz = self._get_fitz()
        blocks = []
        
        try:
            doc = fitz.open(str(file_path))
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Get text blocks with positions
                text_blocks = page.get_text("blocks")
                
                for block in text_blocks:
                    # block format: (x0, y0, x1, y1, text, block_no, block_type)
                    x0, y0, x1, y1, text, block_no, block_type = block
                    
                    if text.strip():
                        text_block = TextBlock(
                            text=clean_text(text),
                            page_number=page_num + 1,
                            bbox={"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0},
                            is_header=block_type == 1,  # 1 = header
                        )
                        blocks.append(text_block)
            
            doc.close()
            
        except Exception as e:
            raise ConversionError(f"Failed to extract text blocks: {str(e)}")
        
        return blocks
