"""Validate optional 16 kHz mono PCM16 WAV contributions and clipping."""
from __future__ import annotations

import argparse
import sys
import wave
from array import array
from pathlib import Path


def inspect_audio(path: Path, min_seconds: float, max_seconds: float) -> tuple[bool, str]:
    """Return a format/quality status and a concise explanation for one WAV."""
    try:
        with wave.open(str(path), "rb") as handle:
            rate = handle.getframerate()
            channels = handle.getnchannels()
            width = handle.getsampwidth()
            frames = handle.getnframes()
            duration = frames / rate if rate else 0.0
            if handle.getcomptype() != "NONE":
                return False, "compressed WAV is not supported"
            if rate != 16000 or channels != 1 or width != 2:
                return False, f"expected 16 kHz mono PCM16; got {rate} Hz, {channels} ch, {width * 8}-bit"
            if frames == 0 or not min_seconds <= duration <= max_seconds:
                return False, f"duration {duration:.2f}s outside {min_seconds:.2f}-{max_seconds:.2f}s"
            samples = array("h")
            samples.frombytes(handle.readframes(frames))
            if sys.byteorder != "little":
                samples.byteswap()
            clipped = sum(sample in (-32768, 32767) for sample in samples)
            if clipped:
                return False, f"{duration:.2f}s; {clipped} full-scale samples (possible clipping)"
            peak = max((abs(sample) for sample in samples), default=0)
            return True, f"{duration:.2f}s; peak {peak}/32767; no full-scale samples"
    except (OSError, wave.Error, EOFError) as exc:
        return False, f"invalid WAV: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default="data/audio")
    parser.add_argument("--min-seconds", type=float, default=0.25)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()
    directory = Path(args.directory)
    files = sorted(directory.glob("*.wav"))
    if not files:
        print(f"No WAV files found in {directory}; audio is optional.")
        return 0
    failed = 0
    for path in files:
        valid, detail = inspect_audio(path, args.min_seconds, args.max_seconds)
        print(f"{path}: {'OK' if valid else 'INVALID'} — {detail}")
        failed += not valid
    print(f"Audio files: {len(files)}; invalid: {failed}")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
