from setuptools import setup

setup(
    name="gpas_adb",
    description="The autonomous database for the SP3 part of GPAS",
    url="https://github.com/oxfordmmm/gpas_adb",
    author="Marc Brouard",
    license="MIT",
    packages=["gpas_adb"],
    install_requires=[
        "sqlalchemy",
        "oracledb",
        "sqlalchemy-jdbcapi",
        "sqlalchemy-views",
        "python-decouple",
    ],
    zip_safe=False,
)
