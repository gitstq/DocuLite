"""
🚨 DocuLite Exceptions Module

Custom exception classes for DocuLite error handling.
"""


class DocuLiteError(Exception):
    """Base exception for all DocuLite errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self):
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class UnsupportedFormatError(DocuLiteError):
    """Raised when the file format is not supported."""
    pass


class ConversionError(DocuLiteError):
    """Raised when document conversion fails."""
    pass


class FileNotFoundError(DocuLiteError):
    """Raised when the specified file does not exist."""
    pass


class OCRError(DocuLiteError):
    """Raised when OCR processing fails."""
    pass


class AIAnalysisError(DocuLiteError):
    """Raised when AI content analysis fails."""
    pass


class PluginError(DocuLiteError):
    """Raised when plugin operations fail."""
    pass
