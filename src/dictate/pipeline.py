"""Pipeline orchestrator: audio → ASR → cleanup → inject."""

from __future__ import annotations

import logging
import threading
from enum import Enum, auto
from typing import Callable

import numpy as np

from dictate.asr.base import ASREngine
from dictate.audio.recorder import AudioRecorder
from dictate.audio.sound_feedback import play_start_beep, play_stop_beep
from dictate.injection.injector import inject_text
from dictate.notification.notifier import show_transcription_preview
from dictate.processing.base import TextProcessor

logger = logging.getLogger(__name__)


class PipelineState(Enum):
    IDLE = auto()
    RECORDING = auto()
    PROCESSING = auto()


class Pipeline:
    """Connects recorder → ASR → text processor → text injection."""

    def __init__(
        self,
        recorder: AudioRecorder,
        asr_engine: ASREngine,
        text_processor: TextProcessor,
        on_state_change: Callable[[PipelineState], None] | None = None,
        enable_sound_feedback: bool = False,
        show_preview_notification: bool = False,
    ) -> None:
        self._recorder = recorder
        self._asr = asr_engine
        self._processor = text_processor
        self._on_state_change = on_state_change
        self._enable_sound_feedback = enable_sound_feedback
        self._show_preview_notification = show_preview_notification
        self._state = PipelineState.IDLE
        self._lock = threading.Lock()

    @property
    def state(self) -> PipelineState:
        return self._state

    def _set_state(self, state: PipelineState) -> None:
        self._state = state
        if self._on_state_change:
            self._on_state_change(state)

    def toggle(self) -> None:
        """Toggle recording on/off. Called from hotkey callback."""
        with self._lock:
            if self._state == PipelineState.IDLE:
                self._start_recording()
            elif self._state == PipelineState.RECORDING:
                self._stop_and_process()

    def _start_recording(self) -> None:
        logger.info("Recording started")
        self._set_state(PipelineState.RECORDING)
        if self._enable_sound_feedback:
            play_start_beep()
        self._recorder.start()

    def _stop_and_process(self) -> None:
        logger.info("Recording stopped, processing...")
        audio = self._recorder.stop()
        if self._enable_sound_feedback:
            play_stop_beep()
        self._set_state(PipelineState.PROCESSING)

        # Run transcription + injection in a background thread
        thread = threading.Thread(target=self._process_audio, args=(audio,), daemon=True)
        thread.start()

    def _process_audio(self, audio: np.ndarray) -> None:
        try:
            if audio.size == 0:
                logger.warning("No audio recorded")
                self._set_state(PipelineState.IDLE)
                return

            duration = len(audio) / self._recorder.sample_rate
            logger.info("Transcribing %.1fs of audio...", duration)

            raw_text = self._asr.transcribe(audio, self._recorder.sample_rate)
            logger.info("Raw transcription: %s", raw_text)

            cleaned_text = self._processor.process(raw_text)
            logger.info("Cleaned text: %s", cleaned_text)

            if cleaned_text:
                if self._show_preview_notification:
                    show_transcription_preview(cleaned_text)

                inject_text(cleaned_text)
                logger.info("Text injected successfully")
            else:
                logger.warning("No text to inject after processing")
        except Exception:
            logger.exception("Error processing audio")
        finally:
            self._set_state(PipelineState.IDLE)
