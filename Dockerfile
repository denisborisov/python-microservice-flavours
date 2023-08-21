# This Dockerfile contains four stages:
# - deps-image-gitlab
# - deps-image-local
# - deps-image
# - app-image
# 
# The purpose of the app-image stage is to create the final image containing our app.
# This stage is the one that should be built by kaniko on the build-app-image step,
# and it is defined in .gitlab-ci.yml file via --target app-image flag.
# 
# Both deps-image-gitlab and deps-image-local stages are destined to load and install all necessary dependencies -
# poetry dependencies in our case. We read Artifactory credentials from kaniko/creds file.
# This file has the following structure:
# 
# username
# password
# 
# And the main difference between deps-image-gitlab and deps-image-local is in the location of this file.
# If we want to run this Dockerfile locally, we should create this kaniko/creds file, placing kaniko folder
# at the same level as this Dockerfile.
# 
# The purpose of the deps-image stage as long as the BUILD_ENVIRONMENT argument variable
# is to switch between deps-image-gitlab and deps-image-local stages while running the app-image stage,
# particularly the COPY --from instruction.
# 
# So in order to run this Docker file locally, we should change the BUILD_ENVIRONMENT argument variable to "local".
# You can also see that this argument variable is set to 'gitlab' on the build-app-image step
# in .gitlab-ci.yml: --build-arg BUILD_ENVIRONMENT=gitlab, because there we want to use deps-image-gitlab
# inside the COPY --from instruction of the app-image stage.
# 
ARG BUILD_ENVIRONMENT="local"

# 
# Base image.
# 
FROM python:3.11-slim as base-image

RUN apt-get update --yes \
    && apt-get upgrade --yes \
    && pip install -U pip poetry \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf ~/.cache

FROM scratch AS runtime-image

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

COPY --from=base-image / /

# 
# This stage is fit for GitLab CI.
# 
FROM runtime-image AS deps-image-gitlab

COPY ["poetry.lock", "pyproject.toml", "./"]

RUN --mount=type=secret,id=creds \
    poetry config http-basic.borisov $(head -1 /kaniko/creds) $(tail -1 /kaniko/creds) \
    && poetry config http-basic.team-name $(head -1 /kaniko/creds) $(tail -1 /kaniko/creds) \
    && poetry config virtualenvs.in-project true \
    && poetry install --only main

# 
# This stage is fit for local development.
# 
FROM runtime-image AS deps-image-local

COPY ["kaniko", "./kaniko"]
COPY ["pyproject.toml", "./"]

RUN --mount=type=secret,id=creds \
    poetry config http-basic.borisov $(head -1 ./kaniko/creds) $(tail -1 ./kaniko/creds) \
    && poetry config http-basic.team-name $(head -1 ./kaniko/creds) $(tail -1 ./kaniko/creds) \
    && poetry config virtualenvs.in-project true \
    && poetry install --only main

# 
# A switch between previous gitlab- and local- stages.
# Will be used in the COPY --from instriction of the app-image stage.
# 
FROM deps-image-${BUILD_ENVIRONMENT} as deps-image

# 
# An image containing our app.
# 
FROM runtime-image as app-image

ENV REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"
ENV VENV_PATH="./.venv"
ENV HOME_PATH="/home/artms-controller"
ENV PATH="${VENV_PATH}/bin:${PATH}"
ENV POSTGRES_DSN=""

WORKDIR ${HOME_PATH}

COPY ["src", "./src"]
COPY ["Dockerfile", "./"]
COPY --from=deps-image ["poetry.lock", "pyproject.toml", "./"]
COPY --from=deps-image ["${VENV_PATH}", "${VENV_PATH}"]

RUN groupadd -g 1000 artms-controller \
    && useradd -u 1000 -g artms-controller \
    -d ${HOME_PATH} -m -s /bin/bash artms-controller \
    && chown -R artms-controller:artms-controller ./

USER artms-controller

ENTRYPOINT ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
