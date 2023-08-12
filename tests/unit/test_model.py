"""Unit tests related to model."""

import pytest

from src.domain import model


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
        article = model.Article(title, preview, body, created_by)

        assert article.title == title
        assert article.preview == preview
        assert article.body == body
        assert article.created_by == created_by

    @pytest.mark.parametrize(
        (
            "first_title", "first_preview", "first_body", "first_created_by",
            "second_title", "second_preview", "second_body", "second_created_by",
            "equality", "cardinality",
        ),
        [
            (
                "First Title", "First Preview", "First Body", 1,
                "First Title", "First Preview", "First Body", 1,
                True, 1,
            ),
            (
                "First Title", "First Preview", "First Body", 1,
                "Second Title", "First Preview", "First Body", 1,
                False, 2,
            ),
            (
                "First Title", "First Preview", "First Body", 1,
                "First Title", "Second Preview", "First Body", 1,
                False, 2,
            ),
            (
                "First Title", "First Preview", "First Body", 1,
                "First Title", "First Preview", "Second Body", 1,
                False, 2,
            ),
            (
                "First Title", "First Preview", "First Body", 1,
                "First Title", "First Preview", "First Body", 2,
                False, 2,
            ),
        ],
    )
    def test_article_identity_is_based_on_title_preview_body_created_by(  # noqa: PLR0913
        self,
        first_title: str, first_preview: str, first_body: str, first_created_by: int,
        second_title: str, second_preview: str, second_body: str, second_created_by: int,
        equality: bool, cardinality: int,
    ) -> None:
        article_1 = model.Article(first_title, first_preview, first_body, first_created_by)
        article_2 = model.Article(second_title, second_preview, second_body, second_created_by)

        assert (article_1 == article_2) is equality
        assert len({article_1, article_2}) == cardinality
