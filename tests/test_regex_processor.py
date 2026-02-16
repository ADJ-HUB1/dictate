"""Tests for regex text processor."""

from __future__ import annotations

import pytest

from dictate.processing.regex_processor import RegexProcessor


@pytest.fixture
def processor() -> RegexProcessor:
    return RegexProcessor()


class TestRegexProcessor:
    def test_empty_string(self, processor: RegexProcessor) -> None:
        assert processor.process("") == ""

    def test_whitespace_only(self, processor: RegexProcessor) -> None:
        assert processor.process("   ") == ""

    def test_removes_um(self, processor: RegexProcessor) -> None:
        result = processor.process("um I was going to the store")
        assert "um" not in result.lower()
        assert "going" in result.lower()

    def test_removes_uh(self, processor: RegexProcessor) -> None:
        result = processor.process("I uh wanted to say something")
        assert "uh" not in result.lower()

    def test_removes_you_know(self, processor: RegexProcessor) -> None:
        result = processor.process("I was you know going there")
        assert "you know" not in result.lower()

    def test_removes_multiple_fillers(self, processor: RegexProcessor) -> None:
        result = processor.process("um so I was like you know going")
        assert result  # Should produce non-empty cleaned text
        assert "um" not in result.lower()
        # "so" and "like" are fillers too
        assert "going" in result.lower()

    def test_capitalizes_first_letter(self, processor: RegexProcessor) -> None:
        result = processor.process("hello world")
        assert result[0] == "H"

    def test_adds_period(self, processor: RegexProcessor) -> None:
        result = processor.process("hello world")
        assert result.endswith(".")

    def test_preserves_existing_punctuation(self, processor: RegexProcessor) -> None:
        result = processor.process("is this a question?")
        assert result.endswith("?")
        assert not result.endswith("?.")

    def test_preserves_exclamation(self, processor: RegexProcessor) -> None:
        result = processor.process("that is amazing!")
        assert result.endswith("!")

    def test_clean_sentence_passes_through(self, processor: RegexProcessor) -> None:
        result = processor.process("The weather is nice today.")
        assert "weather" in result
        assert "nice" in result
        assert "today" in result
