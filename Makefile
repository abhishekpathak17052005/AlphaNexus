.PHONY: help install run-backend run-frontend run test lint clean

help:
	@echo "ALPHANEXUS Development Commands:"
	@echo "  make install        Install all project dependencies"
	@echo "  make run-backend    Start FastAPI backend server on port 8000"
	@echo "  make run-frontend   Start Streamlit frontend on port 8501"
	@echo "  make test           Run all pytest test suites"
	@echo "  make lint           Check code quality using ruff"
	@echo "  make clean          Clean pycache and build artifacts"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run-backend:
	uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

run-frontend:
	streamlit run frontend/streamlit_app.py --server.port 8501

test:
	pytest -v tests/

lint:
	ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
