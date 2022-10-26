install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install_dev:
	pip install --upgrade pip &&\
		pip install -r requirements_dev.txt

test:
	alembic -x testdb=true upgrade head
	python -m pytest -vv

format:
	find . -not \( -path ./.venv -prune \) -type f -name "*.py" -exec black {} \;

lint:
	find . -not \( -path ./.venv -prune \) -type f -name "*.py" -exec pylint --disable=R,C {} \;
