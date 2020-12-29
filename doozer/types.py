"""Custom types for static type analysis."""

from typing import Any, Awaitable, Callable

from typing_extensions import Protocol

__all__ = ("Callback", "Consumer")


Callback = Callable[..., Awaitable]

Message = Any


class Consumer(Protocol):
    """An implementation of the Consumer Interface."""

    async def read(self) -> Any:
        """The read method of the Consumer Interface."""  # NOQA: D401
