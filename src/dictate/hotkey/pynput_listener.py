"""Hotkey listener using pynput (Option+Space)."""

from __future__ import annotations

import logging
from typing import Callable

from pynput import keyboard

logger = logging.getLogger(__name__)


class PynputHotkeyListener:
    """Listens for Option+Space (Alt+Space) to toggle or hold-to-talk recording."""

    def __init__(self, mode: str = "toggle") -> None:
        self._mode = mode
        self._listener: keyboard.Listener | keyboard.GlobalHotKeys | None = None
        self._on_start: Callable[[], None] | None = None
        self._on_stop: Callable[[], None] | None = None

        # For hold-to-talk mode
        self._alt_pressed = False
        self._space_pressed = False
        self._recording = False

    def start(self, on_toggle: Callable[[], None]) -> None:
        """Start listener in toggle mode (legacy interface for backward compatibility)."""
        if self._mode == "toggle":
            self._on_start = on_toggle
            self._listener = keyboard.GlobalHotKeys({
                "<alt>+<space>": self._handle_toggle,
            })
            self._listener.daemon = True
            self._listener.start()
            logger.info("Hotkey listener started (Option+Space, toggle mode)")
        else:
            # Hold mode
            self._on_start = on_toggle
            self._on_stop = on_toggle  # In toggle mode, same callback
            self._listener = keyboard.Listener(
                on_press=self._on_press_hold,
                on_release=self._on_release_hold,
            )
            self._listener.daemon = True
            self._listener.start()
            logger.info("Hotkey listener started (Option+Space, hold-to-talk mode)")

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def _handle_toggle(self) -> None:
        """Handle hotkey press in toggle mode."""
        if self._on_start:
            self._on_start()

    def _on_press_hold(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        """Handle key press in hold-to-talk mode."""
        # Track Alt key state
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            self._alt_pressed = True

        # Track Space key state
        elif key == keyboard.Key.space:
            self._space_pressed = True

            # If both Alt and Space are pressed and not already recording, start recording
            if self._alt_pressed and not self._recording:
                self._recording = True
                if self._on_start:
                    logger.info("Hold-to-talk: Recording started")
                    self._on_start()

    def _on_release_hold(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        """Handle key release in hold-to-talk mode."""
        # Track Alt key release
        if key in (keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r):
            self._alt_pressed = False

        # Track Space key release and stop recording
        elif key == keyboard.Key.space:
            self._space_pressed = False

            # If we were recording, stop now
            if self._recording:
                self._recording = False
                if self._on_stop:
                    logger.info("Hold-to-talk: Recording stopped")
                    self._on_stop()
