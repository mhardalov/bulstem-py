from io import open

from setuptools import find_packages, setup

extras = {}
extras["testing"] = ["pytest", "nltk"]

setup(
    name="bulstem_py",
    version="0.3.0",
    author="Momchil Hardalov",
    author_email="momchil.hardalov@gmail.com",
    description="Python version of the BulStem implemented with Trie",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="BulStem Python",
    license="MIT",
    url="https://github.com/mhardalov/bulstem-py",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["regex", "pathlib"],
    extras_require=extras,
    entry_points={},
    include_package_data=True,
    package_data={"stemrules": ["resources/stemrules/*.txt"]},
    python_requires=">=3.6.0",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence :: Natural Language Processing",
    ],
)
