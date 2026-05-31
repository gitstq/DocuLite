"""
📄 DocuLite Text Converter Module

Converter for plain text and code files.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union
import io
import json
import csv

from .base import BaseConverter
from ..types import ConversionResult, DocumentType
from ..exceptions import ConversionError
from ..utils import clean_text, format_markdown_table


class TextConverter(BaseConverter):
    """Converter for plain text files."""
    
    SUPPORTED_TYPES = [
        DocumentType.TXT, DocumentType.CSV, DocumentType.JSON,
        DocumentType.XML, DocumentType.MARKDOWN
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.detect_code = config.get('detect_code', True)
        self.max_preview_lines = config.get('max_preview_lines', 50)
    
    def convert(self, file_path: Union[str, Path, io.BytesIO], **kwargs) -> ConversionResult:
        """
        Convert a text file to markdown.
        
        Args:
            file_path: Path to the text file or file-like object
            **kwargs: Additional options
            
        Returns:
            ConversionResult with markdown content
        """
        try:
            if isinstance(file_path, (str, Path)):
                path = self.validate_file(file_path)
                file_type = Path(path).suffix.lower().lstrip('.')
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            else:
                file_path.seek(0)
                content = file_path.read().decode('utf-8', errors='ignore')
                file_type = kwargs.get('file_type', 'txt')
            
            metadata = {
                "file_type": file_type,
                "char_count": len(content),
                "line_count": content.count('\n') + 1,
            }
            
            # Process based on file type
            if file_type == 'csv':
                markdown = self._convert_csv(content)
            elif file_type == 'json':
                markdown = self._convert_json(content)
            elif file_type == 'xml':
                markdown = self._convert_xml(content)
            elif file_type in ['md', 'markdown']:
                markdown = content  # Already markdown
            else:
                markdown = self._convert_plain_text(content, file_type)
            
            # Post-process
            markdown = self.post_process_markdown(markdown)
            
            # Generate plain text
            text = content
            
            return ConversionResult(
                markdown=markdown,
                text=text,
                metadata=metadata,
                pages=[],
                images=[],
                tables=[],
                links=[],
            )
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert text file: {str(e)}",
                {"file_path": str(file_path) if isinstance(file_path, (str, Path)) else "stream"}
            )
    
    def _convert_csv(self, content: str) -> str:
        """Convert CSV content to markdown table."""
        lines = content.strip().split('\n')
        if not lines:
            return ""
        
        try:
            reader = csv.reader(lines)
            rows = list(reader)
            
            if not rows:
                return ""
            
            # Use first row as header
            headers = rows[0]
            data = rows[1:]
            
            # Limit rows for preview
            if len(data) > self.max_preview_lines:
                data = data[:self.max_preview_lines]
                note = f"\n\n*Note: Showing {self.max_preview_lines} of {len(rows)-1} rows*"
            else:
                note = ""
            
            return format_markdown_table(headers, data) + note
            
        except Exception as e:
            # Fall back to plain text
            return f"```csv\n{content}\n```"
    
    def _convert_json(self, content: str) -> str:
        """Convert JSON content to formatted markdown."""
        try:
            data = json.loads(content)
            
            # Pretty print JSON
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Wrap in code block
            return f"```json\n{formatted}\n```"
            
        except json.JSONDecodeError:
            # Invalid JSON, treat as plain text
            return f"```\n{content}\n```"
    
    def _convert_xml(self, content: str) -> str:
        """Convert XML content to markdown."""
        # Try to pretty print XML
        try:
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(content)
            pretty = dom.toprettyxml(indent="  ")
            # Remove empty lines
            pretty = '\n'.join(line for line in pretty.split('\n') if line.strip())
            return f"```xml\n{pretty}\n```"
        except:
            # Fall back to plain text
            return f"```xml\n{content}\n```"
    
    def _convert_plain_text(self, content: str, file_type: str) -> str:
        """Convert plain text to markdown."""
        # Detect if it might be code
        if self.detect_code and self._is_likely_code(content, file_type):
            lang = self._detect_language(file_type)
            return f"```{lang}\n{content}\n```"
        
        # Regular text - just clean it
        return clean_text(content)
    
    def _is_likely_code(self, content: str, file_type: str) -> bool:
        """Heuristic to detect if content is code."""
        code_indicators = [
            'def ', 'class ', 'import ', 'from ',
            'function', 'var ', 'const ', 'let ',
            '#include', 'using namespace',
            'public static', 'private ', 'protected ',
        ]
        
        content_lower = content.lower()
        indicator_count = sum(1 for ind in code_indicators if ind in content_lower)
        
        # If more than 2 indicators found, likely code
        return indicator_count >= 2
    
    def _detect_language(self, file_type: str) -> str:
        """Detect programming language from file extension."""
        lang_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'jsx': 'jsx',
            'tsx': 'tsx',
            'java': 'java',
            'c': 'c',
            'cpp': 'cpp',
            'h': 'c',
            'hpp': 'cpp',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust',
            'rb': 'ruby',
            'php': 'php',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
            'r': 'r',
            'm': 'matlab',
            'sh': 'bash',
            'bash': 'bash',
            'zsh': 'bash',
            'ps1': 'powershell',
            'sql': 'sql',
            'yaml': 'yaml',
            'yml': 'yaml',
            'toml': 'toml',
            'ini': 'ini',
            'cfg': 'ini',
        }
        
        return lang_map.get(file_type.lower(), 'text')
