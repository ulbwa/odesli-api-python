from enum import Enum

from typing import List
from typing import Optional

from pydantic import BaseModel


class PlatformName(str, Enum):
    spotify = "spotify"
    itunes = "itunes"
    apple_music = "appleMusic"
    youtube = "youtube"
    youtube_music = "youtubeMusic"
    google = "google"
    google_store = "googleStore"
    pandora = "pandora"
    deezer = "deezer"
    tidal = "tidal"
    amazon_store = "amazonStore"
    amazon_music = "amazonMusic"
    soundcloude = "soundcloud"
    napster = "napster"
    yandex_music = "yandex"
    spinrilla = "spinrilla"
    audius = "audius"
    audiomack = "audiomack"
    anghami = "anghami"
    boomplay = "boomplay"
    bandcamp = "bandcamp"


class Platform(BaseModel):
    name: PlatformName
    country: str
    entity_unique_id: str
    url: str
    native_app_uri_mobile: Optional[str]
    native_app_uri_desktop: Optional[str]

    class Config:
        use_enum_values = True


class APIProvider(str, Enum):
    spotify = "spotify"
    itunes = "itunes"
    youtube = "youtube"
    google = "google"
    pandora = "pandora"
    deezer = "deezer"
    tidal = "tidal"
    amazon = "amazon"
    soundcloud = "soundcloud"
    napster = "napster"
    yandex_music = "yandex"
    spinrilla = "spinrilla"
    audius = "audius"
    audiomack = "audiomack"
    anghami = "anghami"
    boomplay = "boomplay"
    bandcamp = "bandcamp"


class EntityType(str, Enum):
    song = "song"
    album = "album"


class EntityUniqueId(BaseModel):
    id: str
    type: EntityType
    title: Optional[str]
    artist_name: Optional[str]
    thumbnail_url: Optional[str]
    thumbnail_width: Optional[int]
    thumbnail_height: Optional[int]
    api_provider: APIProvider
    platforms: List[PlatformName]

    class Config:
        use_enum_values = True


class APIResponse(BaseModel):
    entity_unique_id: str
    user_country: str
    page_url: str
    entities_by_unique_id: List[EntityUniqueId]
    links_by_platform: List[Platform]
