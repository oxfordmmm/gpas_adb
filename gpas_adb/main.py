"""
Creates the engine object from environmental variables

Uses the new oracledb python package. Currently sqlAlchemy
does not support this package natively, hence work around
in the import statements.

Also includes a test_engine to be used when running the tests
"""

import sys
from sqlalchemy import create_engine
import oracledb
from decouple import config

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb

DB_USER = config("DB_USER", default="user")
DB_PASS = config("DB_PASS", default="pass")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default=1521)
DB_PROTOCOL = config("DB_PROTOCOL", default="tcps")
SERVICE_NAME = config("SERVICE_NAME", default="XEPDB1")
SSL_SERVER_CERT_DN = config("SSL_SERVER_CERT_DN", default="server_cert")
TEST_DB_USER = config("TEST_DB_USER", default="MY_USER")
TEST_DB_PASS = config("TEST_DB_PASS", default="change_this")
TEST_DB_HOST = config("TEST_DB_HOST", default="127.0.0.1")
TEST_DB_PORT = config("TEST_DB_PORT", default=1521)
TEST_SERVICE_NAME = config("TEST_SERVICE_NAME", default="XEPDB1")
TEST_DB_PROTOCOL = config("TEST_DB_PROTOCOL", default="tcps")


engine = create_engine(
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
