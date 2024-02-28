from enum import StrEnum


class EntityType(StrEnum):
    """
    Enumeration representing types of entities.
    """

    song = "song"
    album = "album"


__all__ = ("EntityType",)
