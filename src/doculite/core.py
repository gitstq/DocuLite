"""
🎯 DocuLite Core Module

Main conversion engine for DocuLite.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Type
import io

from .types import ConversionResult, DocumentType, OutputFormat, AIAnalysisResult
from .exceptions import DocuLiteError, UnsupportedFormatError, ConversionError
from .utils import detect_file_type, get_file_info, is_url
from .converters import get_converter, BaseConverter


class DocuLite:
    """
    🚀 DocuLite - Lightweight Intelligent Document Conversion Engine
    
    Main class for converting documents to Markdown and other formats.
    
    Example:
        >>> from doculite import DocuLite
        >>> dl = DocuLite()
        >>> result = dl.convert("document.pdf")
        >>> print(result.markdown)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DocuLite converter.
        
        Args:
            config: Optional configuration dictionary with options:
                - enable_ocr: Enable OCR for images and PDFs (default: False)
                - ocr_language: OCR language code (default: 'eng')
                - preserve_formatting: Keep original formatting (default: True)
                - extract_images: Extract image metadata (default: False)
                - extract_tables: Extract table data (default: True)
                - max_file_size: Maximum file size in bytes (default: 100MB)
        """
        self.config = config or {}
        self._converters: Dict[str, BaseConverter] = {}
        
        # Set default config values
        self.config.setdefault('enable_ocr', False)
        self.config.setdefault('ocr_language', 'eng')
        self.config.setdefault('preserve_formatting', True)
        self.config.setdefault('extract_images', False)
        self.config.setdefault('extract_tables', True)
        self.config.setdefault('max_file_size', 100 * 1024 * 1024)  # 100MB
    
    def convert(
        self,
        file_path: Union[str, Path, io.BytesIO],
        output_format: OutputFormat = OutputFormat.MARKDOWN,
        **kwargs
    ) -> ConversionResult:
        """
        Convert a document to the specified format.
        
        Args:
            file_path: Path to the file, URL, or file-like object
            output_format: Desired output format (default: MARKDOWN)
            **kwargs: Additional conversion options
            
        Returns:
            ConversionResult with converted content and metadata
            
        Raises:
            UnsupportedFormatError: If file format is not supported
            ConversionError: If conversion fails
        """
        # Handle URLs
        if isinstance(file_path, str) and is_url(file_path):
            file_path = self._download_url(file_path)
        
        # Detect file type
        if isinstance(file_path, (str, Path)):
            file_type = detect_file_type(file_path)
        else:
            # For streams, file_type must be provided
            file_type = kwargs.get('file_type')
            if not file_type:
                raise ConversionError("file_type must be specified when converting from stream")
        
        # Get or create converter
        converter = self._get_converter(file_type.value)
        
        # Perform conversion
        result = converter.convert(file_path, **kwargs)
        
        # Post-process based on output format
        if output_format == OutputFormat.TEXT:
            result.markdown = result.text
        elif output_format == OutputFormat.JSON:
            # JSON is handled by the result object structure
            pass
        
        return result
    
    def convert_batch(
        self,
        file_paths: List[Union[str, Path]],
        output_dir: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> List[ConversionResult]:
        """
        Convert multiple documents in batch.
        
        Args:
            file_paths: List of file paths to convert
            output_dir: Optional directory to save converted files
            **kwargs: Additional conversion options
            
        Returns:
            List of ConversionResult objects
        """
        results = []
        
        for file_path in file_paths:
            try:
                result = self.convert(file_path, **kwargs)
                results.append(result)
                
                # Save to output directory if specified
                if output_dir:
                    self._save_result(result, file_path, output_dir)
                    
            except Exception as e:
                # Create error result
                error_result = ConversionResult(
                    markdown=f"",
                    text=f"",
                    metadata={"error": str(e), "file_path": str(file_path)}
                )
                results.append(error_result)
        
        return results
    
    def get_document_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a document without converting.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with document information
        """
        info = get_file_info(file_path)
        
        try:
            file_type = detect_file_type(file_path)
            info['detected_type'] = file_type.value
            
            # Get converter-specific info
            converter = self._get_converter(file_type.value)
            metadata = converter.extract_metadata(file_path)
            info.update(metadata)
            
        except UnsupportedFormatError:
            info['detected_type'] = 'unknown'
        
        return info
    
    def analyze_with_ai(
        self,
        result: ConversionResult,
        analysis_type: str = 'summary'
    ) -> AIAnalysisResult:
        """
        Analyze converted content using AI.
        
        Args:
            result: ConversionResult from convert()
            analysis_type: Type of analysis (summary, keywords, entities)
            
        Returns:
            AIAnalysisResult with analysis results
        """
        text = result.text or result.markdown
        
        if not text:
            return AIAnalysisResult(summary="No content to analyze")
        
        # Simple analysis without external AI dependencies
        # In a real implementation, this could use LLM APIs
        return self._perform_local_analysis(text, analysis_type)
    
    def _get_converter(self, file_type: str) -> BaseConverter:
        """Get or create a converter for a file type."""
        if file_type not in self._converters:
            converter_class = get_converter(file_type)
            self._converters[file_type] = converter_class(self.config)
        
        return self._converters[file_type]
    
    def _download_url(self, url: str) -> Path:
        """Download a file from URL to temporary location."""
        import tempfile
        import urllib.request
        import urllib.error
        
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                urllib.request.urlretrieve(url, tmp.name)
                return Path(tmp.name)
        except urllib.error.URLError as e:
            raise ConversionError(f"Failed to download URL: {url}", {"error": str(e)})
    
    def _save_result(
        self,
        result: ConversionResult,
        original_path: Union[str, Path],
        output_dir: Union[str, Path]
    ) -> Path:
        """Save conversion result to file."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        original_name = Path(original_path).stem
        output_path = output_dir / f"{original_name}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.markdown)
        
        return output_path
    
    def _perform_local_analysis(self, text: str, analysis_type: str) -> AIAnalysisResult:
        """Perform local text analysis without external AI."""
        from .utils import count_words, estimate_reading_time, extract_urls, extract_emails
        
        # Calculate basic stats
        word_count = count_words(text)
        reading_time = estimate_reading_time(text)
        
        # Extract URLs and emails
        urls = extract_urls(text)
        emails = extract_emails(text)
        
        # Simple keyword extraction (most frequent words)
        import re
        from collections import Counter
        
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        # Filter common stop words
        stop_words = {'this', 'that', 'with', 'from', 'they', 'have', 'were', 'been', 'their', 'would', 'there', 'could', 'should'}
        words = [w for w in words if w not in stop_words]
        top_words = [word for word, count in Counter(words).most_common(10)]
        
        # Create summary (first few sentences)
        sentences = re.split(r'[.!?]+', text)
        summary = '. '.join(s.strip() for s in sentences[:3] if s.strip())
        if summary:
            summary += '.'
        
        return AIAnalysisResult(
            summary=summary or "Document content",
            keywords=top_words,
            topics=[],
            reading_time=reading_time,
            entities=[
                {"type": "url", "values": urls[:10]},
                {"type": "email", "values": emails[:10]},
            ]
        )
    
    @property
    def supported_formats(self) -> List[str]:
        """Get list of supported file formats."""
        from .converters import CONVERTER_MAP
        return list(CONVERTER_MAP.keys())
    
    def __repr__(self) -> str:
        return f"DocuLite(config={self.config})"
