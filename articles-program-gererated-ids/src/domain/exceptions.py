"""Exceptions."""


class ArticleCreationError(Exception):
    pass


class ArticleModificationError(Exception):
    pass


class ArticleDeletionError(Exception):
    pass


class CommandHandlingError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


class NetworkConnectionError(Exception):
    pass
