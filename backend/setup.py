# backend/setup.py
from setuptools import setup, find_packages

setup(
    name="uems",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'python-dotenv',
        'openpyxl'
    ]
)