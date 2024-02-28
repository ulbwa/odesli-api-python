from typing import List

from pydantic import BaseModel

from .entity_unique_id import EntityUniqueId
from .platform import Platform


class APIResponse(BaseModel):
    """
    Represents a response from the API.

    :ivar entity_unique_id: The unique identifier of the entity.
    :ivar user_country: The country of the user.
    :ivar page_url: The URL of the page.
    :ivar entities_by_unique_id: List of unique identifiers for entities.
    :ivar links_by_platform: List of platform links.
    """

    entity_unique_id: str
    user_country: str
    page_url: str
    entities_by_unique_id: List[EntityUniqueId]
    links_by_platform: List[Platform]


__all__ = ("APIResponse",)
