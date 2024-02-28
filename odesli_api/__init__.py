import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union

import orjson
from aiohttp_client_cache import CacheBackend, FileBackend, CachedSession
from aiohttp_proxy import ProxyConnector
from fake_headers import Headers

from .types import *


class Odesli:
    """
    Asynchronous client for interacting with the Odesli API.

    :ivar api_url: The base URL of the Odesli API.
    :ivar api_timeout: The timeout duration for API requests in seconds.
    :ivar api_key: Optional. The API key for accessing the Odesli API.
    :ivar api_version: The version of the Odesli API to use.
    :ivar always_use_proxy: Whether to always use a proxy for API requests.
    :ivar cache_backend: Optional. Cache backend for caching API responses.
    """

    api_url: str
    api_timeout: int
    always_use_proxy: bool
    cache_backend: Optional[CacheBackend]

    __connections: Dict[Optional[str], Optional[datetime]]

    def __init__(
        self,
        api_url: str = "https://api.song.link/",
        api_timeout: int = 60,
        api_key: Optional[str] = None,
        api_version: str = "v1-alpha.1",
        proxy: Optional[Union[List[str], str]] = None,
        always_use_proxy: bool = False,
        cache_backend: Optional[CacheBackend] = FileBackend(
            expire_after=timedelta(days=31),
            ignored_parameters=["key"],
            allowed_codes=(200,),
            allowed_methods=["GET", "POST"],
            cache_control=False,
            use_temp=True,
        ),
    ):
        """
        Initializes the Odesli client.

        :param api_url: The base URL of the Odesli API.
        :param api_timeout: The timeout duration for API requests in seconds.
        :param api_key: Optional. The API key for accessing the Odesli API.
        :param api_version: The version of the Odesli API to use.
        :param proxy: Optional. Proxy settings for making API requests.
        :param always_use_proxy: Whether to always use a proxy for API requests.
        :param cache_backend: Optional. Cache backend for caching API responses.
        """

        self.api_url = api_url.rstrip("/")
        self.api_timeout = api_timeout
        self.api_key: str | None = api_key
        self.api_version: str = api_version
        self.always_use_proxy = always_use_proxy
        self.cache_backend = cache_backend

        self.__connections = {}
        if proxy is not None:
            for _proxy in proxy if isinstance(proxy, list) else [proxy]:
                self.__connections[_proxy] = None
        if not always_use_proxy:
            self.__connections[None] = None
        if not self.__connections:
            raise ValueError("No connectors specified.")

    def __repr__(self) -> str:
        """
        Return the string representation of the Odesli instance.

        :return: String representation of the Odesli instance.
        """
        return f"<Odesli at {hex(id(self))}>"

    async def __make_request(
        self,
        method: str,
        params: Dict[str, int | str | float | bool | None] | None = None,
    ) -> APIResponse:
        """
        Makes an API request to the Odesli API.

        :param method: The API method to call.
        :param params: Optional. Parameters for the API request.

        :return: An APIResponse instance representing the API response.
        """
        if all(x is not None for x in self.__connections.values()):
            raise TooManyRequests()

        connection = random.choice(
            [x for x, i in self.__connections.items() if i is None]
        )

        async with CachedSession(
            connector=ProxyConnector.from_url(connection) if connection else None,
            cache=self.cache_backend,
            headers=Headers(os="windows", headers=True).generate(),
        ) as session:
            async with session.get(
                url=f"{self.api_url}/{self.api_version}/{method}",
                params={
                    **(params or {}),
                    **({"key": self.api_key} if self.api_key else {}),
                },
                timeout=self.api_timeout,
            ) as response:
                try:
                    data = orjson.loads(await response.read())
                except Exception as exception:
                    raise APIException(
                        status_code=response.status, message=str(exception)
                    ).with_traceback(exception.__traceback__)

                if response.status != 200 or not data:
                    reason = data.get("code")
                    if reason == "too_many_requests":
                        self.__connections[connection] = datetime.now() + timedelta(
                            seconds=self.api_timeout
                        )
                        raise TooManyRequests()
                    if reason == "could_not_fetch_entity_data":
                        raise EntityNotFound()
                    else:
                        raise APIException(status_code=response.status, message=reason)

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
                            if platform_name in list(PlatformName)
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
        """
        Retrieves music streaming links by URL.

        :param url: The URL for which to retrieve streaming links.
        :param user_country: Optional. The country of the user.
        :param song_if_single: Optional. Whether to treat a single track URL as a song. Default is False.

        :return: An APIResponse instance representing the API response.
        """
        return await self.__make_request(
            method="links",
            params={
                "url": url,
                "userCountry": user_country.upper(),
                "songIfSingle": "true" if song_if_single else "false",
            },
        )

    async def links_by_id(
        self,
        id: str | int,
        platform: PlatformName,
        type: EntityType,
        user_country: str = "US",
        song_if_single: bool = False,
    ) -> APIResponse:
        """
        Retrieves music streaming links by entity ID.

        :param id: The ID of the entity for which to retrieve streaming links.
        :param platform: The platform for which to retrieve streaming links.
        :param type: The type of the entity.
        :param user_country: Optional. The country of the user.
        :param song_if_single: Optional. Whether to treat a single track URL as a song. Default is False.

        :return: An APIResponse instance representing the API response.
        """
        return await self.__make_request(
            method="links",
            params={
                "id": id,
                "platform": platform.name,
                "type": type.name,
                "userCountry": user_country.upper(),
                "songIfSingle": "true" if song_if_single else "false",
            },
        )
