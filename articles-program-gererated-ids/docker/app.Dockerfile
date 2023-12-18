ARG BUILD_ENVIRONMENT="local"

FROM runtime-image

ENV HOME_PATH="/home/artms-controller"
ENV PATH=".venv/bin:${PATH}"
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
                artms-controller \
    && useradd --uid 1000 \
               --gid artms-controller \
               --home ${HOME_PATH} \
               --shell /bin/bash \
               artms-controller \
    && chown --recursive \
             artms-controller:artms-controller \
             ./

USER artms-controller

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
