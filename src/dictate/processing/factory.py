"""Factory for creating text processors based on config."""

from __future__ import annotations

from dictate.config import Config
from dictate.processing.base import TextProcessor


def create_text_processor(config: Config) -> TextProcessor:
    """Create and return the appropriate text processor."""
    if config.text_processor == "ollama":
        from dictate.processing.ollama_processor import OllamaProcessor

        return OllamaProcessor()

    from dictate.processing.regex_processor import RegexProcessor

    return RegexProcessor()
