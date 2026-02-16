"""Tests for audio recorder (mocked — no real audio device needed)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from dictate.audio.recorder import AudioRecorder


class TestAudioRecorder:
    def test_initial_state(self) -> None:
        recorder = AudioRecorder()
        assert not recorder.is_recording

    def test_stop_without_start_returns_empty(self) -> None:
        recorder = AudioRecorder()
        result = recorder.stop()
        assert isinstance(result, np.ndarray)
        assert result.size == 0

    @patch("dictate.audio.recorder.sd.InputStream")
    def test_start_begins_recording(self, mock_stream_cls: MagicMock) -> None:
        mock_stream = MagicMock()
        mock_stream_cls.return_value = mock_stream

        recorder = AudioRecorder(sample_rate=16000)
        recorder.start()

        assert recorder.is_recording
        mock_stream.start.assert_called_once()

    @patch("dictate.audio.recorder.sd.InputStream")
    def test_start_is_idempotent(self, mock_stream_cls: MagicMock) -> None:
        mock_stream = MagicMock()
        mock_stream_cls.return_value = mock_stream

        recorder = AudioRecorder()
        recorder.start()
        recorder.start()  # Should not create a second stream

        assert mock_stream_cls.call_count == 1

    @patch("dictate.audio.recorder.sd.InputStream")
    def test_stop_returns_concatenated_audio(self, mock_stream_cls: MagicMock) -> None:
        mock_stream = MagicMock()
        mock_stream_cls.return_value = mock_stream

        recorder = AudioRecorder(sample_rate=16000)
        recorder.start()

        # Simulate audio chunks arriving via callback
        chunk1 = np.ones((1024, 1), dtype=np.float32) * 0.5
        chunk2 = np.ones((1024, 1), dtype=np.float32) * 0.3
        recorder._audio_callback(chunk1, 1024, None, None)
        recorder._audio_callback(chunk2, 1024, None, None)

        result = recorder.stop()

        assert not recorder.is_recording
        assert result.shape == (2048,)
        mock_stream.stop.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_sample_rate(self) -> None:
        recorder = AudioRecorder(sample_rate=44100)
        assert recorder.sample_rate == 44100
