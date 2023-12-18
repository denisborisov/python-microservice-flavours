"""Container with product repository."""

from dependency_injector import containers, providers

from ..adapters.google_flashcard_repository import GoogleFlashcardRepository


class GoogleFlashcardRepositoryContainer(containers.DeclarativeContainer):
    google_flashcard_repository: providers.Singleton = providers.Singleton(
        GoogleFlashcardRepository,
    )
