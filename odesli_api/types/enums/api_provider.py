from enum import StrEnum


class APIProvider(StrEnum):
    """
    Enum representing various music streaming service providers.
    """

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


__all__ = ("APIProvider",)
