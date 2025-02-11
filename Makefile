install: pyproject.toml
	pip install --upgrade pip &&\
	pip install --editable . 
	pip install .[test]

lint:
	pylint --disable=R,C src/app_calendar/*.py &&\
	pylint --disable=R,C tests/*.py

test:
	python -m pytest -vv --cov=app_calendar tests

format:
	black src/app_calendar/*.py &&\
	black tests/*.py

all: install lint format test 
