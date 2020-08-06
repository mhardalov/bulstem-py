from io import open

from setuptools import find_packages, setup

extras = {}
extras["testing"] = ["pytest", "nltk"]

setup(
    name="bulstem",
    version="0.3.3",
    author="Momchil Hardalov",
    author_email="momchil.hardalov@gmail.com",
    description="Python version of the BulStem stemming algorithm",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="NLP stemmer Bulgarian bulstem",
    license="Apache License, Version 2.0",
    url="https://github.com/mhardalov/bulstem-py",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[],
    extras_require=extras,
    entry_points={},
    include_package_data=True,
    package_data={"bulstem": ["stemrules/*.txt"]},
    python_requires=">=3.6.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
)
