from setuptools import find_packages, setup

setup(
    name="index_builder",
    version="0.1.0",
    packages=find_packages(),
    author="Tamaki Nishino, Yuki Igarashi",
    author_email="otamachan@gmail.com, me@bonprosoft.com",
    license="Apache License 2.0",
    url="https://github.com/rospypi/index_builder",
    install_requires=[
        "click",
        "GitPython>=3.1.0,<4.0.0",
    ],
    extras_require={
        "lint": [
            "black==20.8b1",
            "flake8-bugbear==21.4.3",
            "flake8==3.9.1",
            "isort==5.1.4",
            "mypy==0.790",
            "pysen>=0.9,<0.10",
        ],
    },
)
