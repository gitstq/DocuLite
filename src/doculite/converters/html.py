"""
🌐 DocuLite HTML Converter Module

Converter for HTML documents.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import io
import re
import html

from .base import BaseConverter
from ..types import ConversionResult, DocumentType
from ..exceptions import ConversionError
from ..utils import clean_text


class HTMLConverter(BaseConverter):
    """Converter for HTML documents."""
    
    SUPPORTED_TYPES = [DocumentType.HTML, DocumentType.HTM]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.extract_links = config.get('extract_links', True)
        self.convert_tables = config.get('convert_tables', True)
        
    def _get_bs4(self):
        """Lazy load BeautifulSoup."""
        try:
            from bs4 import BeautifulSoup
            return BeautifulSoup
        except ImportError:
            raise ConversionError(
                "beautifulsoup4 and lxml are required for HTML conversion. "
                "Install with: pip install 'doculite[html]'"
            )
    
    def convert(self, file_path: Union[str, Path, io.BytesIO], **kwargs) -> ConversionResult:
        """
        Convert an HTML document to markdown.
        
        Args:
            file_path: Path to the HTML file or file-like object
            **kwargs: Additional options
            
        Returns:
            ConversionResult with markdown content
        """
        BeautifulSoup = self._get_bs4()
        
        try:
            if isinstance(file_path, (str, Path)):
                path = self.validate_file(file_path)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            else:
                file_path.seek(0)
                content = file_path.read().decode('utf-8', errors='ignore')
            
            soup = BeautifulSoup(content, 'lxml')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            metadata = {}
            links_info = []
            
            # Extract metadata from head
            head = soup.find('head')
            if head:
                title_tag = head.find('title')
                metadata['title'] = title_tag.get_text(strip=True) if title_tag else ""
                
                # Extract meta tags
                for meta in head.find_all('meta'):
                    name = meta.get('name', meta.get('property', ''))
                    content_val = meta.get('content', '')
                    if name and content_val:
                        metadata[name] = content_val
            
            # Extract links
            if self.extract_links:
                for a in soup.find_all('a', href=True):
                    links_info.append({
                        "text": a.get_text(strip=True),
                        "url": a['href'],
                    })
            
            # Convert content
            body = soup.find('body') or soup
            markdown = self._convert_element(body)
            
            # Post-process
            markdown = self.post_process_markdown(markdown)
            
            # Generate plain text
            text = re.sub(r'[#*_`\[\]|]', '', markdown)
            text = clean_text(text)
            
            return ConversionResult(
                markdown=markdown,
                text=text,
                metadata=metadata,
                pages=[],
                images=[],
                tables=[],
                links=links_info,
            )
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert HTML: {str(e)}",
                {"file_path": str(file_path) if isinstance(file_path, (str, Path)) else "stream"}
            )
    
    def _convert_element(self, element) -> str:
        """Convert a BeautifulSoup element to markdown."""
        parts = []
        
        for child in element.children:
            if child.name is None:
                # Text node
                text = str(child)
                if text.strip():
                    parts.append(html.unescape(text))
            else:
                # Element node
                md = self._convert_tag(child)
                if md:
                    parts.append(md)
        
        return ''.join(parts)
    
    def _convert_tag(self, tag) -> str:
        """Convert a single tag to markdown."""
        name = tag.name.lower()
        
        # Headings
        if name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(name[1])
            prefix = '#' * level
            text = self._get_text_content(tag)
            return f"\n\n{prefix} {text}\n\n"
        
        # Paragraphs
        if name == 'p':
            text = self._get_text_content(tag)
            return f"\n\n{text}\n\n"
        
        # Divs (treat as paragraphs if they have text)
        if name == 'div':
            text = self._get_text_content(tag)
            if text.strip():
                return f"\n\n{text}\n\n"
            return ""
        
        # Line breaks
        if name == 'br':
            return "\n"
        
        # Horizontal rules
        if name in ['hr']:
            return "\n\n---\n\n"
        
        # Lists
        if name == 'ul':
            return self._convert_list(tag, ordered=False)
        
        if name == 'ol':
            return self._convert_list(tag, ordered=True)
        
        if name == 'li':
            text = self._get_text_content(tag)
            return f"- {text}\n"
        
        # Tables
        if name == 'table' and self.convert_tables:
            return self._convert_table(tag)
        
        # Links
        if name == 'a':
            href = tag.get('href', '')
            text = self._get_text_content(tag)
            if href and text:
                return f"[{text}]({href})"
            return text
        
        # Images
        if name == 'img':
            src = tag.get('src', '')
            alt = tag.get('alt', '')
            return f"![{alt}]({src})"
        
        # Emphasis
        if name in ['em', 'i']:
            text = self._get_text_content(tag)
            return f"*{text}*"
        
        if name in ['strong', 'b']:
            text = self._get_text_content(tag)
            return f"**{text}**"
        
        # Code
        if name == 'code':
            text = self._get_text_content(tag)
            return f"`{text}`"
        
        if name == 'pre':
            text = self._get_text_content(tag)
            return f"\n\n```\n{text}\n```\n\n"
        
        # Blockquote
        if name == 'blockquote':
            text = self._get_text_content(tag)
            lines = text.split('\n')
            quoted = '\n'.join(f"> {line}" for line in lines)
            return f"\n\n{quoted}\n\n"
        
        # Default: process children
        return self._convert_element(tag)
    
    def _get_text_content(self, tag) -> str:
        """Get text content of a tag."""
        texts = []
        for desc in tag.descendants:
            if desc.name is None:
                texts.append(str(desc))
        return html.unescape(''.join(texts)).strip()
    
    def _convert_list(self, tag, ordered: bool = False) -> str:
        """Convert a list to markdown."""
        items = []
        
        for li in tag.find_all('li', recursive=False):
            text = self._get_text_content(li)
            if ordered:
                items.append(f"1. {text}")
            else:
                items.append(f"- {text}")
        
        return '\n' + '\n'.join(items) + '\n'
    
    def _convert_table(self, table) -> str:
        """Convert a table to markdown."""
        rows = []
        
        # Get header
        thead = table.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
                rows.append(headers)
        
        # Get body
        tbody = table.find('tbody') or table
        for tr in tbody.find_all('tr'):
            if tr.parent.name == 'thead':
                continue
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cells:
                rows.append(cells)
        
        if not rows:
            return ""
        
        # Build markdown table
        lines = []
        
        # Header
        header = rows[0]
        lines.append("| " + " | ".join(header) + " |")
        
        # Separator
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        
        # Data rows
        for row in rows[1:]:
            while len(row) < len(header):
                row.append("")
            row = row[:len(header)]
            lines.append("| " + " | ".join(row) + " |")
        
        return '\n' + '\n'.join(lines) + '\n'
