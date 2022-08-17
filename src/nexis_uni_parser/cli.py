"""Command-line interface."""
from pathlib import Path

import typer

from .parser import convert_rtf_to_plain_text as convert_rtf_to_plain_text
from .parser import parse as parse


app = typer.Typer(name="nexis-uni", help="Parse NexisUni RTF files.")


@app.command()
def convert(rtf_file: Path = typer.Argument(None, help="Rich text file")) -> None:
    """Convert a rich text file to a plain text file."""
    newfile = convert_rtf_to_plain_text(rtf_file)
    typer.echo(f"New file created at: {newfile}")
