export POSTGRES_DSN=postgresql+asyncpg://artms:artms@0.0.0.0/artms
export PYTEST_COVER_PERCENT=80
export PYTHONDONTWRITEBYTECODE=1

up-db:
	podman-compose up -d

up-alembic: up-db
	poetry run alembic upgrade head

test-alembic: up-alembic
	poetry run alembic downgrade base

up: up-alembic
	poetry run uvicorn src.main:app --reload

down:
	podman-compose down --remove-orphans \
	                    --volumes

test-app:
	poetry run pytest --cov-fail-under=${PYTEST_COVER_PERCENT} \
	                  tests/unit/

cleanup:
	podman rm $(podman ps -aq)
	podman rmi $(podman image ls -q)

lint:
	yamllint .
