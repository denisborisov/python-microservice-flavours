"""Unit tests related to schemata."""

import uuid

from src.domain import schemata


class TestArticles:
    def test_can_create_article(self) -> None:
        article_id = uuid.uuid4
        article = schemata.Article(
            article_id=str(article_id),
            title="Title",
            preview="Preview",
            body="Body",
            created_by=1,
        )
        assert article.article_id == str(article_id)
        assert article.title == "Title"
        assert article.preview == "Preview"
        assert article.body == "Body"
        assert article.created_by == 1
