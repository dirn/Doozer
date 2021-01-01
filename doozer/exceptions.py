"""Custom exceptions used by Doozer."""
from __future__ import annotations

from .types import Message

__all__ = ("Abort",)


class Abort(Exception):
    """An exception that signals to Doozer to stop processing a message.

    When this exception is caught by Doozer it will immediately stop
    processing the message. None of the remaining callbacks will be
    called.

    If the exception is caught while processing a result, that result
    will no longer be processed. Any other results generated by the same
    message will still be processed.

    Args:
        reason: The reason the message is being aborted. It should be in
            the form of "noun.verb" (e.g., "provider.ignored").
        message: The message that is being aborted. Usually this will be
            the incoming message, but it can also be the result.
    """

    def __init__(self, reason: str, message: Message) -> None:
        """Initialize the class."""
        super().__init__(reason)
        self.message = message
