from pydantic import BaseModel

from ..enums.platform_name import PlatformName


class Platform(BaseModel, use_enum_values=True):
    """
    Represents a platform associated with an entity.

    :ivar name: The name of the platform.
    :ivar country: The country of the platform.
    :ivar entity_unique_id: The unique identifier of the entity.
    :ivar url: The URL of the platform.
    :ivar native_app_uri_mobile: Optional. The native app URI for mobile devices.
    :ivar native_app_uri_desktop: Optional. The native app URI for desktop devices.
    """

    name: PlatformName
    country: str
    entity_unique_id: str
    url: str
    native_app_uri_mobile: str | None
    native_app_uri_desktop: str | None


__all__ = ("Platform",)
