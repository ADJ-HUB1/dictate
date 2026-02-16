"""macOS notification system for previewing transcribed text."""

from __future__ import annotations

import logging
import subprocess

logger = logging.getLogger(__name__)


def show_notification(title: str, message: str, subtitle: str = "") -> None:
    """Show a macOS notification using osascript.

    Args:
        title: Notification title
        message: Notification body text
        subtitle: Optional subtitle text
    """
    try:
        # Escape quotes in the message for AppleScript
        message = message.replace('"', '\\"').replace("'", "\\'")
        subtitle = subtitle.replace('"', '\\"').replace("'", "\\'")

        script = f'''
        display notification "{message}" with title "{title}" subtitle "{subtitle}"
        '''

        subprocess.run(
            ["osascript", "-e", script],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        logger.debug("Could not show notification", exc_info=True)


def show_transcription_preview(text: str) -> None:
    """Show transcribed text in a notification.

    Args:
        text: The transcribed text to preview
    """
    # Truncate long messages for the notification
    preview = text if len(text) <= 200 else text[:197] + "..."
    show_notification(
        title="Dictate",
        message=preview,
        subtitle="Text ready to paste",
    )
