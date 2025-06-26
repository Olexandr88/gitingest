"""Compatibility layer for typing."""

from typing import TypeVar

try:  # Py ≥ 3.10
    from typing import ParamSpec, TypeAlias
except ImportError:  # Py 3.8 / 3.9
    from typing_extensions import ParamSpec, TypeAlias

try:  # Py ≥ 3.9
    from typing import Annotated
except ImportError:  # Py 3.8
    from typing_extensions import Annotated


T = TypeVar("T")
P = ParamSpec("P")


__all__ = ["Annotated", "P", "ParamSpec", "T", "TypeAlias"]
