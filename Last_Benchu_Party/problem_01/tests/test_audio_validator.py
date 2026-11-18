import struct
import wave
from pathlib import Path

from tools.check_audio import inspect_audio


def write_wav(path: Path, samples: list[int]) -> None:
    with wave.open(str(path), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(struct.pack("<" + "h" * len(samples), *samples))


def test_audio_validator_accepts_clean_mono_16khz(tmp_path):
    path = tmp_path / "clean.wav"
    write_wav(path, [0, 100, -100] * 2000)
    valid, detail = inspect_audio(path, 0.25, 30)
    assert valid
    assert "no full-scale samples" in detail


def test_audio_validator_flags_full_scale_clipping(tmp_path):
    path = tmp_path / "clipped.wav"
    write_wav(path, [0, 32767, -32768] * 2000)
    valid, detail = inspect_audio(path, 0.25, 30)
    assert not valid
    assert "possible clipping" in detail
