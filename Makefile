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
	black --extend-exclude .venv --extend-exclude alembic .

lint:
	flake8 main.py model.py tests/*.py
	
