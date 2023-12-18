"""Unit tests related to commands."""

import uuid

import pytest

from src import domain


class TestCreateArticleCommand:
    def test_cannot_create_with_empty_title(self) -> None:
        with pytest.raises(domain.exceptions.ArticleCreationError) as exc_info:
            domain.commands.CreateArticle(" ", "Preview", "Body", created_by=1)

        assert exc_info.value.args[0] == "Cannot create an article with an empty title."

    def test_cannot_create_with_empty_preview(self) -> None:
        with pytest.raises(domain.exceptions.ArticleCreationError) as exc_info:
            domain.commands.CreateArticle("Title", " ", "Body", created_by=1)

        assert exc_info.value.args[0] == "Cannot create an article with an empty preview."

    def test_cannot_create_with_empty_body(self) -> None:
        with pytest.raises(domain.exceptions.ArticleCreationError) as exc_info:
            domain.commands.CreateArticle("Title", "Preview", " ", created_by=1)

        assert exc_info.value.args[0] == "Cannot create an article with an empty body."

    def test_strips_title(self) -> None:
        command = domain.commands.CreateArticle(" Title ", "Preview", "Body", created_by=1)

        assert command.title == "Title"

    def test_strips_preview(self) -> None:
        command = domain.commands.CreateArticle("Title", " Preview ", "Body", created_by=1)

        assert command.preview == "Preview"

    def test_strips_body(self) -> None:
        command = domain.commands.CreateArticle("Title", "Preview", " Body ", created_by=1)

        assert command.body == "Body"


class TestUpdateArticleCommand:
    def test_cannot_update_with_empty_title(self) -> None:
        with pytest.raises(domain.exceptions.ArticleModificationError) as exc_info:
            domain.commands.UpdateArticle(uuid.uuid4(), " ", "Preview", "Body")

        assert exc_info.value.args[0] == "Cannot update an article with an empty title."

    def test_cannot_update_with_empty_preview(self) -> None:
        with pytest.raises(domain.exceptions.ArticleModificationError) as exc_info:
            domain.commands.UpdateArticle(uuid.uuid4(), "Title", " ", "Body")

        assert exc_info.value.args[0] == "Cannot update an article with an empty preview."

    def test_cannot_update_with_empty_body(self) -> None:
        with pytest.raises(domain.exceptions.ArticleModificationError) as exc_info:
            domain.commands.UpdateArticle(uuid.uuid4(), "Title", "Preview", " ")

        assert exc_info.value.args[0] == "Cannot update an article with an empty body."

    def test_strips_title(self) -> None:
        command = domain.commands.UpdateArticle(uuid.uuid4(), " Title ", "Preview", "Body")

        assert command.title == "Title"

    def test_strips_preview(self) -> None:
        command = domain.commands.UpdateArticle(uuid.uuid4(), "Title", " Preview ", "Body")

        assert command.preview == "Preview"

    def test_strips_body(self) -> None:
        command = domain.commands.UpdateArticle(uuid.uuid4(), "Title", "Preview", " Body ")

        assert command.body == "Body"
