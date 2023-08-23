ARG BUILD_ENVIRONMENT="local"

FROM runtime-image

ENV HOME_PATH="/home/artms-controller"
ENV PATH=".venv/bin:${PATH}"
ENV POSTGRES_DSN=""

WORKDIR ${HOME_PATH}

COPY ["src", "./src"]
COPY ["docker/app.Dockerfile", "docker/runtime.Dockerfile", "poetry.lock", "pyproject.toml", "./"]

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main \
    && groupadd -g 1000 artms-controller \
    && useradd -u 1000 -g artms-controller -d ${HOME_PATH} -m -s /bin/bash artms-controller \
    && chown -R artms-controller:artms-controller ./

USER artms-controller

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
