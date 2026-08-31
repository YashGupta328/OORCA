.PHONY: help install up down api worker test lint format clean

help:
	@echo "OORCA — make targets"
	@echo "  install    Install Python dependencies"
	@echo "  up         Bring up docker-compose stack"
	@echo "  down       Tear down docker-compose stack"
	@echo "  api        Run the FastAPI backend"
	@echo "  worker     Run a Celery worker"
	@echo "  test       Run pytest"
	@echo "  lint       Run ruff"
	@echo "  format     Run black"
	@echo "  clean      Remove build artifacts"

install:
	pip install -e ".[dev]"

up:
	docker compose up -d

down:
	docker compose down

api:
	uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

worker:
	celery -A backend.workers.celery_app worker --loglevel=INFO

test:
	pytest

lint:
	ruff check .

format:
	black .

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache .mypy_cache