# Environment
export PYTHON=python3
export VENV=.venv
export PIP=$(VENV)/bin/pip
export UVICORN=$(VENV)/bin/uvicorn

# Commands
.PHONY: install run lint format test clean reset

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(UVICORN) main:app --reload

lint:
	$(VENV)/bin/ruff . --ignore E501

format:
	$(VENV)/bin/black .

test:
	$(PYTHON) test_upload.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache

reset: clean
	rm -rf $(VENV)
