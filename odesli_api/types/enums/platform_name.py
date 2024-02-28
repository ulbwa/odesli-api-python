from enum import StrEnum


class PlatformName(StrEnum):
    """
    Enumeration representing various platform names.
    """

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


__all__ = ("PlatformName",)
