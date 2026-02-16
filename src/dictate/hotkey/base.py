"""Protocol interface for hotkey listeners."""

from __future__ import annotations

from typing import Callable, Protocol


class HotkeyListener(Protocol):
    """Interface that all hotkey listeners must implement."""

    def start(self, on_toggle: Callable[[], None]) -> None:
        """Start listening for the hotkey.

        Args:
            on_toggle: Callback invoked each time the hotkey is pressed.
        """
        ...

    def stop(self) -> None:
        """Stop listening for the hotkey."""
        ...
