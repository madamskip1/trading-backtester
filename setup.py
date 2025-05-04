from setuptools import setup

setup(
    name="trading-backtester",
    version="0.2.0",
    description="A trading backtesting framework for Python",
    author="Adamski Maciej",
    author_email="madamskip1@gmail.com",
    packages=["trading_backtester"],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.16.0",
    ],
)
