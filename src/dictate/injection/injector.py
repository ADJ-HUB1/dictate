"""Text injection via clipboard + Cmd+V paste."""

from __future__ import annotations

import logging
import time

import pyperclip
from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)

_keyboard = Controller()


def inject_text(text: str) -> None:
    """Copy text to clipboard and simulate Cmd+V to paste into active app."""
    if not text:
        logger.warning("inject_text called with empty text")
        return

    logger.info("Attempting to inject text: %r", text)

    # Save current clipboard content to restore after paste
    try:
        previous = pyperclip.paste()
        logger.debug("Saved previous clipboard content")
    except Exception as e:
        logger.warning("Failed to read clipboard: %s", e)
        previous = None

    try:
        pyperclip.copy(text)
        logger.debug("Text copied to clipboard")
    except Exception as e:
        logger.error("Failed to copy text to clipboard: %s", e)
        return

    time.sleep(0.05)  # Brief pause to ensure clipboard is set

    try:
        logger.debug("Simulating Cmd+V keypress")
        _keyboard.press(Key.cmd)
        _keyboard.press("v")
        _keyboard.release("v")
        _keyboard.release(Key.cmd)
        logger.info("Cmd+V keypress sent successfully")
    except Exception as e:
        logger.error("Failed to simulate Cmd+V keypress: %s", e)
        logger.error("This usually means accessibility permissions are not granted")
        return

    # Restore previous clipboard content after a short delay
    time.sleep(0.1)
    if previous is not None:
        try:
            pyperclip.copy(previous)
            logger.debug("Restored previous clipboard content")
        except Exception as e:
            logger.debug("Failed to restore clipboard: %s", e)
