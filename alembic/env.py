from logging.config import fileConfig
from alembic import context
from gpas_adb.model import Base
from gpas_adb.main import engine
from gpas_adb.main import test_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    ee = context.config.attributes.get("connection", None)
    
    if ee is None:
        test_db = context.get_x_argument(as_dictionary=True).get('testdb')
        if test_db:
            ee = test_engine
        else:
            ee = engine

    with ee.connect() as conn:
        context.configure(
            connection=conn, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
run_migrations_online()
