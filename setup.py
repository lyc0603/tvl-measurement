"""
Script to setup the repository for the first time.
"""

from setuptools import setup, find_packages

setup(
    name="environ",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "web3",
    ],
    extras_require={"dev": ["pylint", "black"]},
)
