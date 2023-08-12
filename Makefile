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

up-alembic: up-db
    # Run Alembic migrations
	poetry run alembic upgrade head

test-alembic: up-alembic
    # Run forward and downward Alembic migrations
	poetry run alembic downgrade base

test-all: test-app test-alembic
    # Run tests related both to app and alembic migrations

up: up-alembic
    # Run app by first creating a database and runnign migrations
	poetry run uvicorn src.main:app --reload

down:
    # Remove a PostgreSQL container
	podman-compose down --remove-orphans \
	                    --volumes

cleanup:
	podman rm $(podman ps -aq)
	podman rmi $(podman image ls -q)
