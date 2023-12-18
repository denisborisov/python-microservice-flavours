"""Container with HTTP client."""

from dependency_injector import containers, providers

from ..services.web_scraper import SeleniumWebScraper


class WebScraperContainer(containers.DeclarativeContainer):
    web_scraper: providers.Singleton = providers.Singleton(SeleniumWebScraper)
