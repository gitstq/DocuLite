"""
🧪 DocuLite Core Tests

Tests for the core DocuLite functionality.
"""

import pytest
from pathlib import Path
import tempfile

from doculite import DocuLite, ConversionResult
from doculite.exceptions import UnsupportedFormatError, FileNotFoundError


class TestDocuLite:
    """Test cases for DocuLite class."""
    
    def test_initialization(self):
        """Test DocuLite initialization."""
        dl = DocuLite()
        assert dl.config is not None
        assert dl.config['enable_ocr'] == False
        
    def test_initialization_with_config(self):
        """Test DocuLite initialization with custom config."""
        config = {'enable_ocr': True, 'ocr_language': 'chi_sim'}
        dl = DocuLite(config)
        assert dl.config['enable_ocr'] == True
        assert dl.config['ocr_language'] == 'chi_sim'
    
    def test_supported_formats(self):
        """Test getting supported formats."""
        dl = DocuLite()
        formats = dl.supported_formats
        assert isinstance(formats, list)
        assert 'pdf' in formats
        assert 'docx' in formats
        assert 'txt' in formats
    
    def test_get_document_info_nonexistent(self):
        """Test getting info for non-existent file."""
        dl = DocuLite()
        with pytest.raises(FileNotFoundError):
            dl.get_document_info("/nonexistent/file.pdf")


class TestTextConversion:
    """Test text file conversion."""
    
    def test_convert_txt_file(self):
        """Test converting a text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello World\nThis is a test.")
            temp_path = f.name
        
        try:
            dl = DocuLite()
            result = dl.convert(temp_path)
            
            assert isinstance(result, ConversionResult)
            assert "Hello World" in result.markdown
            assert "test" in result.text
        finally:
            Path(temp_path).unlink()
    
    def test_convert_json_file(self):
        """Test converting a JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"name": "test", "value": 123}')
            temp_path = f.name
        
        try:
            dl = DocuLite()
            result = dl.convert(temp_path)
            
            assert isinstance(result, ConversionResult)
            assert "```json" in result.markdown
            assert '"name": "test"' in result.markdown
        finally:
            Path(temp_path).unlink()


class TestUtils:
    """Test utility functions."""
    
    def test_file_info(self):
        """Test getting file info."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            from doculite.utils import get_file_info
            info = get_file_info(temp_path)
            
            assert 'file_path' in info
            assert 'file_size' in info
            assert 'extension' in info
            assert info['extension'] == '.txt'
        finally:
            Path(temp_path).unlink()
