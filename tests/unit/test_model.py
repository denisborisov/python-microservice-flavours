"""Unit tests related to model."""

import uuid

import pytest

from src.domain import model


class ServiceClass:
    @staticmethod
    def create_aricle(
        article_data: dict,
    ) -> model.Article:
        article = model.Article(
            article_data["title"],
            article_data["preview"],
            article_data["body"],
            article_data["created_by"],
        )
        article.article_id = article_data.get("article_id") or article.article_id
        return article


class TestArticles:
    @pytest.mark.parametrize(
        ("title", "preview", "body", "created_by"),
        [
            ("Title", "Preview", "Body", 1),
            (" ", " ", " ", 0),
            ("", "", "", -1),
        ],
    )
    def test_can_create_article(
        self,
        title: str,
        preview: str,
        body: str,
        created_by: int,
    ) -> None:
        article = ServiceClass.create_aricle(
            {
                "title": title,
                "preview": preview,
                "body": body,
                "created_by": created_by,
            },
        )

        assert isinstance(article.article_id, uuid.UUID)
        assert article.title == title
        assert article.preview == preview
        assert article.body == body
        assert article.created_by == created_by

    @pytest.mark.parametrize(
        (
            "a_article_id",
            "a_title",
            "a_preview",
            "a_body",
            "a_created_by",
            "b_article_id",
            "b_title",
            "b_preview",
            "b_body",
            "b_created_by",
            "equality",
            "cardinality",
        ),
        [
            (
                "24dcf370-...-644867b63186",
                "First Title",
                "First Preview",
                "First Body",
                1,
                "24dcf370-...-644867b63186",
                "Second Title",
                "Second Preview",
                "Second Body",
                2,
                True,
                1,
            ),
            (
                "24dcf370-...-644867b63186",
                "First Title",
                "First Preview",
                "First Body",
                1,
                "03d2ca1e-...-1c8d75e074da",
                "First Title",
                "First Preview",
                "First Body",
                1,
                False,
                2,
            ),
        ],
    )
    def test_article_identity_is_based_on_article_id(  # noqa: PLR0913
        self,
        a_article_id: uuid.UUID,
        a_title: str,
        a_preview: str,
        a_body: str,
        a_created_by: int,
        b_article_id: uuid.UUID,
        b_title: str,
        b_preview: str,
        b_body: str,
        b_created_by: int,
        equality: bool,
        cardinality: int,
    ) -> None:
        article_1 = ServiceClass.create_aricle(
            {
                "article_id": a_article_id,
                "title": a_title,
                "preview": a_preview,
                "body": a_body,
                "created_by": a_created_by,
            },
        )

        article_2 = ServiceClass.create_aricle(
            {
                "article_id": b_article_id,
                "title": b_title,
                "preview": b_preview,
                "body": b_body,
                "created_by": b_created_by,
            },
        )

        assert (article_1 == article_2) is equality
        assert len({article_1, article_2}) == cardinality
