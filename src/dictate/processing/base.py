"""Protocol interface for text processors."""

from __future__ import annotations

from typing import Protocol


class TextProcessor(Protocol):
    """Interface that all text processors must implement."""

    def process(self, text: str) -> str:
        """Clean up and format transcribed text.

        Args:
            text: Raw transcription text.

        Returns:
            Cleaned and formatted text.
        """
        ...
