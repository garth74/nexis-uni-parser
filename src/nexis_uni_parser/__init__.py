"""Convert NexisUni rtf files into tabular data."""

from .parser import convert_rtf_to_plain_text as convert_rtf_to_plain_text
from .parser import parse as parse


__all__ = ["convert_rtf_to_plain_text", "parse"]
