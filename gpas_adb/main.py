"""
Creates the engine object from environmental variables

Uses the new oracledb python package. Currently sqlAlchemy
does not support this package natively, hence work around
in the import statements.

Also includes a test_engine to be used when running the tests
"""

import sys
from sqlalchemy import create_engine, engine
import oracledb
from decouple import config as cfg
from alembic import config, script
from alembic.runtime import migration

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb

DB_USER = cfg("DB_USER", default="user")
DB_PASS = cfg("DB_PASS", default="pass")
DB_HOST = cfg("DB_HOST", default="localhost")
DB_PORT = cfg("DB_PORT", default=1521)
DB_PROTOCOL = cfg("DB_PROTOCOL", default="tcps")
SERVICE_NAME = cfg("SERVICE_NAME", default="XEPDB1")
SSL_SERVER_CERT_DN = cfg("SSL_SERVER_CERT_DN", default="server_cert")
TEST_DB_USER = cfg("TEST_DB_USER", default="MY_USER")
TEST_DB_PASS = cfg("TEST_DB_PASS", default="change_this")
TEST_DB_HOST = cfg("TEST_DB_HOST", default="127.0.0.1")
TEST_DB_PORT = cfg("TEST_DB_PORT", default=1521)
TEST_SERVICE_NAME = cfg("TEST_SERVICE_NAME", default="XEPDB1")
TEST_DB_PROTOCOL = cfg("TEST_DB_PROTOCOL", default="tcps")


live_engine = create_engine(
    f"oracle://{DB_USER}:{DB_PASS}@",
    connect_args={
        "host": DB_HOST,
        "port": DB_PORT,
        "protocol": DB_PROTOCOL,
        "retry_count": 20,
        "retry_delay": 3,
        "service_name": SERVICE_NAME,
        "ssl_server_cert_dn": SSL_SERVER_CERT_DN,
    },
)

test_engine = create_engine(
    (
        f"oracle://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}"
        f":{TEST_DB_PORT}/?service_name={TEST_SERVICE_NAME}"
    ),
    connect_args={
        "protocol": TEST_DB_PROTOCOL,
        "retry_count": 20,
        "retry_delay": 3,
    },
)


def check_current_head(connectable: engine.Engine) -> bool:
    alembic_cfg: config.Config = config.Config("alembic.ini")
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())
