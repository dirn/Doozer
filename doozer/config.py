"""A custom configuration."""

from typing import Mapping

__all__ = ('Config',)


class Config(dict):
    """Custom mapping used to extend and override an app's settings."""

    def from_mapping(self, mapping: Mapping) -> None:
        """Convert a mapping into settings.

        Uppercase keys of the specified mapping will be used to extend
        and update the existing settings.

        Args:
            mapping: A mapping encapsulating settings.
        """
        for key, value in mapping.items():
            self[key] = value

    def from_object(self, obj: object) -> None:
        """Convert an object into settings.

        Uppercase attributes of the specified object will be used to
        extend and update the existing settings.

        Args:
            obj: An object encapsulating settings. This will typically
              be a module or class.
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
