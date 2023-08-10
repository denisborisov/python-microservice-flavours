"""Unit tests related to FastAPI app."""

from src.main import app


class TestFastapiApp:
    def test_app_attributes(self) -> None:
        assert app.docs_url == "/api/docs"
        assert app.redoc_url == "/api/redoc"
        assert app.title == "Articles Microservice"
        assert app.description == "This is an article microservice."
        assert app.version == "0.1.0"
        assert app.contact == {
            "name": "Denis Borisov",
            "email": "denis.borisov@hotmail.com",
        }
