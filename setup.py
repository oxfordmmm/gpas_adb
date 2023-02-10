from setuptools import setup

setup(
    name="gpas_adb",
    description="The autonomous database for the SP3 part of GPAS",
    url="https://github.com/oxfordmmm/gpas_adb",
    author="Marc Brouard",
    license="MIT",
    packages=["gpas_adb"],
    install_requires=[
        "sqlalchemy<2.0",
        "oracledb",
        "sqlalchemy-jdbcapi",
        "sqlalchemy-views",
        "python-decouple",
        "alembic",
    ],
    zip_safe=False,
)
