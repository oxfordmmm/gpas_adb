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

DB_USER = config("DB_USER", default='user')
DB_PASS = config("DB_PASS", default='pass')
DB_HOST = config("DB_HOST", default='localhost')
DB_PORT = config("DB_PORT", default='1521')
DB_PROTOCOL = config("DB_PROTOCOL", default='tcps')
SERVICE_NAME = config("SERVICE_NAME", default='XEPDB1')
SSL_SERVER_CERT_DN = config("SSL_SERVICE_CERT_DN", default="server_cert")

engine = create_engine(
    f'oracle://{DB_USER}:{DB_PASS}@',
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
    "oracle://MY_USER:change_this@127.0.0.1:1521/?service_name=XEPDB1",
    connect_args={
        "protocol": "tcps",
        "retry_count": 20,
        "retry_delay": 3,
    },
)
