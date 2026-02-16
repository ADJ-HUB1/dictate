"""Shared test fixtures."""

from __future__ import annotations

import pytest

from dictate.config import Config


@pytest.fixture
def default_config() -> Config:
    return Config()


@pytest.fixture
def api_config() -> Config:
    return Config(asr_engine="openai_api", openai_api_key="test-key-123")
