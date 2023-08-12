"""Container with HTTP client."""

from dependency_injector import containers, providers

from ..services.http_client import HttpxClient


class HttpClientContainer(containers.DeclarativeContainer):
    http_client: providers.Singleton = providers.Singleton(HttpxClient)
