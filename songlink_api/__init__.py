from typing import Optional
from typing import Union

from songlink_api.types.exceptions import APIException
from songlink_api.types.exceptions import TooManyRequests
from songlink_api.types.exceptions import EntityNotFound

from songlink_api.types import PlatformName
from songlink_api.types import EntityType
from songlink_api.types import EntityUniqueId
from songlink_api.types import APIResponse
from songlink_api.types import APIProvider
from songlink_api.types import Platform

import httpx_cache
import orjson
import pkg_resources
import datetime

try:
    __version__ = pkg_resources.get_distribution("songlink_api").version
except pkg_resources.DistributionNotFound:
    __version__ = ""


class SongLink:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: str = "https://api.song.link/",
        api_version: str = "v1-alpha.1",
        api_timeout: int = 60,
        use_cache: bool = True,
        cache_time: int = 900,
    ) -> None:
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.api_version = api_version
        self.api_timeout = api_timeout
        self.use_cache = use_cache
        self.cache_time = cache_time
        self.__throttling_reset_in = None

    def __repr__(self) -> str:
        return f"<SongLink at {hex(id(self))}>"

    async def __make_request(
        self, method: str, params: Optional[dict] = None
    ) -> APIResponse:
        if (
            self.__throttling_reset_in is not None
            and self.__throttling_reset_in >= datetime.datetime.now()
        ):
            raise TooManyRequests()

        async with httpx_cache.AsyncClient(
            headers={
                "User-Agent": f"SongLinkAPI/v{__version__}",
                "cache-control": f"max-age={self.cache_time}"
                if self.use_cache
                else "no-cache",
            },
            cache=httpx_cache.FileCache(),
            always_cache=True,
        ) as client:
            request = client.build_request(
                "GET",
                f"{self.api_url}/{self.api_version}/{method}",
                params={
                    **(
                        {k: v for k, v in params.items() if v is not None}
                        if params is not None
                        else {}
                    ),
                    **({"key": self.api_key} if self.api_key is not None else {}),
                },
                timeout=self.api_timeout,
            )
            response = await client.send(request)
            try:
                data = orjson.loads(response.content)
            except Exception:
                data = {}
            if response.status_code != 200 or data == {}:
                reason = data.get("code")
                if reason == "too_many_requests":
                    self.__throttling_reset_in = (
                        datetime.datetime.now()
                        + datetime.timedelta(seconds=self.api_timeout)
                    )
                    raise TooManyRequests()
                if reason == "could_not_fetch_entity_data":
                    raise EntityNotFound()
                else:
                    raise APIException(status_code=response.status_code, message=reason)

            return APIResponse(
                entity_unique_id=data.get("entityUniqueId"),
                user_country=data.get("userCountry", params.get("userCountry", "US")),
                page_url=data.get("pageUrl"),
                entities_by_unique_id=[
                    EntityUniqueId(
                        id=entity.get("id"),
                        type=entity.get("type"),
                        title=entity.get("title"),
                        artist_name=entity.get("artistName"),
                        thumbnail_url=entity.get("thumbnailUrl"),
                        thumbnail_width=entity.get("thumbnailWidth"),
                        thumbnail_height=entity.get("thumbnailHeight"),
                        api_provider=entity.get("apiProvider"),
                        platforms=[
                            PlatformName(platform_name)
                            for platform_name in entity.get("platforms")
                            if entity.get("platforms") in list(PlatformName)
                        ],
                    )
                    for entity in data.get("entitiesByUniqueId").values()
                    if entity.get("apiProvider") in list(APIProvider)
                ],
                links_by_platform=[
                    Platform(
                        name=platform_name,
                        country=platform.get("country"),
                        entity_unique_id=platform.get("entityUniqueId"),
                        url=platform.get("url"),
                        native_app_uri_mobile=platform.get("nativeAppUriMobile"),
                        native_app_uri_desktop=platform.get("nativeAppUriDesktop"),
                    )
                    for platform_name, platform in data.get("linksByPlatform").items()
                    if platform_name in list(PlatformName)
                ],
            )

    async def links_by_url(
        self,
        url: str,
        user_country: str = "US",
        song_if_single: bool = False,
    ) -> APIResponse:
        return await self.__make_request(
            method="links",
            params={
                "url": url,
                "userCountry": user_country,
                "songIfSingle": "true" if song_if_single else "false",
            },
        )

    async def links_by_id(
        self,
        id: Union[str, int],
        platform: PlatformName,
        type: EntityType,
        user_country: str = "US",
        song_if_single: bool = False,
    ) -> APIResponse:
        return await self.__make_request(
            method="links",
            params={
                "id": id,
                "platform": platform.name,
                "type": type.name,
                "userCountry": user_country,
                "songIfSingle": "true" if song_if_single else "false",
            },
        )
