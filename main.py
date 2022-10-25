"""
Creates the engine object from environmental variables

Uses the new oracledb python package. Currently sqlAlchemy
does not support this package natively, hence work around
in the import statements.

Also includes a test_engine to be used when running the tests
"""

import sys
from sqlalchemy import create_engine
from dotenv import dotenv_values
import oracledb

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb

config = dotenv_values(".env")


engine = create_engine(
    f'oracle://{config["DB_USER"]}:{config["DB_PASS"]}@',
    connect_args={
        "host": config["DB_HOST"],
        "port": config["DB_PORT"],
        "protocol": config["DB_PROTOCOL"],
        "retry_count": 20,
        "retry_delay": 3,
        "service_name": config["SERVICE_NAME"],
        "ssl_server_cert_dn": config["SSL_SERVER_CERT_DN"],
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
