"""Entry point for Dictate: python -m dictate."""

from __future__ import annotations

import logging
import sys


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    # Check platform
    if sys.platform != "darwin":
        logger.error("Dictate only runs on macOS.")
        sys.exit(1)

    from dictate.app import DictateApp
    from dictate.config import load_config

    try:
        config = load_config()
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        sys.exit(1)

    logger.info("Starting Dictate (ASR=%s, model=%s)", config.asr_engine, config.whisper_model)

    app = DictateApp(config)
    app.run()


if __name__ == "__main__":
    main()
