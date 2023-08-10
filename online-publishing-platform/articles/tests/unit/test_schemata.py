"""Unit tests related to schemata."""

from src.domain import schemata


class TestArticles:
    def test_can_create_article(self) -> None:
        article = schemata.Article(
            article_id=1,
            title="Title",
            preview="Preview",
            body="Body",
            created_by=1,
        )
        assert article.article_id == 1
        assert article.title == "Title"
        assert article.preview == "Preview"
        assert article.body == "Body"
        assert article.created_by == 1
