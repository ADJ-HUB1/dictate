"""OpenAI Whisper API fallback engine."""

from __future__ import annotations

import io
import logging

import numpy as np
from scipy.io import wavfile

logger = logging.getLogger(__name__)


class WhisperAPIEngine:
    """Transcribes audio via the OpenAI Whisper API."""

    def __init__(self, api_key: str) -> None:
        from openai import OpenAI

        self._client = OpenAI(api_key=api_key)

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        if audio.size == 0:
            return ""
        # Convert float32 [-1, 1] to int16 WAV in memory
        audio_int16 = (audio * 32767).astype(np.int16)
        buf = io.BytesIO()
        wavfile.write(buf, sample_rate, audio_int16)
        buf.seek(0)
        buf.name = "audio.wav"

        transcript = self._client.audio.transcriptions.create(
            model="whisper-1",
            file=buf,
        )
        return transcript.text.strip()
