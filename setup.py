from setuptools import setup

setup(
    name="trading-backtester",
    version="1.0.0a1",
    description="A trading backtesting framework for Python",
    author="Adamski Maciej",
    author_email="madamskip1@gmail.com",
    packages=["trading_backtester"],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.16.0",
        "matplotlib>=3.0.0",
    ],
)
