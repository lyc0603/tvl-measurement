"""
Automatically set up the project for development.
"""

from setuptools import setup, find_packages

setup(
    name="environ",
    packages=find_packages(),
    install_requires=[
        "multicall",
        "python-dotenv",
        "pandas",
        "web3",
        "tqdm",
        "requests",
        "plotly",
        "randomcolor",
        "pycoingecko",
        "matplotlib",
        "bs4",
        "plotly",
        "Jinja2",
    ],
    extra_require={"dev": ["pylint", "black"]},
)
