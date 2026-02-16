"""Factory for creating hotkey listeners based on config."""

from __future__ import annotations

from dictate.config import Config
from dictate.hotkey.base import HotkeyListener


def create_hotkey_listener(config: Config) -> HotkeyListener:
    """Create and return the appropriate hotkey listener."""
    if config.hotkey_backend == "pyobjc_fn":
        from dictate.hotkey.pyobjc_fn_listener import PyObjCFnListener

        return PyObjCFnListener()

    from dictate.hotkey.pynput_listener import PynputHotkeyListener

    return PynputHotkeyListener(mode=config.hotkey_mode)
