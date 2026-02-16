"""Audio recording using sounddevice into numpy arrays."""

from __future__ import annotations

import threading

import numpy as np
import sounddevice as sd


class AudioRecorder:
    """Records audio from the default microphone into a numpy array."""

    def __init__(self, sample_rate: int = 16000) -> None:
        self.sample_rate = sample_rate
        self._chunks: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None
        self._lock = threading.Lock()
        self._recording = False

    @property
    def is_recording(self) -> bool:
        return self._recording

    def start(self) -> None:
        """Start recording audio."""
        with self._lock:
            if self._recording:
                return
            self._chunks = []
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                callback=self._audio_callback,
            )
            self._stream.start()
            self._recording = True

    def stop(self) -> np.ndarray:
        """Stop recording and return the captured audio as a 1-D float32 array."""
        with self._lock:
            if not self._recording or self._stream is None:
                return np.array([], dtype=np.float32)
            self._stream.stop()
            self._stream.close()
            self._stream = None
            self._recording = False
            if not self._chunks:
                return np.array([], dtype=np.float32)
            return np.concatenate(self._chunks).flatten()

    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: object,
        status: sd.CallbackFlags,
    ) -> None:
        self._chunks.append(indata.copy())
