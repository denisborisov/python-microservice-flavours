ARG BUILD_ENVIRONMENT="local"

FROM runtime-image

ENV HOME_PATH="/home/translation-controller"
ENV PATH=".venv/bin:${PATH}"
ENV GOOGLE_TRANSLATOR_URL=""
ENV WEB_SCRAPER_TIMEOUT=""

ENV DICTIONARY_LINK_CSS_SELECTOR=""
ENV BUTTON_CSS_SELECTOR=""
ENV DEFINITION_CSS_SELECTOR=""
ENV SYNONYM_CSS_SELECTOR=""
ENV TRANSLATION_CSS_SELECTOR=""
ENV EXAMPLE_CSS_SELECTOR=""

ENV POSTGRES_DSN=""

WORKDIR ${HOME_PATH}

COPY ["src", "./src"]
COPY ["docker/app.Dockerfile", \
      "docker/runtime.Dockerfile", \
      "poetry.lock", \
      "pyproject.toml", \
      "./"]

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main \
    && groupadd --gid 1000 \
                flashcards-controller \
    && useradd --uid 1000 \
               --gid flashcards-controller \
               --home ${HOME_PATH} \
               --shell /bin/bash \
               flashcards-controller \
    && chown --recursive \
             flashcards-controller:flashcards-controller \
             ./

USER flashcards-controller

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
