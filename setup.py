from io import open
from setuptools import find_packages, setup

setup(
    name="bulstem_py",
    version="0.2.0",
    author="Momchil Hardalov",
    author_email="momchil.hardalov@gmail.com",
    description="Python version of the BulStem implemented with Trie",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords='BulStem Python',
    license='MIT',
    url="https://github.com/mhardalov/bulstem-py",
    packages=find_packages(exclude=["*.tests", "*.tests.*",
                                    "tests.*", "tests"]),
    install_requires=['nltk', 'importlib_resources'],
    entry_points={

    },
    include_package_data=True,    # include everything in source control
    # python_requires='>=3.5.0',
    tests_require=['nltk', 'importlib_resources'],
    classifiers=[
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Artificial Intelligence :: Natural Language Processing',
    ],
)
