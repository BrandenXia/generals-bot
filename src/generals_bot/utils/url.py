from typing import Mapping, Self
from urllib.parse import urlunparse, urlencode


class URL:
    """URL builder class"""

    def __init__(
            self,
            scheme: str = "https",
            netloc: str = "",
            url: str = "",
            params: str = "",
            query: Mapping[str, str] | None = None,
            fragment: str = "",
    ):
        self._scheme = scheme
        self._netloc = netloc
        self._url = url
        self._params = params
        self._query: Mapping[str, str] = query or {}
        self._fragment = fragment

    def scheme(self, scheme: str) -> Self:
        self._scheme = scheme
        return self

    def netloc(self, netloc: str) -> Self:
        self._netloc = netloc
        return self

    def url(self, url: str) -> Self:
        self._url = url
        return self

    def query(self, query: Mapping[str, str]) -> Self:
        self._query = query
        return self

    def fragment(self, fragment: str) -> Self:
        self._fragment = fragment
        return self

    def build(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return urlunparse(
            (
                self._scheme,
                self._netloc,
                self._url,
                self._params,
                urlencode(self._query),
                self._fragment,
            )
        )
