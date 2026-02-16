"""macOS menu bar app using rumps."""

from __future__ import annotations

import logging
import os

import rumps

from dictate.asr.factory import create_asr_engine
from dictate.audio.recorder import AudioRecorder
from dictate.config import Config
from dictate.hotkey.factory import create_hotkey_listener
from dictate.pipeline import Pipeline, PipelineState
from dictate.processing.factory import create_text_processor

logger = logging.getLogger(__name__)

# Icon paths relative to this file
_RESOURCES = os.path.join(os.path.dirname(__file__), "resources")
_ICONS = {
    PipelineState.IDLE: os.path.join(_RESOURCES, "icon_idle.png"),
    PipelineState.RECORDING: os.path.join(_RESOURCES, "icon_recording.png"),
    PipelineState.PROCESSING: os.path.join(_RESOURCES, "icon_processing.png"),
}

_STATUS_TEXT = {
    PipelineState.IDLE: "Dictate",
    PipelineState.RECORDING: "Recording...",
    PipelineState.PROCESSING: "Processing...",
}


class DictateApp(rumps.App):
    """Menu bar application for Dictate."""

    def __init__(self, config: Config) -> None:
        super().__init__(
            "Dictate",
            icon=_ICONS.get(PipelineState.IDLE),
            template=True,
        )

        self._config = config

        # Build components
        recorder = AudioRecorder(sample_rate=config.sample_rate)
        asr_engine = create_asr_engine(config)
        text_processor = create_text_processor(config)

        self._pipeline = Pipeline(
            recorder=recorder,
            asr_engine=asr_engine,
            text_processor=text_processor,
            on_state_change=self._on_state_change,
            enable_sound_feedback=config.enable_sound_feedback,
            show_preview_notification=config.show_preview_notification,
        )

        self._hotkey = create_hotkey_listener(config)

        # Menu items
        self.menu = [
            rumps.MenuItem("Status: Idle", callback=None),
            None,  # separator
            rumps.MenuItem("ASR: " + config.asr_engine),
            rumps.MenuItem("Model: " + config.whisper_model),
            rumps.MenuItem("Hotkey: Option+Space"),
            None,  # separator
        ]

    def _on_state_change(self, state: PipelineState) -> None:
        """Update menu bar icon and status on state changes."""
        icon_path = _ICONS.get(state)
        if icon_path and os.path.exists(icon_path):
            self.icon = icon_path
        self.title = _STATUS_TEXT.get(state, "Dictate")

        # Update status menu item
        status_item = self.menu.get("Status: Idle") or self.menu.get("Status: Recording...") or self.menu.get("Status: Processing...")
        if status_item:
            status_item.title = f"Status: {state.name.capitalize()}"

    @rumps.clicked("Quit Dictate")
    def on_quit(self, _: rumps.MenuItem) -> None:
        self._hotkey.stop()
        rumps.quit_application()

    def run(self, **kwargs: object) -> None:
        """Start the hotkey listener and run the app."""
        self._hotkey.start(self._pipeline.toggle)
        logger.info("Dictate is running. Press Option+Space to toggle recording.")
        super().run(**kwargs)
