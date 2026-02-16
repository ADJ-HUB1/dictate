"""Configuration loading and validation from .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    asr_engine: str = "local"
    whisper_model: str = "base"
    whisper_language: str = "en"
    openai_api_key: str = ""
    text_processor: str = "regex"
    hotkey_backend: str = "pynput"
    hotkey_mode: str = "toggle"
    sample_rate: int = 16000
    enable_sound_feedback: bool = False
    show_preview_notification: bool = False

    def __post_init__(self) -> None:
        valid_asr = ("local", "openai_api")
        if self.asr_engine not in valid_asr:
            raise ValueError(f"ASR_ENGINE must be one of {valid_asr}, got '{self.asr_engine}'")

        valid_models = ("tiny", "base", "small", "medium", "large-v3")
        if self.whisper_model not in valid_models:
            raise ValueError(f"WHISPER_MODEL must be one of {valid_models}, got '{self.whisper_model}'")

        if self.asr_engine == "openai_api" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when ASR_ENGINE=openai_api")

        valid_processors = ("regex", "ollama")
        if self.text_processor not in valid_processors:
            raise ValueError(f"TEXT_PROCESSOR must be one of {valid_processors}, got '{self.text_processor}'")

        valid_hotkey = ("pynput", "pyobjc_fn")
        if self.hotkey_backend not in valid_hotkey:
            raise ValueError(f"HOTKEY_BACKEND must be one of {valid_hotkey}, got '{self.hotkey_backend}'")

        valid_modes = ("toggle", "hold")
        if self.hotkey_mode not in valid_modes:
            raise ValueError(f"HOTKEY_MODE must be one of {valid_modes}, got '{self.hotkey_mode}'")


def load_config(env_path: Path | None = None) -> Config:
    """Load configuration from .env file and environment variables."""
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

    return Config(
        asr_engine=os.getenv("ASR_ENGINE", "local").lower(),
        whisper_model=os.getenv("WHISPER_MODEL", "base").lower(),
        whisper_language=os.getenv("WHISPER_LANGUAGE", "en").lower(),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        text_processor=os.getenv("TEXT_PROCESSOR", "regex").lower(),
        hotkey_backend=os.getenv("HOTKEY_BACKEND", "pynput").lower(),
        hotkey_mode=os.getenv("HOTKEY_MODE", "toggle").lower(),
        sample_rate=int(os.getenv("SAMPLE_RATE", "16000")),
        enable_sound_feedback=os.getenv("ENABLE_SOUND_FEEDBACK", "false").lower() == "true",
        show_preview_notification=os.getenv("SHOW_PREVIEW_NOTIFICATION", "false").lower() == "true",
    )
