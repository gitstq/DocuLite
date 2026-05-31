<div align="center">

# 🚀 DocuLite

**Lightweight Intelligent Document Conversion & Content Extraction Engine**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/gitstq/doculite/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-doculite-blue)](https://pypi.org/project/doculite/)

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

</div>

---

## 🎉 Project Introduction

**DocuLite** is a lightweight, zero-dependency-first Python library designed to effortlessly convert various document formats into clean, structured Markdown. Whether you're building LLM-powered applications, managing documentation workflows, or simply need to extract text from documents, DocuLite provides an elegant solution.

### What It Does

- **Universal Conversion**: Transform PDF, DOCX, XLSX, HTML, images, and more into Markdown
- **Intelligent Extraction**: Extract tables, images, metadata, and structured content
- **OCR Support**: Convert scanned documents and images to text using Tesseract OCR
- **Batch Processing**: Process entire directories of documents in one command
- **AI-Ready Output**: Generate clean Markdown optimized for LLM consumption

### Core Value

In the age of AI and Large Language Models, clean structured text is more valuable than ever. DocuLite bridges the gap between legacy document formats and modern AI workflows, enabling:

- 📚 **Knowledge Base Construction** - Convert archives into searchable Markdown
- 🤖 **LLM Training Data Preparation** - Clean, structured text for model fine-tuning
- 🔍 **Document Analysis** - Extract insights and metadata from any document
- 📝 **Content Migration** - Seamlessly move content between platforms

### Pain Points Solved

| Problem | DocuLite Solution |
|---------|-------------------|
| Heavy dependencies slowing your project | Zero-dependency-first design with optional extras |
| Complex document conversion APIs | Simple, intuitive Python API and CLI |
| Scanned documents without text | Built-in OCR with multi-language support |
| Messy table extraction | Structured table-to-Markdown conversion |
| Batch document processing | One-command batch conversion |
| Inconsistent output formats | Standardized Markdown output |

---

## ✨ Core Features

### 📄 Multi-Format Support
- **Documents**: PDF, DOCX, DOC
- **Spreadsheets**: XLSX, XLS (with table extraction)
- **Web**: HTML, HTM
- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP (with OCR)
- **Text**: TXT, CSV, JSON, XML, MD

### 🔧 Powerful Capabilities
- **🎯 Smart Format Detection** - Automatic file type detection
- **📊 Table Extraction** - Convert tables to Markdown format
- **🖼️ Image Processing** - Extract and describe images
- **🔍 OCR Engine** - Tesseract-powered text recognition
- **📦 Batch Processing** - Convert entire directories
- **🌐 URL Support** - Convert documents directly from URLs
- **📋 Rich Metadata** - Extract document properties and statistics

### 🛠️ Developer-Friendly
- **Clean API** - Simple, Pythonic interface
- **Type Hints** - Full type annotation support
- **Rich CLI** - Beautiful terminal output with progress indicators
- **Extensible** - Easy to add custom converters
- **Well Documented** - Comprehensive docstrings and examples

---

## 🚀 Quick Start

### Installation

```bash
# Basic installation (minimal dependencies)
pip install doculite

# With PDF support
pip install doculite[pdf]

# With DOCX support
pip install doculite[docx]

# With OCR support
pip install doculite[ocr]

# Install everything
pip install doculite[all]
```

### Basic Usage

#### Command Line Interface

```bash
# Convert a single file
doculite convert document.pdf -o output.md

# Enable OCR for scanned documents
doculite convert scan.pdf --ocr --ocr-language eng

# Batch convert entire directory
doculite batch ./documents -o ./output

# Get document information
doculite info document.docx

# List supported formats
doculite formats

# Analyze document with AI
doculite analyze report.pdf --type summary
```

#### Python API

```python
from doculite import DocuLite

# Initialize converter
dl = DocuLite()

# Convert a document
result = dl.convert("document.pdf")
print(result.markdown)

# Access metadata
print(f"Pages: {len(result.pages)}")
print(f"Tables: {len(result.tables)}")
print(f"Metadata: {result.metadata}")

# Batch conversion
results = dl.convert_batch(["file1.pdf", "file2.docx"])

# Get document info
info = dl.get_document_info("document.xlsx")
print(info)
```

---

## 📖 Detailed Usage Guide

### Configuration Options

```python
from doculite import DocuLite

# Configure with options
dl = DocuLite({
    'enable_ocr': True,           # Enable OCR for images/PDFs
    'ocr_language': 'eng',        # OCR language code
    'extract_images': True,       # Extract image metadata
    'extract_tables': True,       # Extract table data
    'preserve_formatting': True,  # Keep original formatting
    'max_file_size': 100_000_000  # 100MB max file size
})
```

### Advanced CLI Usage

```bash
# Convert with specific output format
doculite convert document.pdf -f json -o output.json

# Extract tables and images
doculite convert report.pdf --extract-tables --extract-images

# OCR with Chinese language support
doculite convert scan.png --ocr --ocr-language chi_sim

# Quiet mode (no progress output)
doculite convert document.docx -q

# Using the short alias
dlite convert document.pdf
```

### Working with Conversion Results

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("document.pdf")

# Main content
markdown_content = result.markdown
plain_text = result.text

# Structured data
for page in result.pages:
    print(f"Page {page['number']}: {page['content'][:100]}...")

for table in result.tables:
    print(f"Table with {table['rows']} rows")

# Metadata
author = result.metadata.get('author')
title = result.metadata.get('title')
creation_date = result.metadata.get('created_at')
```

### Batch Processing

```python
from doculite import DocuLite
from pathlib import Path

dl = DocuLite({'enable_ocr': True})

# Process all PDFs in a directory
input_dir = Path("./documents")
pdf_files = list(input_dir.glob("*.pdf"))

results = dl.convert_batch(pdf_files, output_dir="./output")

# Handle results
for result in results:
    if 'error' in result.metadata:
        print(f"Error: {result.metadata['error']}")
    else:
        print(f"Converted: {len(result.markdown)} characters")
```

### AI-Powered Analysis

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("article.pdf")

# Analyze content
analysis = dl.analyze_with_ai(result, analysis_type='all')

print(f"Summary: {analysis.summary}")
print(f"Keywords: {', '.join(analysis.keywords)}")
print(f"Reading time: {analysis.reading_time} minutes")
```

---

## 💡 Design Philosophy & Roadmap

### Why DocuLite?

1. **Zero-Dependency-First**: Core functionality works without heavy dependencies. Install only what you need.
2. **Markdown as Universal Format**: Markdown is human-readable, AI-friendly, and universally supported.
3. **Pythonic API**: Simple, intuitive, and follows Python best practices.
4. **Extensible Architecture**: Easy to add new converters and extend functionality.

### Architecture Principles

```
┌─────────────────────────────────────────────────────────┐
│                    DocuLite Core                        │
├─────────────────────────────────────────────────────────┤
│  CLI Layer  │  Python API  │  Batch Processor          │
├─────────────────────────────────────────────────────────┤
│              Converter Registry                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │   PDF   │ │  DOCX   │ │  XLSX   │ │  Image  │ ...  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
├─────────────────────────────────────────────────────────┤
│              Output: Markdown / Text / JSON             │
└─────────────────────────────────────────────────────────┘
```

### Roadmap

#### ✅ Completed (v1.0.0)
- [x] Core conversion engine
- [x] PDF, DOCX, XLSX, HTML support
- [x] OCR integration
- [x] CLI with rich output
- [x] Batch processing
- [x] URL support

#### 🚧 In Progress
- [ ] PPTX/PowerPoint support
- [ ] EPUB support
- [ ] Audio transcription (Whisper)
- [ ] Plugin system

#### 📋 Planned
- [ ] Cloud storage integration (S3, GCS)
- [ ] Webhook support
- [ ] REST API server
- [ ] Docker container
- [ ] GUI application
- [ ] VS Code extension

---

## 📦 Packaging & Deployment

### Building from Source

```bash
# Clone repository
git clone https://github.com/gitstq/doculite.git
cd doculite

# Install build dependencies
pip install build hatchling

# Build package
python -m build

# Install locally
pip install -e .
```

### Publishing to PyPI

```bash
# Build distribution
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    && rm -rf /var/lib/apt/lists/*

RUN pip install doculite[all]

ENTRYPOINT ["doculite"]
```

```bash
# Build and run
docker build -t doculite .
docker run -v $(pwd):/docs doculite convert /docs/document.pdf
```

---

## 🤝 Contributing Guide

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/doculite.git
cd doculite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[all]"
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

### Contribution Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Areas for Contribution

- 🐛 **Bug Fixes** - Help fix reported issues
- ✨ **New Converters** - Add support for new file formats
- 📚 **Documentation** - Improve docs and examples
- 🌍 **Translations** - Translate README and docs
- 🧪 **Tests** - Increase test coverage
- ⚡ **Performance** - Optimize conversion speed

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write docstrings for public APIs
- Include tests for new features
- Update documentation as needed

---

## 📄 License

DocuLite is released under the **MIT License**.

```
MIT License

Copyright (c) 2026 DocuLite Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

See [LICENSE](LICENSE) for full details.

---

<div align="center">

**Made with ❤️ by the DocuLite Team**

[⭐ Star us on GitHub](https://github.com/gitstq/doculite) • [🐛 Report Issues](https://github.com/gitstq/doculite/issues) • [💬 Discussions](https://github.com/gitstq/doculite/discussions)

</div>
