"""Protocol interface for ASR engines."""

from __future__ import annotations

from typing import Protocol

import numpy as np


class ASREngine(Protocol):
    """Interface that all ASR engines must implement."""

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcribe audio data to text.

        Args:
            audio: 1-D float32 numpy array of audio samples.
            sample_rate: Sample rate of the audio data.

        Returns:
            Transcribed text string.
        """
        ...
