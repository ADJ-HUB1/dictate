"""Sound feedback for recording start/stop events."""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


def _play_sound(sound_file: str, rate: float = 1.0) -> None:
    """Play a macOS system sound non-blocking.

    Args:
        sound_file: Path to the .aiff sound file
        rate: Playback rate (higher = higher pitch). 1.0 = normal, 2.0 = double speed/pitch
    """
    try:
        # Popen is non-blocking — sound plays in background without stalling the pipeline
        subprocess.Popen(
            ["afplay", "-r", str(rate), sound_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        logger.debug("Could not play sound feedback", exc_info=True)


def play_start_beep() -> None:
    """Play a higher-pitched beep when recording starts."""
    _play_sound("/System/Library/Sounds/Tink.aiff", rate=1.5)


def play_stop_beep() -> None:
    """Play a lower-pitched beep when recording stops."""
    _play_sound("/System/Library/Sounds/Pop.aiff", rate=1.0)
