import sys
import pytest
import oracledb
from gpas_adb.main import test_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection, Transaction

oracledb.version = "19.0.0"
sys.modules["cx_Oracle"] = oracledb


@pytest.fixture
def alembic_engine():
    return test_engine


@pytest.fixture()
def dbsession(alembic_engine):
    con: Connection = alembic_engine.connect()
    trans: Transaction = con.begin()
    session: Session = Session(bind=con)

    yield session

    session.close()
    trans.rollback()
    con.close()
