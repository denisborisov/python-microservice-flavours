.PHONY: all

export POSTGRES_DSN=postgresql+psycopg://artms:artms@/artms?host=0.0.0.0:5432&host=0.0.0.0:5432&target_session_attrs=read-write
export PYTEST_COVER_PERCENT=80
export PYTHONDONTWRITEBYTECODE=1

.PHONY: pre-commit
pre-commit:
    # Run pre-commit checks
	poetry run pre-commit autoupdate
	poetry run pre-commit run --all-files

.PHONY: test-app
test-app:
    # Run tests related to app
	poetry run pytest --cov-fail-under=${PYTEST_COVER_PERCENT} \
                      tests/

.PHONY: up-db
up-db:
    # Run a PostgreSQL container
	podman-compose up -d
	sleep 1

.PHONY: up-alembic
up-alembic: up-db
    # Run Alembic migrations
	poetry run alembic upgrade head

.PHONY: test-alembic
test-alembic: up-alembic
    # Run forward and downward Alembic migrations
	poetry run alembic downgrade base

.PHONY: test
test: pre-commit test-app test-alembic
    # Run tests related both to app and alembic migrations

.PHONY: up
up: up-alembic
    # Run app by first creating a database and running migrations
	poetry run uvicorn src.main:app --reload

.PHONY: down
down:
    # Remove a PostgreSQL container
	podman-compose down --remove-orphans \
                        --volumes

.PHONY: build-runtime-image
build-runtime-image:
    # Build runtime image.
	podman build --file docker/runtime.Dockerfile \
                 --tag runtime-image \
                 .

.PHONY: build-app-migration-image
build-app-migration-image: build-runtime-image
    # Build an image with Alembic migrations
	podman build --file docker/migration.Dockerfile \
                 --build-arg REVISION=head \
                 --build-arg ROLLBACK_REVISION=base \
                 --tag app-migration-image \
                 .

.PHONY: build-app-image
build-app-image: build-runtime-image
    # Build an image with app
	podman build --file docker/app.Dockerfile \
                 --tag app-image \
                 .

.PHONY: build-all
build-all: build-app-migration-image build-app-image
    # Build all images

.PHONY: run-app-migration-image
run-app-migration-image: up-db
    # Run a container with Alembic migrations
	podman run --env POSTGRES_DSN="${POSTGRES_DSN}" \
               --network host \
               app-migration-image \
               upgrade.sh

.PHONY: run-app-image
run-app-image:
    # Run a container with app
	chmod -R 777 ./reports
	podman run --env POSTGRES_DSN="${POSTGRES_DSN}" \
               --publish 8000:8000 \
               app-image

.PHONY: clean
clean: down
	podman rm $(podman ps -aq)
	podman rmi $(podman image ls -q)
