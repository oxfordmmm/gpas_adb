install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install_dev:
	pip install --upgrade pip &&\
		pip install -r requirements_dev.txt

setup:
	if ! command -v docker &> /dev/null; \
	then\
			echo "Docker could not be found";\
			exit;\
	fi
	docker run -d --name oracle_xe \
		-p 1521:1521 \
		-e ORACLE_RANDOM_PASSWORD=true, \
		-e APP_USER=MY_USER \
		-e APP_USER_PASSWORD=change_this \
		gvenzl/oracle-xe:latest-faststart
	docker container ls

teardown_setup:
	if ! command -v docker &> /dev/null; \
	then\
			echo "Docker could not be found";\
			exit;\
	fi
	docker stop oracle_xe

setup_mac_m1:
	if ! command -v colima &> /dev/null; \
	then\
			echo "Colima could not be found";\
			exit;\
	fi
	if ! command -v docker &> /dev/null; \
	then\
			echo "Docker could not be found";\
			exit;\
	fi
	colima start --arch x86_64 --memory 4
	docker run -d --name oracle_xe \
		-p 1521:1521 \
		-e ORACLE_RANDOM_PASSWORD=true, \
		-e APP_USER=MY_USER \
		-e APP_USER_PASSWORD=change_this \
		gvenzl/oracle-xe:latest-faststart
	docker container ls

teardown_setup_mac_m1:
	if ! command -v colima &> /dev/null; \
	then\
			echo "Colima could not be found";\
			exit;\
	fi
	if ! command -v docker &> /dev/null; \
	then\
			echo "Docker could not be found";\
			exit;\
	fi
	docker stop oracle_xe
	colima stop

test:
	alembic -x testdb=true upgrade head
	python -m pytest -vv gpas_adb

format:
	black --extend-exclude .venv --extend-exclude alembic .

lint:
	flake8 gpas_adb/*.py gpas_adb/tests/*.py

