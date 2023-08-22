# This Dockerfile contains four stages:
# - deps-image-gitlab
# - deps-image-local
# - deps-image
# - app-image
# 
# The purpose of the `app-migration-image` stage is to create the final image containing our app.
# This stage is the one that should be built by kaniko on the `build-app-migration-image` step,
# and it is defined in `.gitlab-ci.yml` file via `--target app-migration-image` flag.
# 
# Both `deps-image-gitlab` and `deps-image-local` stages are destined to load and install all necessary dependencies -
# poetry dependencies in our case. We read Artifactory credentials from `kaniko/creds` file.
# This file has the following structure:
# 
# username
# password
# 
# And the main difference between `deps-image-gitlab` and `deps-image-local` is in the location of this file.
# If we want to run this Dockerfile locally, we should create this `kaniko/creds` file, placing `kaniko` folder
# at the same level as this Dockerfile.
# 
# The purpose of the `deps-image` stage as long as the `BUILD_ENVIRONMENT` argument variable
# is to switch between `deps-image-gitlab` and `deps-image-local` stages while running the `app-migration-image` stage,
# particularly the `COPY --from` instruction.
# 
# So in order to run this Docker file locally, we should change the `BUILD_ENVIRONMENT` argument variable to "local".
# You can also see that this argument variable is set to 'gitlab' on the `build-app-migration-image` step
# in `.gitlab-ci.yml`: `--build-arg BUILD_ENVIRONMENT=gitlab`, because there we want to use `deps-image-gitlab`
# inside the `COPY --from` instruction of the `app-migration-image` stage.
# 
ARG BUILD_ENVIRONMENT="local"
ARG REVISION=
ARG ROLLBACK_REVISION=

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
COPY ["poetry.lock", "pyproject.toml", "./"]

RUN --mount=type=secret,id=creds \
    poetry config http-basic.borisov $(head -1 ./kaniko/creds) $(tail -1 ./kaniko/creds) \
    && poetry config http-basic.team-name $(head -1 ./kaniko/creds) $(tail -1 ./kaniko/creds) \
    && poetry config virtualenvs.in-project true \
    && poetry install --only main

# 
# A switch between previous gitlab- and local- stages.
# Will be used in the `COPY --from` instriction of the `app-migration-image` stage.
# 
FROM deps-image-${BUILD_ENVIRONMENT} as deps-image

# 
# An image containing our app.
# 
FROM runtime-image as app-migration-image

ARG REVISION
ARG ROLLBACK_REVISION

ENV VENV_PATH="./.venv"
ENV HOME_PATH="/home/artms-controller"
ENV PATH="${VENV_PATH}/bin:${PATH}"
ENV POSTGRES_DSN=""

WORKDIR ${HOME_PATH}

COPY ["alembic", "./alembic"]
COPY ["alembic.ini", "docker/runtime.Dockerfile", "docker/migration.Dockerfile", "./"]
COPY --from=deps-image ["poetry.lock", "pyproject.toml", "./"]
COPY --from=deps-image ["${VENV_PATH}", "${VENV_PATH}"]

RUN groupadd -g 1000 artms-controller \
    && useradd -u 1000 -g artms-controller \
    -d ${HOME_PATH} -m -s /bin/bash artms-controller \
    && chown -R artms-controller:artms-controller ./

RUN echo "python -m alembic upgrade ${REVISION}" > upgrade.sh \
    && echo "python -m alembic downgrade ${ROLLBACK_REVISION}" > rollback.sh \
    && chmod +x upgrade.sh && chmod +x rollback.sh

USER artms-controller

ENTRYPOINT ["/bin/bash"]
