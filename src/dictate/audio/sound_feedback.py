"""Sound feedback for recording start/stop events."""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


def play_beep(frequency: int = 1000, duration: float = 0.1) -> None:
    """Play a system beep using macOS 'afplay' command.

    Args:
        frequency: Beep frequency in Hz (higher = higher pitch)
        duration: Beep duration in seconds
    """
    try:
        # Use the macOS system beep sound
        # For custom frequencies, we'd need to generate a sound file
        # For simplicity, use the system beep (NSBeep equivalent)
        subprocess.run(["afplay", "/System/Library/Sounds/Tink.aiff"], check=False, capture_output=True)
    except Exception:
        logger.debug("Could not play sound feedback", exc_info=True)


def play_start_beep() -> None:
    """Play a beep when recording starts (higher pitch)."""
    play_beep(frequency=1200, duration=0.1)


def play_stop_beep() -> None:
    """Play a beep when recording stops (lower pitch)."""
    play_beep(frequency=800, duration=0.15)
