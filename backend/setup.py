from setuptools import setup

setup(
    name="mirrorscan",
    version="1.0.0",
    packages=["app"],
    package_dir={"": "."},
    install_requires=[
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        "sqlalchemy>=2.0.27",
        "pydantic>=2.7.0",
        "pydantic-settings>=2.9.1",
    ],
) 