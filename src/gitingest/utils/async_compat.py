"""Compatibility utilities wrapping asyncio features that are missing on older Python versions (e.g. 3.8)."""

from __future__ import annotations

import asyncio
import functools
import sys
from typing import Callable, TypeVar

_T = TypeVar("_T")

if sys.version_info >= (3, 9):
    from asyncio import to_thread
else:

    async def to_thread(func: Callable[..., _T], /, *args: object, **kwargs: object) -> _T:
        """Back-port :pyfunc:`asyncio.to_thread` for Python < 3.9.

        Run *func* in the default thread-pool executor and return the result.
        """
        loop = asyncio.get_running_loop()

        if loop.is_running():
            return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

        # Shouldn't happen under normal circumstances; fall back defensively.
        return func(*args, **kwargs)

    # Patch stdlib so that *existing* imports of ``asyncio`` see the shim.
    if not hasattr(asyncio, "to_thread"):
        asyncio.to_thread = to_thread  # type: ignore[attr-defined, assignment]

__all__ = ["to_thread"]
