"""Unit tests related to FastAPI app."""

from src.main import app


class TestFastapiApp:
    def test_app_attributes(self) -> None:
        assert app.title == "Articles Microservice"
        assert app.summary == "Provides with ability to manipulate articles."
        assert app.description == (
            "Articles Microservice is one of the **core** microservices.\n"
            "It provides with ability to perform CRUD operations."
        )
        assert app.version == "0.1.0"
        assert app.contact == {
            "name": "Denis Borisov",
            "email": "denis.borisov@hotmail.com",
            "url": "https://www.linkedin.com/in/borisovdenis/",
        }
        assert app.docs_url == "/api/docs"
        assert app.redoc_url == "/api/redoc"
