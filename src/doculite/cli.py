"""
⌨️ DocuLite CLI Module

Command-line interface for DocuLite.
"""

import sys
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .core import DocuLite
from .types import OutputFormat
from .exceptions import DocuLiteError


console = Console()


def print_banner():
    """Print DocuLite banner."""
    banner = Text()
    banner.append("🚀 ", style="bold yellow")
    banner.append("DocuLite", style="bold cyan")
    banner.append(f" v{__version__}", style="dim")
    banner.append(" - Lightweight Document Conversion Engine", style="dim")
    console.print(banner)
    console.print()


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version information')
@click.pass_context
def main(ctx, version):
    """🚀 DocuLite - Lightweight Intelligent Document Conversion Engine"""
    if version:
        console.print(f"DocuLite version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("[dim]Use --help for available commands[/dim]")


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'text', 'json'], case_sensitive=False),
              default='markdown', help='Output format')
@click.option('--ocr/--no-ocr', default=False, help='Enable OCR for images and PDFs')
@click.option('--ocr-language', default='eng', help='OCR language (e.g., eng, chi_sim)')
@click.option('--extract-images', is_flag=True, help='Extract image metadata')
@click.option('--extract-tables', is_flag=True, default=True, help='Extract table data')
@click.option('--quiet', '-q', is_flag=True, help='Suppress progress output')
def convert(
    input_path: str,
    output: Optional[str],
    output_format: str,
    ocr: bool,
    ocr_language: str,
    extract_images: bool,
    extract_tables: bool,
    quiet: bool
):
    """Convert a document to Markdown or other formats"""
    if not quiet:
        print_banner()
    
    input_path = Path(input_path)
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.with_suffix('.md')
    
    # Configure DocuLite
    config = {
        'enable_ocr': ocr,
        'ocr_language': ocr_language,
        'extract_images': extract_images,
        'extract_tables': extract_tables,
    }
    
    dl = DocuLite(config)
    
    try:
        if not quiet:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(f"Converting {input_path.name}...", total=None)
                
                format_map = {
                    'markdown': OutputFormat.MARKDOWN,
                    'text': OutputFormat.TEXT,
                    'json': OutputFormat.JSON,
                }
                result = dl.convert(input_path, output_format=format_map[output_format])
                
                progress.update(task, completed=True)
        else:
            format_map = {
                'markdown': OutputFormat.MARKDOWN,
                'text': OutputFormat.TEXT,
                'json': OutputFormat.JSON,
            }
            result = dl.convert(input_path, output_format=format_map[output_format])
        
        # Write output
        output_path.write_text(result.markdown, encoding='utf-8')
        
        if not quiet:
            # Display results
            console.print(f"\n[green]✓[/green] Converted: [cyan]{input_path.name}[/cyan]")
            console.print(f"[green]✓[/green] Output: [cyan]{output_path.absolute()}[/cyan]")
            
            # Show metadata
            if result.metadata:
                console.print("\n[bold]Document Metadata:[/bold]")
                meta_table = Table(show_header=False, box=None)
                meta_table.add_column("Key", style="dim")
                meta_table.add_column("Value")
                
                for key, value in result.metadata.items():
                    if value and str(value).strip():
                        meta_table.add_row(key, str(value)[:50])
                
                console.print(meta_table)
            
            # Show stats
            console.print(f"\n[dim]Characters: {len(result.markdown)} | Pages: {len(result.pages)} | Tables: {len(result.tables)}[/dim]")
        
    except DocuLiteError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--output-dir', '-o', type=click.Path(), required=True, help='Output directory')
@click.option('--ocr/--no-ocr', default=False, help='Enable OCR')
@click.option('--quiet', '-q', is_flag=True, help='Suppress progress output')
def batch(input_dir: str, output_dir: str, ocr: bool, quiet: bool):
    """Batch convert all documents in a directory"""
    if not quiet:
        print_banner()
    
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all supported files
    supported_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.html', '.htm', '.txt', '.md', '.png', '.jpg', '.jpeg']
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in supported_extensions]
    
    if not files:
        console.print("[yellow]No supported files found in directory[/yellow]")
        return
    
    config = {'enable_ocr': ocr}
    dl = DocuLite(config)
    
    success_count = 0
    error_count = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for file_path in files:
            task = progress.add_task(f"Converting {file_path.name}...", total=None)
            
            try:
                result = dl.convert(file_path)
                output_path = output_dir / f"{file_path.stem}.md"
                output_path.write_text(result.markdown, encoding='utf-8')
                success_count += 1
                progress.update(task, description=f"[green]✓[/green] {file_path.name}")
                
            except Exception as e:
                error_count += 1
                progress.update(task, description=f"[red]✗[/red] {file_path.name}")
    
    console.print(f"\n[green]✓[/green] Successfully converted: {success_count}")
    if error_count > 0:
        console.print(f"[red]✗[/red] Failed: {error_count}")
    console.print(f"Output directory: [cyan]{output_dir.absolute()}[/cyan]")


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
def info(file_path: str):
    """Display document information without converting"""
    print_banner()
    
    file_path = Path(file_path)
    dl = DocuLite()
    
    try:
        info = dl.get_document_info(file_path)
        
        console.print(Panel.fit(
            f"[bold cyan]{file_path.name}[/bold cyan]",
            title="Document Information"
        ))
        
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="bold")
        table.add_column("Value")
        
        for key, value in info.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(table)
        
    except DocuLiteError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def formats():
    """List all supported file formats"""
    print_banner()
    
    dl = DocuLite()
    formats_list = dl.supported_formats
    
    console.print("[bold]Supported File Formats:[/bold]\n")
    
    # Group by category
    categories = {
        'Documents': ['pdf', 'docx', 'doc'],
        'Spreadsheets': ['xlsx', 'xls'],
        'Web': ['html', 'htm'],
        'Text': ['txt', 'csv', 'json', 'xml', 'md', 'markdown'],
        'Images': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'],
    }
    
    for category, exts in categories.items():
        supported = [ext for ext in exts if ext in formats_list]
        if supported:
            console.print(f"[bold]{category}:[/bold] {', '.join(f'.{ext}' for ext in supported)}")
    
    console.print(f"\n[dim]Total: {len(formats_list)} formats supported[/dim]")


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--type', '-t', 'analysis_type', 
              type=click.Choice(['summary', 'keywords', 'all'], case_sensitive=False),
              default='all', help='Type of analysis')
def analyze(file_path: str, analysis_type: str):
    """Analyze document content using AI"""
    print_banner()
    
    file_path = Path(file_path)
    dl = DocuLite()
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing document...", total=None)
            
            result = dl.convert(file_path)
            analysis = dl.analyze_with_ai(result, analysis_type)
            
            progress.update(task, completed=True)
        
        console.print(Panel.fit(
            f"[bold cyan]{file_path.name}[/bold cyan]",
            title="Document Analysis"
        ))
        
        if analysis.summary:
            console.print(f"\n[bold]Summary:[/bold]\n{analysis.summary}")
        
        if analysis.keywords:
            console.print(f"\n[bold]Keywords:[/bold] {', '.join(analysis.keywords)}")
        
        if analysis.reading_time:
            console.print(f"\n[bold]Estimated Reading Time:[/bold] {analysis.reading_time} minutes")
        
        if analysis.entities:
            console.print(f"\n[bold]Extracted Entities:[/bold]")
            for entity in analysis.entities:
                if entity.get('values'):
                    console.print(f"  [dim]{entity['type']}:[/dim] {len(entity['values'])} found")
        
    except DocuLiteError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
