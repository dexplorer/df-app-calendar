install: requirements.txt 
	pip install --upgrade pip &&\
	pip install -r requirements.txt

setup: 
	python setup.py install

lint:
	pylint --disable=R,C *.py &&\
	pylint --disable=R,C app_calendar/*.py &&\
	pylint --disable=R,C app_calendar/tests/*.py

test:
	python -m pytest -vv --cov=app_calendar app_calendar/tests

format:
	black *.py &&\
	black app_calendar/*.py
	black app_calendar/tests/*.py

all: install setup lint format test 
