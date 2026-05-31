<div align="center">

# 🚀 DocuLite

**輕量級智能文件轉換與內容提取引擎**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/gitstq/doculite/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-doculite-blue)](https://pypi.org/project/doculite/)

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

</div>

---

## 🎉 專案介紹

**DocuLite** 是一款輕量級、零依賴優先的 Python 函式庫，旨在輕鬆將各種文件格式轉換為乾淨、結構化的 Markdown。無論您是在建構基於大型語言模型的應用、管理文件工作流程，還是僅僅需要從文件中提取文字，DocuLite 都能提供優雅的解決方案。

### 它能做什麼

- **萬能轉換**：將 PDF、DOCX、XLSX、HTML、圖片等格式轉換為 Markdown
- **智能提取**：提取表格、圖片、元資料和結構化內容
- **OCR 支援**：使用 Tesseract OCR 將掃描文件和圖片轉換為文字
- **批次處理**：一條指令處理整個資料夾的文件
- **AI 就緒輸出**：生成針對大型語言模型優化的乾淨 Markdown

### 核心價值

在 AI 和大型語言模型時代，乾淨的結構化文字比以往任何時候都更有價值。DocuLite 架起了傳統文件格式與現代 AI 工作流程之間的橋樑，實現：

- 📚 **知識庫建構** - 將檔案轉換為可搜尋的 Markdown
- 🤖 **LLM 訓練資料準備** - 為模型微調提供乾淨、結構化的文字
- 🔍 **文件分析** - 從任何文件中提取洞察和元資料
- 📝 **內容遷移** - 在不同平台間無縫遷移內容

### 解決的痛點

| 問題 | DocuLite 解決方案 |
|---------|-------------------|
| 繁重的依賴拖慢專案 | 零依賴優先設計，按需安裝額外元件 |
| 複雜的文件轉換 API | 簡單直觀的 Python API 和 CLI |
| 掃描文件無文字內容 | 內建 OCR，支援多語言辨識 |
| 表格提取混亂 | 結構化表格轉 Markdown |
| 批次文件處理困難 | 一鍵批次轉換 |
| 輸出格式不一致 | 標準化的 Markdown 輸出 |

---

## ✨ 核心功能

### 📄 多格式支援
- **文件**：PDF、DOCX、DOC
- **試算表**：XLSX、XLS（支援表格提取）
- **網頁**：HTML、HTM
- **圖片**：PNG、JPG、JPEG、GIF、BMP、TIFF、WEBP（支援 OCR）
- **文字**：TXT、CSV、JSON、XML、MD

### 🔧 強大能力
- **🎯 智能格式偵測** - 自動識別檔案類型
- **📊 表格提取** - 將表格轉換為 Markdown 格式
- **🖼️ 圖片處理** - 提取和描述圖片內容
- **🔍 OCR 引擎** - 基於 Tesseract 的文字辨識
- **📦 批次處理** - 轉換整個資料夾
- **🌐 URL 支援** - 直接從 URL 轉換文件
- **📋 豐富元資料** - 提取文件屬性和統計資訊

### 🛠️ 開發者友善
- **簡潔 API** - 簡單、Pythonic 的介面設計
- **類型提示** - 完整的類型註解支援
- **精美 CLI** - 帶進度指示器的漂亮終端輸出
- **可擴展** - 輕鬆添加自訂轉換器
- **文件完善** - 全面的文件字串和範例

---

## 🚀 快速開始

### 安裝

```bash
# 基礎安裝（最小依賴）
pip install doculite

# 帶 PDF 支援
pip install doculite[pdf]

# 帶 DOCX 支援
pip install doculite[docx]

# 帶 OCR 支援
pip install doculite[ocr]

# 安裝全部功能
pip install doculite[all]
```

### 基本用法

#### 命令列介面

```bash
# 轉換單個檔案
doculite convert document.pdf -o output.md

# 為掃描文件啟用 OCR
doculite convert scan.pdf --ocr --ocr-language chi_tra

# 批次轉換整個資料夾
doculite batch ./documents -o ./output

# 取得文件資訊
doculite info document.docx

# 列出支援的格式
doculite formats

# 使用 AI 分析文件
doculite analyze report.pdf --type summary
```

#### Python API

```python
from doculite import DocuLite

# 初始化轉換器
dl = DocuLite()

# 轉換文件
result = dl.convert("document.pdf")
print(result.markdown)

# 存取元資料
print(f"頁數: {len(result.pages)}")
print(f"表格數: {len(result.tables)}")
print(f"元資料: {result.metadata}")

# 批次轉換
results = dl.convert_batch(["file1.pdf", "file2.docx"])

# 取得文件資訊
info = dl.get_document_info("document.xlsx")
print(info)
```

---

## 📖 詳細使用指南

### 配置選項

```python
from doculite import DocuLite

# 帶選項配置
dl = DocuLite({
    'enable_ocr': True,           # 為圖片/PDF 啟用 OCR
    'ocr_language': 'chi_tra',    # OCR 語言代碼
    'extract_images': True,       # 提取圖片元資料
    'extract_tables': True,       # 提取表格資料
    'preserve_formatting': True,  # 保留原始格式
    'max_file_size': 100_000_000  # 最大檔案大小 100MB
})
```

### 進階 CLI 用法

```bash
# 指定輸出格式轉換
doculite convert document.pdf -f json -o output.json

# 提取表格和圖片
doculite convert report.pdf --extract-tables --extract-images

# OCR 辨識繁體中文
doculite convert scan.png --ocr --ocr-language chi_tra

# 靜默模式（無進度輸出）
doculite convert document.docx -q

# 使用短別名
dlite convert document.pdf
```

### 處理轉換結果

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("document.pdf")

# 主要內容
markdown_content = result.markdown
plain_text = result.text

# 結構化資料
for page in result.pages:
    print(f"第 {page['number']} 頁: {page['content'][:100]}...")

for table in result.tables:
    print(f"表格有 {table['rows']} 列")

# 元資料
author = result.metadata.get('author')
title = result.metadata.get('title')
creation_date = result.metadata.get('created_at')
```

### 批次處理

```python
from doculite import DocuLite
from pathlib import Path

dl = DocuLite({'enable_ocr': True})

# 處理資料夾中的所有 PDF
input_dir = Path("./documents")
pdf_files = list(input_dir.glob("*.pdf"))

results = dl.convert_batch(pdf_files, output_dir="./output")

# 處理結果
for result in results:
    if 'error' in result.metadata:
        print(f"錯誤: {result.metadata['error']}")
    else:
        print(f"已轉換: {len(result.markdown)} 字元")
```

### AI 智能分析

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("article.pdf")

# 分析內容
analysis = dl.analyze_with_ai(result, analysis_type='all')

print(f"摘要: {analysis.summary}")
print(f"關鍵詞: {', '.join(analysis.keywords)}")
print(f"閱讀時間: {analysis.reading_time} 分鐘")
```

---

## 💡 設計理念與路線圖

### 為什麼選擇 DocuLite？

1. **零依賴優先**：核心功能無需繁重依賴，按需安裝所需元件
2. **Markdown 作為通用格式**：Markdown 人類可讀、AI 友善、普遍支援
3. **Pythonic API**：簡單直觀，遵循 Python 最佳實踐
4. **可擴展架構**：易於添加新轉換器和擴展功能

### 架構原則

```
┌─────────────────────────────────────────────────────────┐
│                    DocuLite 核心                        │
├─────────────────────────────────────────────────────────┤
│  CLI 層  │  Python API  │  批次處理器                    │
├─────────────────────────────────────────────────────────┤
│                   轉換器註冊表                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │   PDF   │ │  DOCX   │ │  XLSX   │ │  圖片   │ ...  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
├─────────────────────────────────────────────────────────┤
│              輸出: Markdown / 文字 / JSON               │
└─────────────────────────────────────────────────────────┘
```

### 路線圖

#### ✅ 已完成 (v1.0.0)
- [x] 核心轉換引擎
- [x] PDF、DOCX、XLSX、HTML 支援
- [x] OCR 整合
- [x] 精美 CLI 輸出
- [x] 批次處理
- [x] URL 支援

#### 🚧 進行中
- [ ] PPTX/PowerPoint 支援
- [ ] EPUB 支援
- [ ] 音訊轉錄 (Whisper)
- [ ] 外掛系統

#### 📋 計劃中
- [ ] 雲端儲存整合 (S3、GCS)
- [ ] Webhook 支援
- [ ] REST API 服務
- [ ] Docker 容器
- [ ] GUI 應用
- [ ] VS Code 擴充功能

---

## 📦 打包與部署

### 從原始碼建構

```bash
# 克隆倉庫
git clone https://github.com/gitstq/doculite.git
cd doculite

# 安裝建構依賴
pip install build hatchling

# 建構套件
python -m build

# 本地安裝
pip install -e .
```

### 發布到 PyPI

```bash
# 建構發布套件
python -m build

# 上傳到 PyPI
python -m twine upload dist/*
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-chi-tra \
    && rm -rf /var/lib/apt/lists/*

RUN pip install doculite[all]

ENTRYPOINT ["doculite"]
```

```bash
# 建構並執行
docker build -t doculite .
docker run -v $(pwd):/docs doculite convert /docs/document.pdf
```

---

## 🤝 貢獻指南

我們歡迎貢獻！以下是入門指南：

### 開發環境設定

```bash
# Fork 並克隆
git clone https://github.com/YOUR_USERNAME/doculite.git
cd doculite

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝開發依賴
pip install -e ".[all]"
pip install pytest black flake8 mypy

# 執行測試
pytest

# 格式化程式碼
black src/

# 類型檢查
mypy src/
```

### 貢獻流程

1. **Fork** 倉庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m '添加神奇功能'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **發起** Pull Request

### 貢獻領域

- 🐛 **Bug 修復** - 幫助修復報告的問題
- ✨ **新轉換器** - 添加對新文件格式的支援
- 📚 **文件** - 改進文件和範例
- 🌍 **翻譯** - 翻譯 README 和文件
- 🧪 **測試** - 提高測試覆蓋率
- ⚡ **效能** - 優化轉換速度

### 程式碼規範

- 遵循 PEP 8 程式碼風格指南
- 為所有函式添加類型提示
- 為公共 API 撰寫文件字串
- 為新功能包含測試
- 根據需要更新文件

---

## 📄 授權條款

DocuLite 基於 **MIT 授權條款** 發布。

```
MIT 授權條款

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

詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**由 DocuLite 團隊用 ❤️ 打造**

[⭐ 在 GitHub 上 Star](https://github.com/gitstq/doculite) • [🐛 報告問題](https://github.com/gitstq/doculite/issues) • [💬 參與討論](https://github.com/gitstq/doculite/discussions)

</div>
