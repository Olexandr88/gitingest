"""Utility functions for working with files and directories."""

from __future__ import annotations

import locale
import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "C")

_CHUNK_SIZE = 1024  # bytes


def get_preferred_encodings() -> list[str]:
    """Get list of encodings to try, prioritized for the current platform.

    Returns
    -------
    list[str]
        List of encoding names to try in priority order, starting with the
        platform's default encoding followed by common fallback encodings.

    """
    encodings = [locale.getpreferredencoding(), "utf-8", "utf-16", "utf-16le", "utf-8-sig", "latin"]
    if platform.system() == "Windows":
        encodings += ["cp1252", "iso-8859-1"]
    return encodings


def is_text_file(path: Path) -> bool:
    """Heuristically decide whether *path* is a text file.

    Tries to decode a small chunk with multiple encodings, and checking for common binary markers.

    Parameters
    ----------
    path : Path
        The path to the file to check.

    Returns
    -------
    bool
        `True` if the file is likely textual; `False` if it appears to be binary.

    """
    # Attempt to read a portion of the file in binary mode
    chunk = _read_chunk(path)

    if chunk is None:  # File is not readable
        return False

    if chunk == b"":  # empty file → text
        # TODO: should we include empty files?
        return True

    if b"\x00" in chunk or b"\xff" in chunk:  # obvious binary markers
        return False

    # any encoding that works → text file
    return any(_decodes(chunk, encoding=enc) for enc in get_preferred_encodings())


def _read_chunk(path: Path, size: int = _CHUNK_SIZE) -> bytes | None:
    """Return the first *size* bytes of *path*, or None on any `OSError`.

    Parameters
    ----------
    path : Path
        The path to the file to read.
    size : int
        The number of bytes to read (default: 1024).

    Returns
    -------
    bytes | None
        The first *size* bytes of *path*, or None on any `OSError` (file is not readable).

    """
    try:
        with path.open("rb") as fp:
            return fp.read(size)
    except OSError:  # File is not readable
        return None


def _decodes(chunk: bytes, encoding: str) -> bool:
    """Return *True* if *chunk* decodes cleanly with *encoding*.

    Parameters
    ----------
    chunk : bytes
        The chunk of bytes to decode.
    encoding : str
        The encoding to use to decode the chunk.

    Returns
    -------
    bool
        True if the chunk decodes cleanly with the encoding, False otherwise.

    """
    try:
        chunk.decode(encoding)
    except (UnicodeDecodeError, UnicodeError):
        return False
    return True
