"""Unit tests related to schemata."""

import uuid

import pytest

from src.domain import schemata


class TestArticlePost:
    def test_can_create_article_post(self) -> None:
        article = schemata.ArticlePost(
            title="Title",
            preview="Preview",
            body="Body",
            created_by=1,
        )

        assert article.title == "Title"
        assert article.preview == "Preview"
        assert article.body == "Body"
        assert article.created_by == 1

    def test_article_post_contains_valid_config(self) -> None:
        example = schemata.ArticlePost.model_config["json_schema_extra"]["examples"][0]

        assert example["title"] == "Заголовок статьи"
        assert example["preview"] == (
            "Небольшое превью, размером с абзац-два, чтобы понять, о чём идёт речь в статье."
        )
        assert example["body"] == "Содержимое статьи, сколь угодно большое"
        assert example["created_by"] == 1


class TestArticle:
    def test_can_create_article(self) -> None:
        article_id = uuid.uuid4()

        article = schemata.Article(
            article_id=article_id,
            title="Title",
            preview="Preview",
            body="Body",
            created_by=1,
        )

        assert article.article_id == article_id
        assert article.title == "Title"
        assert article.preview == "Preview"
        assert article.body == "Body"
        assert article.created_by == 1

    def test_article_contains_valid_config(self) -> None:
        example = schemata.Article.model_config["json_schema_extra"]["examples"][0]

        assert isinstance(example["article_id"], uuid.UUID)
        assert example["title"] == "Заголовок статьи"
        assert example["preview"] == (
            "Небольшое превью, размером с абзац-два, чтобы понять, о чём идёт речь в статье."
        )
        assert example["body"] == "Содержимое статьи, сколь угодно большое"
        assert example["created_by"] == 1


class TestArticlePatch:
    @pytest.mark.parametrize(
        ("patch_data"),
        [
            ({}),
            ({"title": "Another Title"}),
            ({"preview": "Another Preview"}),
            ({"body": "Another Body"}),
            (
                {
                    "title": "Another Title",
                    "preview": "Another Preview",
                    "body": "Another Body",
                }
            ),
        ],
    )
    def test_can_create_article_patch(self, patch_data: dict) -> None:
        article = schemata.ArticlePatch(**patch_data)

        assert article.title == patch_data.get("title")
        assert article.preview == patch_data.get("preview")
        assert article.body == patch_data.get("body")

    def test_article_post_contains_valid_config(self) -> None:
        example = schemata.ArticlePost.model_config["json_schema_extra"]["examples"][0]

        assert example["title"] == "Заголовок статьи"
        assert example["preview"] == (
            "Небольшое превью, размером с абзац-два, чтобы понять, о чём идёт речь в статье."
        )
        assert example["body"] == "Содержимое статьи, сколь угодно большое"
