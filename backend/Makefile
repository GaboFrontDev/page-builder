.PHONY: test run dev clean install

install:
	pip install -r requirements.txt

test:
	pytest test_main.py -v

test-generator:
	python run_tests.py

test-all:
	pytest -v

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term

run:
	uvicorn main:app --host 0.0.0.0 --port 3001

dev:
	uvicorn main:app --host 0.0.0.0 --port 3001 --reload

clean:
	rm -rf __pycache__ .pytest_cache htmlcov .coverage test.db

lint:
	flake8 . --exclude=venv,__pycache__

format:
	black . --exclude=venv