export PYTHONDONTWRITEBYTECODE=1
export DB_HOST=localhost
export DB_USER=postgres
export DB_NAME=articles
export DB_PASSWORD=password

up:
	chmod 777 database
	podman-compose up -d
	poetry run uvicorn src.main:app
down:
	podman-compose down --volumes
test:
	poetry run pytest
