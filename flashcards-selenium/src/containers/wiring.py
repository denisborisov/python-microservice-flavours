"""Wiring containers with modules."""

from fastapi import FastAPI

from .. import adapters, routines, services
from ..api import endpoints
from .database_engine import DatabaseEngineContainer
from .web_scraper import WebScraperContainer
from .google_flashcard_repository import GoogleFlashcardRepositoryContainer
from .message_bus import MessageBusContainer
from .session_factory import SessionFactoryContainer
from .unit_of_work import SqlAlchemyUnitOfWorkContainer


def attach_containers_to_app(app: FastAPI) -> None:
    database_engine_container = DatabaseEngineContainer()
    database_engine_container.wire(modules=[routines.database_engine, services.session_factory])
    setattr(app, "database_engine_container", database_engine_container)

    session_factory_container = SessionFactoryContainer()
    session_factory_container.wire(modules=[services.unit_of_work])
    setattr(app, "session_factory_container", session_factory_container)

    unit_of_work_container = SqlAlchemyUnitOfWorkContainer()
    unit_of_work_container.wire(modules=[services.message_bus])
    setattr(app, "unit_of_work_container", unit_of_work_container)

    message_bus_container = MessageBusContainer()
    message_bus_container.wire(
        modules=[endpoints.flashcards, routines.message_bus],
    )
    setattr(app, "message_bus_container", message_bus_container)

    web_scraper_container = WebScraperContainer()
    web_scraper_container.wire(
        modules=[adapters.google_flashcard_repository],
    )
    setattr(app, "web_scraper_container", web_scraper_container)

    google_flashcard_repository_container = GoogleFlashcardRepositoryContainer()
    google_flashcard_repository_container.wire(
        modules=[services.unit_of_work],
    )
    setattr(app, "google_flashcard_repository_container", google_flashcard_repository_container)
