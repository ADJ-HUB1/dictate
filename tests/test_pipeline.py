"""Tests for the pipeline orchestrator."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from dictate.pipeline import Pipeline, PipelineState


@pytest.fixture
def mock_components() -> tuple[MagicMock, MagicMock, MagicMock]:
    recorder = MagicMock()
    recorder.sample_rate = 16000
    recorder.is_recording = False

    asr_engine = MagicMock()
    asr_engine.transcribe.return_value = "um hello world"

    text_processor = MagicMock()
    text_processor.process.return_value = "Hello world."

    return recorder, asr_engine, text_processor


class TestPipeline:
    def test_initial_state_is_idle(self, mock_components: tuple) -> None:
        recorder, asr, processor = mock_components
        pipeline = Pipeline(recorder, asr, processor)
        assert pipeline.state == PipelineState.IDLE

    def test_toggle_starts_recording(self, mock_components: tuple) -> None:
        recorder, asr, processor = mock_components
        states: list[PipelineState] = []
        pipeline = Pipeline(recorder, asr, processor, on_state_change=states.append)

        pipeline.toggle()

        assert pipeline.state == PipelineState.RECORDING
        recorder.start.assert_called_once()
        assert PipelineState.RECORDING in states

    @patch("dictate.pipeline.inject_text")
    def test_toggle_twice_processes_audio(
        self, mock_inject: MagicMock, mock_components: tuple
    ) -> None:
        recorder, asr, processor = mock_components
        audio_data = np.ones(16000, dtype=np.float32)
        recorder.stop.return_value = audio_data

        states: list[PipelineState] = []
        pipeline = Pipeline(recorder, asr, processor, on_state_change=states.append)

        # First toggle: start recording
        pipeline.toggle()
        assert pipeline.state == PipelineState.RECORDING

        # Second toggle: stop and process
        pipeline.toggle()

        # Wait for background thread to complete
        time.sleep(0.5)

        recorder.stop.assert_called_once()
        asr.transcribe.assert_called_once_with(audio_data, 16000)
        processor.process.assert_called_once_with("um hello world")
        mock_inject.assert_called_once_with("Hello world.")
        assert pipeline.state == PipelineState.IDLE

    @patch("dictate.pipeline.inject_text")
    def test_empty_audio_skips_injection(
        self, mock_inject: MagicMock, mock_components: tuple
    ) -> None:
        recorder, asr, processor = mock_components
        recorder.stop.return_value = np.array([], dtype=np.float32)

        pipeline = Pipeline(recorder, asr, processor)
        pipeline.toggle()  # start
        pipeline.toggle()  # stop

        time.sleep(0.5)

        asr.transcribe.assert_not_called()
        mock_inject.assert_not_called()
        assert pipeline.state == PipelineState.IDLE
