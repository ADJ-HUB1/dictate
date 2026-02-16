"""macOS notification system for previewing transcribed text."""

from __future__ import annotations

import logging
import subprocess
import threading

logger = logging.getLogger(__name__)


def _escape_applescript(text: str) -> str:
    """Escape a string for use inside AppleScript double-quoted strings.

    AppleScript uses doubled double-quotes inside string literals, and
    backslashes must also be doubled.
    """
    return text.replace("\\", "\\\\").replace('"', '\\"')


def show_notification(title: str, message: str, subtitle: str = "") -> None:
    """Show a macOS notification using osascript (non-blocking).

    Args:
        title: Notification title
        message: Notification body text
        subtitle: Optional subtitle text
    """
    try:
        title = _escape_applescript(title)
        message = _escape_applescript(message)
        subtitle = _escape_applescript(subtitle)

        script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'

        # Run in a thread so we don't block text injection
        threading.Thread(
            target=subprocess.run,
            args=(["osascript", "-e", script],),
            kwargs={"check": False, "capture_output": True},
            daemon=True,
        ).start()
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
