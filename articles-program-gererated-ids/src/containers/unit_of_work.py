"""Container with SQLAlchemy unit of work."""

from dependency_injector import containers, providers

from ..services.unit_of_work import SqlAlchemyUnitOfWork


class SqlAlchemyUnitOfWorkContainer(containers.DeclarativeContainer):
    sql_alchemy_unit_of_work: providers.Singleton = providers.Singleton(SqlAlchemyUnitOfWork)
