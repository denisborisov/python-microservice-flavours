"""Exceptions."""

import traceback


class FlashcardCreationError(Exception):
    pass


class FlashcardDeletionError(Exception):
    pass


class CommandHandlingError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


class WebScraperError(Exception):
    def __init__(self) -> None:
        traceback.print_exc()
