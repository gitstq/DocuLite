"""
🖼️ DocuLite Image Converter Module

Converter for image files with OCR support.
"""

from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import io
import re

from .base import BaseConverter
from ..types import ConversionResult, DocumentType
from ..exceptions import ConversionError, OCRError
from ..utils import clean_text


class ImageConverter(BaseConverter):
    """Converter for image files with OCR support."""
    
    SUPPORTED_TYPES = [
        DocumentType.PNG, DocumentType.JPG, DocumentType.JPEG,
        DocumentType.GIF, DocumentType.BMP, DocumentType.TIFF, DocumentType.WEBP
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.enable_ocr = config.get('enable_ocr', True)
        self.ocr_language = config.get('ocr_language', 'eng')
        self.extract_metadata = config.get('extract_metadata', True)
        
    def _get_pillow(self):
        """Lazy load Pillow."""
        try:
            from PIL import Image
            return Image
        except ImportError:
            raise ConversionError(
                "Pillow is required for image conversion. "
                "Install with: pip install 'doculite[ocr]'"
            )
    
    def _get_pytesseract(self):
        """Lazy load pytesseract."""
        try:
            import pytesseract
            return pytesseract
        except ImportError:
            raise ConversionError(
                "pytesseract is required for OCR. "
                "Install with: pip install 'doculite[ocr]'"
            )
    
    def convert(self, file_path: Union[str, Path, io.BytesIO], **kwargs) -> ConversionResult:
        """
        Convert an image to markdown (with optional OCR).
        
        Args:
            file_path: Path to the image file or file-like object
            **kwargs: Additional options
            
        Returns:
            ConversionResult with markdown content
        """
        Image = self._get_pillow()
        
        try:
            if isinstance(file_path, (str, Path)):
                path = self.validate_file(file_path)
                img = Image.open(str(path))
            else:
                file_path.seek(0)
                img = Image.open(file_path)
            
            metadata = {}
            
            # Extract image metadata
            if self.extract_metadata:
                metadata = {
                    "format": img.format,
                    "mode": img.mode,
                    "width": img.width,
                    "height": img.height,
                    "size": f"{img.width}x{img.height}",
                }
                
                # Extract EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    exif = img._getexif()
                    exif_data = {}
                    for tag_id, value in exif.items():
                        # Convert tag ID to name if possible
                        try:
                            from PIL.ExifTags import TAGS
                            tag_name = TAGS.get(tag_id, tag_id)
                            exif_data[tag_name] = str(value)
                        except:
                            exif_data[str(tag_id)] = str(value)
                    metadata['exif'] = exif_data
            
            # Perform OCR if enabled
            markdown_parts = []
            
            if self.enable_ocr:
                try:
                    ocr_text = self._perform_ocr(img)
                    if ocr_text.strip():
                        markdown_parts.append(f"## OCR Text Extraction\n\n{ocr_text}")
                    else:
                        markdown_parts.append("*No text detected in image*")
                except Exception as e:
                    markdown_parts.append(f"*OCR failed: {str(e)}*")
            
            # Add image reference
            if isinstance(file_path, (str, Path)):
                img_ref = f"![Image]({Path(file_path).name})"
            else:
                img_ref = "![Image](image)"
            
            markdown_parts.insert(0, img_ref)
            
            # Combine
            markdown = "\n\n".join(markdown_parts)
            markdown = self.post_process_markdown(markdown)
            
            # Generate plain text
            text = re.sub(r'[#*_`\[\]|]', '', markdown)
            text = clean_text(text)
            
            img.close()
            
            return ConversionResult(
                markdown=markdown,
                text=text,
                metadata=metadata,
                pages=[],
                images=[{"format": img.format, "size": metadata.get("size", "unknown")}],
                tables=[],
                links=[],
            )
            
        except Exception as e:
            raise ConversionError(
                f"Failed to convert image: {str(e)}",
                {"file_path": str(file_path) if isinstance(file_path, (str, Path)) else "stream"}
            )
    
    def _perform_ocr(self, img) -> str:
        """
        Perform OCR on an image.
        
        Args:
            img: PIL Image object
            
        Returns:
            Extracted text
        """
        pytesseract = self._get_pytesseract()
        
        try:
            # Convert image to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(img, lang=self.ocr_language)
            return clean_text(text)
            
        except Exception as e:
            raise OCRError(f"OCR processing failed: {str(e)}")
    
    def extract_text_with_boxes(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Extract text with bounding boxes from an image.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            List of dictionaries with text and bounding box info
        """
        Image = self._get_pillow()
        pytesseract = self._get_pytesseract()
        
        try:
            img = Image.open(str(file_path))
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get data with bounding boxes
            data = pytesseract.image_to_data(img, lang=self.ocr_language, output_type=pytesseract.Output.DICT)
            
            results = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Filter low confidence
                    results.append({
                        'text': data['text'][i],
                        'confidence': data['conf'][i],
                        'bbox': {
                            'x': data['left'][i],
                            'y': data['top'][i],
                            'width': data['width'][i],
                            'height': data['height'][i],
                        }
                    })
            
            img.close()
            return results
            
        except Exception as e:
            raise OCRError(f"Failed to extract text with boxes: {str(e)}")
