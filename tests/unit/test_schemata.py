"""Unit tests related to schemata."""

import uuid

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
        config = schemata.ArticlePost.Config.json_schema_extra

        assert config["example"]["title"] == "Заголовок статьи"
        assert config["example"]["preview"] == (
            "Небольшое превью, размером с абзац-два, чтобы понять, о чём идёт речь в статье."
        )
        assert config["example"]["body"] == "Содержимое статьи, сколь угодно большое"
        assert config["example"]["created_by"] == 1


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
        config = schemata.Article.Config.json_schema_extra

        assert isinstance(config["example"]["article_id"], uuid.UUID)
        assert config["example"]["title"] == "Заголовок статьи"
        assert config["example"]["preview"] == (
            "Небольшое превью, размером с абзац-два, чтобы понять, о чём идёт речь в статье."
        )
        assert config["example"]["body"] == "Содержимое статьи, сколь угодно большое"
        assert config["example"]["created_by"] == 1
