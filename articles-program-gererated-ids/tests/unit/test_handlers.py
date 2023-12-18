"""Unit tests related to handlers."""

import uuid

import pytest

from src.domain import commands
from src.domain.model import Article
from src.services.message_bus import MessageBus

from ..conftest import handle
from .conftest import FakeUnitOfWork


class ServiceClass:
    @staticmethod
    async def create_articles_in_repository(
        fake_uow: FakeUnitOfWork,
        *article_data: dict,
    ) -> list[uuid.UUID] | uuid.UUID:
        cmds = [
            commands.CreateArticle(
                one_dict["title"],
                one_dict["preview"],
                one_dict["body"],
                one_dict["created_by"],
            )
            for one_dict in article_data
        ]
        result = [await handle(MessageBus(uow=fake_uow), one_command) for one_command in cmds]
        return result[0] if len(result) == 1 else result

    @staticmethod
    async def update_and_retrieve_article(
        fake_uow: FakeUnitOfWork,
        article_id: uuid.UUID,
        patch_data: dict,
    ) -> Article | None:
        patch_data["article_id"] = article_id
        await handle(
            MessageBus(uow=fake_uow),
            commands.UpdateArticle(**patch_data),
        )
        return await fake_uow.article_repository.retrieve_article_by_id(article_id)

    @staticmethod
    async def delete_and_retrieve_article(
        fake_uow: FakeUnitOfWork,
        article_id: uuid.UUID,
    ) -> Article | None:
        await handle(
            MessageBus(uow=fake_uow),
            commands.DeleteArticle(article_id),
        )
        return await fake_uow.article_repository.retrieve_article_by_id(article_id)


class TestArticleHandlers:
    async def test_can_create_article(self, fake_uow: FakeUnitOfWork) -> None:
        article_id: uuid.UUID = (
            await ServiceClass.create_articles_in_repository(  # type: ignore[assignment]
                fake_uow,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )
        )

        articles = await fake_uow.article_repository.retrieve_all_articles()

        assert fake_uow.committed
        assert articles[0].article_id == article_id
        assert articles[0].title == "TITLE"
        assert articles[0].preview == "PREVIEW"
        assert articles[0].body == "BODY"
        assert articles[0].created_by == 1

    @pytest.mark.parametrize(
        ("patch_data", "result"),
        [
            (
                {"title": None, "preview": None, "body": None},
                {"title": "TITLE", "preview": "PREVIEW", "body": "BODY"},
            ),
            (
                {"title": "ANOTHER TITLE", "preview": None, "body": None},
                {"title": "ANOTHER TITLE", "preview": "PREVIEW", "body": "BODY"},
            ),
            (
                {"title": None, "preview": "ANOTHER PREVIEW", "body": None},
                {"title": "TITLE", "preview": "ANOTHER PREVIEW", "body": "BODY"},
            ),
            (
                {"title": None, "preview": None, "body": "ANOTHER BODY"},
                {"title": "TITLE", "preview": "PREVIEW", "body": "ANOTHER BODY"},
            ),
            (
                {"title": "ANOTHER TITLE", "preview": "ANOTHER PREVIEW", "body": "ANOTHER BODY"},
                {"title": "ANOTHER TITLE", "preview": "ANOTHER PREVIEW", "body": "ANOTHER BODY"},
            ),
        ],
    )
    async def test_can_update_article(
        self,
        patch_data: dict,
        result: dict,
        fake_uow: FakeUnitOfWork,
    ) -> None:
        article_id: uuid.UUID = (
            await ServiceClass.create_articles_in_repository(  # type: ignore[assignment]
                fake_uow,
                {
                    "title": "TITLE",
                    "preview": "PREVIEW",
                    "body": "BODY",
                    "created_by": 1,
                },
            )
        )

        article = await ServiceClass.update_and_retrieve_article(
            fake_uow,
            article_id,
            patch_data,
        )

        assert fake_uow.committed
        assert article
        assert article.article_id == article_id
        assert article.title == result["title"]
        assert article.preview == result["preview"]
        assert article.body == result["body"]
        assert article.created_by == 1

    async def test_can_delete_article(self, fake_uow: FakeUnitOfWork) -> None:
        article_ids: list[
            uuid.UUID
        ] = await ServiceClass.create_articles_in_repository(  # type: ignore[assignment]
            fake_uow,
            {
                "title": "FIRST TITLE",
                "preview": "FIRST PREVIEW",
                "body": "FIRST BODY",
                "created_by": 1,
            },
            {
                "title": "SECOND TITLE",
                "preview": "SECOND PREVIEW",
                "body": "SECOND BODY",
                "created_by": 2,
            },
        )

        await ServiceClass.delete_and_retrieve_article(fake_uow, article_ids[1])

        articles = await fake_uow.article_repository.retrieve_all_articles()

        assert fake_uow.committed
        assert articles[0].article_id == article_ids[0]
        assert articles[0].title == "FIRST TITLE"
        assert articles[0].preview == "FIRST PREVIEW"
        assert articles[0].body == "FIRST BODY"
        assert articles[0].created_by == 1
