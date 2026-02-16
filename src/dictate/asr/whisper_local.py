"""Local ASR engine using faster-whisper."""

from __future__ import annotations

import logging

import numpy as np
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class WhisperLocalEngine:
    """Transcribes audio locally using faster-whisper (CTranslate2)."""

    def __init__(self, model_size: str = "base", language: str = "en") -> None:
        self._model_size = model_size
        self._language = language
        self._model: WhisperModel | None = None
        logger.info("WhisperLocalEngine initialized (model will load on first use)")

    def _ensure_model_loaded(self) -> None:
        """Lazy-load the Whisper model on first transcription."""
        if self._model is None:
            logger.info("Loading Whisper model '%s' (this may take a few seconds)...", self._model_size)
            self._model = WhisperModel(self._model_size, device="cpu", compute_type="int8")
            logger.info("Whisper model loaded successfully.")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        if audio.size == 0:
            return ""

        self._ensure_model_loaded()
        assert self._model is not None  # for type checker

        segments, _info = self._model.transcribe(
            audio,
            language=self._language,
            beam_size=3,
            vad_filter=True,
            initial_prompt="Hello, welcome. I'd like to discuss the following topics, and please use proper punctuation.",
        )
        return " ".join(seg.text.strip() for seg in segments).strip()
