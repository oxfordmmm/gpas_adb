import sys
import pytest
from sqlalchemy import create_engine
import oracledb

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb

ee = create_engine(
    "oracle://MY_USER:change_this@127.0.0.1:1521/?service_name=XEPDB1",
    connect_args={
        "protocol": "tcps",
        "retry_count": 20,
        "retry_delay": 3,
    },
)


@pytest.fixture
def alembic_engine():
    return ee
