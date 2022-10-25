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
	black *.py

lint:
	pylint --disable=R,C main.py model.py
