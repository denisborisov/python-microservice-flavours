"""Unit tests related to containers wiring."""

from fastapi import FastAPI
from src import adapters, routines, services
from src.api import endpoints
from src.containers.wiring import attach_containers_to_app


class ServiceClass:
    @staticmethod
    def create_fastapi_app() -> FastAPI:
        app = FastAPI()
        attach_containers_to_app(app)
        return app


class TestDependencyInjection:
    def test_containers_attached_to_app(self) -> None:
        app = ServiceClass.create_fastapi_app()

        containers = [attribute for attribute in app.__dict__ if attribute.endswith("_container")]

        assert len(containers) == 6  # noqa: PLR2004
        assert getattr(app, "database_engine_container", None)
        assert getattr(app, "google_flashcard_repository_container", None)
        assert getattr(app, "web_scraper_container", None)
        assert getattr(app, "message_bus_container", None)
        assert getattr(app, "session_factory_container", None)
        assert getattr(app, "unit_of_work_container", None)

    def test_required_modules_are_wired_to_containers(self) -> None:
        app = ServiceClass.create_fastapi_app()

        assert getattr(app, "database_engine_container").wired_to_modules == [
            routines.database_engine,
            services.session_factory,
        ]
        assert getattr(app, "google_flashcard_repository_container").wired_to_modules == [
            services.unit_of_work,
        ]
        assert getattr(app, "web_scraper_container").wired_to_modules == [
            adapters.google_flashcard_repository,
        ]
        assert getattr(app, "message_bus_container").wired_to_modules == [
            endpoints.flashcards,
            routines.message_bus,
        ]
        assert getattr(app, "session_factory_container").wired_to_modules == [
            services.unit_of_work,
        ]
        assert getattr(app, "unit_of_work_container").wired_to_modules == [
            services.message_bus,
        ]
