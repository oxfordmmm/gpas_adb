import sys
import oracledb
oracledb.version = "8.3.0"
sys.modules["cx_Oracle"] = oracledb
import cx_Oracle

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from dotenv import dotenv_values

config = dotenv_values(".env")

engine = create_engine(f'oracle://{config["DB_USER"]}:{config["DB_PASS"]}@',
           connect_args={
               "host": config["DB_HOST"],
               "port": config["DB_PORT"],
               "protocol": config["DB_PROTOCOL"],
               "retry_count": 20,
               "retry_delay": 3,
               "service_name": config["SERVICE_NAME"],
               "ssl_server_cert_dn": config["SSL_SERVER_CERT_DN"]
           }
     )
