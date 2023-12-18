ARG BUILD_ENVIRONMENT="local"
ARG REVISION=
ARG ROLLBACK_REVISION=

FROM runtime-image

ARG REVISION
ARG ROLLBACK_REVISION

ENV HOME_PATH="/home/translation-controller"
ENV PATH=".venv/bin:${PATH}"
ENV POSTGRES_DSN=""

WORKDIR ${HOME_PATH}

COPY ["alembic", "./alembic"]
COPY ["alembic.ini", \
      "docker/migration.Dockerfile", \
      "docker/runtime.Dockerfile", \
      "poetry.lock",\
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
             ./ \
    && echo "python -m alembic upgrade ${REVISION}" > upgrade.sh \
    && echo "python -m alembic downgrade ${ROLLBACK_REVISION}" > rollback.sh \
    && chmod +x upgrade.sh \
    && chmod +x rollback.sh

USER flashcards-controller

ENTRYPOINT ["/bin/bash"]
