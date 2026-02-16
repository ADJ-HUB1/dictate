"""Factory for creating ASR engines based on config."""

from __future__ import annotations

from dictate.asr.base import ASREngine
from dictate.config import Config


def create_asr_engine(config: Config) -> ASREngine:
    """Create and return the appropriate ASR engine."""
    if config.asr_engine == "openai_api":
        from dictate.asr.whisper_api import WhisperAPIEngine

        return WhisperAPIEngine(api_key=config.openai_api_key)

    from dictate.asr.whisper_local import WhisperLocalEngine

    return WhisperLocalEngine(model_size=config.whisper_model, language=config.whisper_language)
