import sys
import pytest
import oracledb
from gpas_adb import test_engine

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb


@pytest.fixture
def alembic_engine():
    return test_engine
