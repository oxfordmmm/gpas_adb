[![GPAS Autonomous Database Models](https://github.com/oxfordmmm/gpas_adb/actions/workflows/db_tests.yml/badge.svg)](https://github.com/oxfordmmm/gpas_adb/actions/workflows/db_tests.yml)

# GPAS Autonomous Database

## Setup Dev machine

- Clone the repo to your local machine.

- If you are using an Autonomous database then you will need to set some environmental variables, the easiest way to do this if using an virtual environment, is to use a `.env` file. A template is provided in the repo, just copy `env_template` to `.env`. Git should ignore the `.env` file, but make sure it is not copied to the GitHub repo.

- Set up a new virtual environment using either `venv` python or `pipenv`

  - With `venv`, `cd` into the project directory and run the following

  ```
  python3 -m venv .venv
  source .venv/bin/activate
  make install_dev
  ```

  Use `deactivate` to exit virtual environment

  - With `pipenv`, `cd` into the project directory and run the following

  ```
  mkdir .venv
  pipenv install --python 3.8 -r requirements_dev.txt
  pipenv shell
  ```

  Use `exit` to exit virtual environment

## Setup test database using docker and Oracle XE

For testing a docker container of Oracle XE is used. If using a M1 Mac you will
need to install colima ([instructions](https://github.com/abiosoft/colima#installation)) and run the following command. 

```
colima start --arch x86_64 --memory 4
```

This will allow you to run x86 64 applications on M1 Macs using docker. As
Oracle XE does not support (yet) arm64 this is required.

Use the following command to run Oracle XE in docker

```
docker run -d -p 1521:1521 -e ORACLE_RANDOM_PASSWORD=true, -e APP_USER=MY_USER -e APP_USER_PASSWORD=change_this gvenzl/oracle-xe:latest-faststart
```

Check the status of the docker container with `docker container ls`. Once
running issue the following command to upgrade the database to the latest
version.

```
alembic -x testdb=true upgrade head
```

The `Makefile` includes the docker setup commands for both x86_64 and M1

## Running the tests

Issue the following command to run the tests.

```
pytest
```

This will run the four built-in tests from `ptest-alembic`.

The following is taken from `pytest-alembic`, and repeated here for convenience 

### test_single_head_revision

Assert that there only exists one head revision.

### test_upgrade

Assert that the revision history can be run through from base to head.

### test_model_definitions_match_ddl

Assert that the state of the migrations matches the state of the models describing the DDL.

### test_up_down_consistency

Assert that all downgrades succeed.

## Makefile

The following operations are include in a `Makefile` and can be run using the
`make` command followed by operation name

### install

Installs the dependencies using `pip`

### install_dev

Installs the dependencies and additional tools for development and testing using
`pip`

### test

Makes sure the test database (Oracle XE) is updated to the latest version and
then runs the tests.

### format

Calls the `black` command to format the code to PEP8 standards. Ignores the
`.venv` and `alembic` directories.

### lint

Calls the `pylint` to check the syntax of the Python code. Ignores the `.venv`
and `alembic` directories

### setup_docker

Runs the Oxford XE container in docker

### setup_docker_mac_m1

Uses Colima to run x86_64 containers and runs the Oxford XE container in docker

### teardown_setup

Stops the docker container running Oracle XE

### teardown_setup_mac_m1

Stops the docker container running Oracle XE and stops Colima

## Generating migrations

Run the following command to generate the migration file.

```
alembic revision --autogenerate -m "<description of change>"
```

If you are using the test database to develop against, and you probably should, then use the following command to generate migrations for any changes that you make.

```
alembic -x testdb=true revision --autogenerate -m "<description of change>"
```

Replace `<description of change>` with something descriptive.

**IMPORTANT** Always manually check the generated migrations file. Not all
operations can be auto-generated, so you may need to manually modify the
migrations file.

### Applying migrations

To apply the migrations to the test database, run the following

```
alembic -x testdb=true upgrade head
```

And to run the migrations against the Live Autonomous Database, run the following

```
alembic upgrade head
```
