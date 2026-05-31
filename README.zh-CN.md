<div align="center">

# 🚀 DocuLite

**轻量级智能文档转换与内容提取引擎**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/gitstq/doculite/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-doculite-blue)](https://pypi.org/project/doculite/)

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

</div>

---

## 🎉 项目介绍

**DocuLite** 是一款轻量级、零依赖优先的 Python 库，旨在轻松将各种文档格式转换为干净、结构化的 Markdown。无论您是在构建基于大语言模型的应用、管理文档工作流，还是仅仅需要从文档中提取文本，DocuLite 都能提供优雅的解决方案。

### 它能做什么

- **万能转换**：将 PDF、DOCX、XLSX、HTML、图片等格式转换为 Markdown
- **智能提取**：提取表格、图片、元数据和结构化内容
- **OCR 支持**：使用 Tesseract OCR 将扫描文档和图片转换为文本
- **批量处理**：一条命令处理整个文件夹的文档
- **AI 就绪输出**：生成针对大语言模型优化的干净 Markdown

### 核心价值

在 AI 和大语言模型时代，干净的结构化文本比以往任何时候都更有价值。DocuLite 架起了传统文档格式与现代 AI 工作流之间的桥梁，实现：

- 📚 **知识库构建** - 将档案转换为可搜索的 Markdown
- 🤖 **LLM 训练数据准备** - 为模型微调提供干净、结构化的文本
- 🔍 **文档分析** - 从任何文档中提取洞察和元数据
- 📝 **内容迁移** - 在不同平台间无缝迁移内容

### 解决的痛点

| 问题 | DocuLite 解决方案 |
|---------|-------------------|
| 繁重的依赖拖慢项目 | 零依赖优先设计，按需安装额外组件 |
| 复杂的文档转换 API | 简单直观的 Python API 和 CLI |
| 扫描文档无文字内容 | 内置 OCR，支持多语言识别 |
| 表格提取混乱 | 结构化表格转 Markdown |
| 批量文档处理困难 | 一键批量转换 |
| 输出格式不一致 | 标准化的 Markdown 输出 |

---

## ✨ 核心功能

### 📄 多格式支持
- **文档**：PDF、DOCX、DOC
- **表格**：XLSX、XLS（支持表格提取）
- **网页**：HTML、HTM
- **图片**：PNG、JPG、JPEG、GIF、BMP、TIFF、WEBP（支持 OCR）
- **文本**：TXT、CSV、JSON、XML、MD

### 🔧 强大能力
- **🎯 智能格式检测** - 自动识别文件类型
- **📊 表格提取** - 将表格转换为 Markdown 格式
- **🖼️ 图片处理** - 提取和描述图片内容
- **🔍 OCR 引擎** - 基于 Tesseract 的文字识别
- **📦 批量处理** - 转换整个文件夹
- **🌐 URL 支持** - 直接从 URL 转换文档
- **📋 丰富元数据** - 提取文档属性和统计信息

### 🛠️ 开发者友好
- **简洁 API** - 简单、Pythonic 的接口设计
- **类型提示** - 完整的类型注解支持
- **精美 CLI** - 带进度指示器的漂亮终端输出
- **可扩展** - 轻松添加自定义转换器
- **文档完善** - 全面的文档字符串和示例

---

## 🚀 快速开始

### 安装

```bash
# 基础安装（最小依赖）
pip install doculite

# 带 PDF 支持
pip install doculite[pdf]

# 带 DOCX 支持
pip install doculite[docx]

# 带 OCR 支持
pip install doculite[ocr]

# 安装全部功能
pip install doculite[all]
```

### 基本用法

#### 命令行界面

```bash
# 转换单个文件
doculite convert document.pdf -o output.md

# 为扫描文档启用 OCR
doculite convert scan.pdf --ocr --ocr-language chi_sim

# 批量转换整个文件夹
doculite batch ./documents -o ./output

# 获取文档信息
doculite info document.docx

# 列出支持的格式
doculite formats

# 使用 AI 分析文档
doculite analyze report.pdf --type summary
```

#### Python API

```python
from doculite import DocuLite

# 初始化转换器
dl = DocuLite()

# 转换文档
result = dl.convert("document.pdf")
print(result.markdown)

# 访问元数据
print(f"页数: {len(result.pages)}")
print(f"表格数: {len(result.tables)}")
print(f"元数据: {result.metadata}")

# 批量转换
results = dl.convert_batch(["file1.pdf", "file2.docx"])

# 获取文档信息
info = dl.get_document_info("document.xlsx")
print(info)
```

---

## 📖 详细使用指南

### 配置选项

```python
from doculite import DocuLite

# 带选项配置
dl = DocuLite({
    'enable_ocr': True,           # 为图片/PDF 启用 OCR
    'ocr_language': 'chi_sim',    # OCR 语言代码
    'extract_images': True,       # 提取图片元数据
    'extract_tables': True,       # 提取表格数据
    'preserve_formatting': True,  # 保留原始格式
    'max_file_size': 100_000_000  # 最大文件大小 100MB
})
```

### 高级 CLI 用法

```bash
# 指定输出格式转换
doculite convert document.pdf -f json -o output.json

# 提取表格和图片
doculite convert report.pdf --extract-tables --extract-images

# OCR 识别中文
doculite convert scan.png --ocr --ocr-language chi_sim

# 静默模式（无进度输出）
doculite convert document.docx -q

# 使用短别名
dlite convert document.pdf
```

### 处理转换结果

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("document.pdf")

# 主要内容
markdown_content = result.markdown
plain_text = result.text

# 结构化数据
for page in result.pages:
    print(f"第 {page['number']} 页: {page['content'][:100]}...")

for table in result.tables:
    print(f"表格有 {table['rows']} 行")

# 元数据
author = result.metadata.get('author')
title = result.metadata.get('title')
creation_date = result.metadata.get('created_at')
```

### 批量处理

```python
from doculite import DocuLite
from pathlib import Path

dl = DocuLite({'enable_ocr': True})

# 处理文件夹中的所有 PDF
input_dir = Path("./documents")
pdf_files = list(input_dir.glob("*.pdf"))

results = dl.convert_batch(pdf_files, output_dir="./output")

# 处理结果
for result in results:
    if 'error' in result.metadata:
        print(f"错误: {result.metadata['error']}")
    else:
        print(f"已转换: {len(result.markdown)} 字符")
```

### AI 智能分析

```python
from doculite import DocuLite

dl = DocuLite()
result = dl.convert("article.pdf")

# 分析内容
analysis = dl.analyze_with_ai(result, analysis_type='all')

print(f"摘要: {analysis.summary}")
print(f"关键词: {', '.join(analysis.keywords)}")
print(f"阅读时间: {analysis.reading_time} 分钟")
```

---

## 💡 设计理念与路线图

### 为什么选择 DocuLite？

1. **零依赖优先**：核心功能无需繁重依赖，按需安装所需组件
2. **Markdown 作为通用格式**：Markdown 人类可读、AI 友好、 universally 支持
3. **Pythonic API**：简单直观，遵循 Python 最佳实践
4. **可扩展架构**：易于添加新转换器和扩展功能

### 架构原则

```
┌─────────────────────────────────────────────────────────┐
│                    DocuLite 核心                        │
├─────────────────────────────────────────────────────────┤
│  CLI 层  │  Python API  │  批处理器                     │
├─────────────────────────────────────────────────────────┤
│                   转换器注册表                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │
│  │   PDF   │ │  DOCX   │ │  XLSX   │ │  图片   │ ...  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘      │
├─────────────────────────────────────────────────────────┤
│              输出: Markdown / 文本 / JSON               │
└─────────────────────────────────────────────────────────┘
```

### 路线图

#### ✅ 已完成 (v1.0.0)
- [x] 核心转换引擎
- [x] PDF、DOCX、XLSX、HTML 支持
- [x] OCR 集成
- [x] 精美 CLI 输出
- [x] 批量处理
- [x] URL 支持

#### 🚧 进行中
- [ ] PPTX/PowerPoint 支持
- [ ] EPUB 支持
- [ ] 音频转录 (Whisper)
- [ ] 插件系统

#### 📋 计划中
- [ ] 云存储集成 (S3、GCS)
- [ ] Webhook 支持
- [ ] REST API 服务
- [ ] Docker 容器
- [ ] GUI 应用
- [ ] VS Code 扩展

---

## 📦 打包与部署

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/gitstq/doculite.git
cd doculite

# 安装构建依赖
pip install build hatchling

# 构建包
python -m build

# 本地安装
pip install -e .
```

### 发布到 PyPI

```bash
# 构建分发包
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

### Docker 部署

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
# 构建并运行
docker build -t doculite .
docker run -v $(pwd):/docs doculite convert /docs/document.pdf
```

---

## 🤝 贡献指南

我们欢迎贡献！以下是入门指南：

### 开发环境设置

```bash
# Fork 并克隆
git clone https://github.com/YOUR_USERNAME/doculite.git
cd doculite

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[all]"
pip install pytest black flake8 mypy

# 运行测试
pytest

# 格式化代码
black src/

# 类型检查
mypy src/
```

### 贡献流程

1. **Fork** 仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m '添加神奇功能'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **发起** Pull Request

### 贡献领域

- 🐛 **Bug 修复** - 帮助修复报告的问题
- ✨ **新转换器** - 添加对新文件格式的支持
- 📚 **文档** - 改进文档和示例
- 🌍 **翻译** - 翻译 README 和文档
- 🧪 **测试** - 提高测试覆盖率
- ⚡ **性能** - 优化转换速度

### 代码规范

- 遵循 PEP 8 代码风格指南
- 为所有函数添加类型提示
- 为公共 API 编写文档字符串
- 为新功能包含测试
- 根据需要更新文档

---

## 📄 许可证

DocuLite 基于 **MIT 许可证** 发布。

```
MIT 许可证

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

详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**由 DocuLite 团队用 ❤️ 打造**

[⭐ 在 GitHub 上 Star](https://github.com/gitstq/doculite) • [🐛 报告问题](https://github.com/gitstq/doculite/issues) • [💬 参与讨论](https://github.com/gitstq/doculite/discussions)

</div>
