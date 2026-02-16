"""Tests for config module."""

from __future__ import annotations

import pytest

from dictate.config import Config


class TestConfig:
    def test_default_values(self) -> None:
        config = Config()
        assert config.asr_engine == "local"
        assert config.whisper_model == "base"
        assert config.whisper_language == "en"
        assert config.text_processor == "regex"
        assert config.hotkey_backend == "pynput"
        assert config.sample_rate == 16000

    def test_invalid_asr_engine(self) -> None:
        with pytest.raises(ValueError, match="ASR_ENGINE"):
            Config(asr_engine="invalid")

    def test_invalid_whisper_model(self) -> None:
        with pytest.raises(ValueError, match="WHISPER_MODEL"):
            Config(whisper_model="huge")

    def test_api_engine_requires_key(self) -> None:
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            Config(asr_engine="openai_api", openai_api_key="")

    def test_api_engine_with_key(self) -> None:
        config = Config(asr_engine="openai_api", openai_api_key="sk-test")
        assert config.asr_engine == "openai_api"

    def test_invalid_text_processor(self) -> None:
        with pytest.raises(ValueError, match="TEXT_PROCESSOR"):
            Config(text_processor="gpt")

    def test_invalid_hotkey_backend(self) -> None:
        with pytest.raises(ValueError, match="HOTKEY_BACKEND"):
            Config(hotkey_backend="keyboard")

    def test_frozen(self) -> None:
        config = Config()
        with pytest.raises(AttributeError):
            config.asr_engine = "openai_api"  # type: ignore[misc]
