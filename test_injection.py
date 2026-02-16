#!/usr/bin/env python3
"""Test script to diagnose text injection issues."""

import logging
import time
from src.dictate.injection.injector import inject_text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)

logger.info("Testing text injection...")
logger.info("Switch to a text editor now. Injection will happen in 3 seconds...")
time.sleep(3)

test_text = "This is a test of the text injection system."
logger.info(f"Injecting: {test_text}")
inject_text(test_text)
logger.info("Injection complete. Did the text appear?")
