export POSTGRES_DSN=postgresql+psycopg://artms:artms@/artms?host=0.0.0.0:5432&host=0.0.0.0:5432&target_session_attrs=read-write
export PYTEST_COVER_PERCENT=80
export PYTHONDONTWRITEBYTECODE=1

lint-yaml:
    # Lint yaml files
	yamllint .

lint-all: lint-yaml
    # Lint all files

test-app: lint-all
    # Run tests related to app
	poetry run pytest --cov-fail-under=${PYTEST_COVER_PERCENT} \
                      tests/

up-db:
    # Run a PostgreSQL container
	podman-compose up -d
	sleep 1

up-alembic: up-db
    # Run Alembic migrations
	poetry run alembic upgrade head

test-alembic: up-alembic
    # Run forward and downward Alembic migrations
	poetry run alembic downgrade base

test-all: test-app test-alembic
    # Run tests related both to app and alembic migrations

up: up-alembic
    # Run app by first creating a database and running migrations
	poetry run uvicorn src.main:app --reload

down:
    # Remove a PostgreSQL container
	podman-compose down --remove-orphans \
                        --volumes

build-runtime-image:
    # Build runtime image.
	podman build --file docker/runtime.Dockerfile \
                 --tag runtime-image \
                 .

build-app-migration-image: build-runtime-image
    # Build an image with Alembic migrations
	podman build --file docker/migration.Dockerfile \
                 --build-arg REVISION=head \
                 --build-arg ROLLBACK_REVISION=base \
                 --tag app-migration-image \
                 .

build-app-image: build-runtime-image
    # Build an image with app
	podman build --file docker/app.Dockerfile \
                 --tag app-image \
                 .

build-all: build-app-migration-image build-app-image
    # Build all images

run-app-migration-image: up-db
    # Run a container with Alembic migrations
	podman run --env POSTGRES_DSN="${POSTGRES_DSN}" \
               --network host \
               app-migration-image \
               upgrade.sh

run-app-image:
    # Run a container with app
	chmod -R 777 ./reports
	podman run --env POSTGRES_DSN="${POSTGRES_DSN}" \
               --publish 8000:8000 \
               app-image

cleanup: down
	podman rm $(podman ps -aq)
	podman rmi $(podman image ls -q)
