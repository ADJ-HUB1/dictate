"""Experimental Fn key listener using PyObjC.

WARNING: macOS intercepts the Fn key for the emoji picker on modern macOS.
This listener is experimental and may not work reliably on all systems.
"""

from __future__ import annotations

import logging
from typing import Callable

logger = logging.getLogger(__name__)


class PyObjCFnListener:
    """Experimental Fn key listener via NSEvent global monitor.

    Requires PyObjC to be installed. The Fn key is intercepted by macOS
    for the emoji picker, so this may not fire on all systems.
    """

    def __init__(self) -> None:
        self._monitor = None
        self._on_toggle: Callable[[], None] | None = None

    def start(self, on_toggle: Callable[[], None]) -> None:
        self._on_toggle = on_toggle
        try:
            from AppKit import NSEvent, NSFlagsChangedMask
            from Cocoa import NSEventModifierFlagFunction

            def handler(event: object) -> None:
                flags = event.modifierFlags()
                # Fn key toggle: fires when Fn modifier flag changes
                if flags & NSEventModifierFlagFunction:
                    if self._on_toggle:
                        self._on_toggle()

            self._monitor = NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
                NSFlagsChangedMask, handler
            )
            logger.info("Fn key listener started (experimental)")
        except ImportError:
            logger.error(
                "PyObjC not installed. Install with: pip install pyobjc-framework-Cocoa"
            )
            raise

    def stop(self) -> None:
        if self._monitor is not None:
            try:
                from AppKit import NSEvent

                NSEvent.removeMonitor_(self._monitor)
            except Exception:
                pass
            self._monitor = None
