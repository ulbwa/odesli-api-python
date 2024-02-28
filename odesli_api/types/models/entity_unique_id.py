from typing import List

from pydantic import BaseModel

from ..enums.api_provider import APIProvider
from ..enums.entity_type import EntityType
from ..enums.platform_name import PlatformName


class EntityUniqueId(BaseModel, use_enum_values=True):
    """
    Represents a unique identifier for an entity.

    :ivar id: The unique identifier.
    :ivar type: The type of the entity.
    :ivar title: Optional. The title of the entity.
    :ivar artist_name: Optional. The name of the artist associated with the entity.
    :ivar thumbnail_url: Optional. The URL of the thumbnail image for the entity.
    :ivar thumbnail_width: Optional. The width of the thumbnail image.
    :ivar thumbnail_height: Optional. The height of the thumbnail image.
    :ivar api_provider: The API provider for the entity.
    :ivar platforms: List of platforms associated with the entity.
    """

    id: str
    type: EntityType
    title: str | None
    artist_name: str | None
    thumbnail_url: str | None
    thumbnail_width: int | None
    thumbnail_height: int | None
    api_provider: APIProvider
    platforms: List[PlatformName]


__all__ = ("EntityUniqueId",)
