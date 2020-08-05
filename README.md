# BulStem-py: A Python Re-implementation of BulStem - inflectional stemmer for Bulgarian

[![Build](https://img.shields.io/circleci/build/github/mhardalov/bulstem-py/master)](https://circleci.com/gh/mhardalov/bulstem-py)
[![PyPI](https://img.shields.io/pypi/v/bulstem.svg)](https://pypi.python.org/pypi/bulstem) 
[![License](https://img.shields.io/github/license/mhardalov/bulstem-py.svg?color=blue)](https://github.com/mhardalov//bulstem-py/blob/master/LICENSE)


## Introduction
This is the Python version of the BulStem stemming algorithm. It follows the algorithm presented in

```
Nakov, P. BulStem: Design and evaluation of inflectional stemmer for Bulgarian. In Workshop on 
Balkan Language Resources and Tools (Balkan Conference in Informatics).
```

See http://people.ischool.berkeley.edu/~nakov/bulstem/ for the homepage of the algorithm. Also, check the original [paper](http://people.ischool.berkeley.edu/~nakov/bulstem/BulStem.pdf) for more details and examples.

## Implementation

This implementation, in contrast of other available, uses a Trie, instead of Dictionary/Hashtable/, to find the longest possible rule, which can be applied to a certain token.
The Stemmer class is derived from NLTK's `StemmerI` interface, making it fully compatible with its pipelines. 

Basic algorithm steps:
1. Find the position of the first vowel in the token.
2. Finds the longest possible rule traversing the string in reverse order until there is a matching suffix, or the position of the first vowel found in Step. 1.
3. Prepend the non-stemmed prefix to the stemmed suffix (Step. 2).

## Installation

This library is compatible Python >= 3.6.

Clone the repository and run:

### With pip

```bash
pip install -e .
pip install -r requirements.txt
```

### Test

A set of tests are included in the project, under the [tests folder](https://github.com/mhardalov/bulstem-py/tree/master/tests).
The test suit can be run as follows:
 

```bash
pip install -e ".[testing]"
pip install -r requirements-test.txt
python -m unittest
```

## Usage

The library needs a set of rules to apply stemming properly. The rules can be either a list to the `BulStemmer` constructor, or a path to a file containing them.

For both options the rules need to be formatted as follows:

`word ==> stem ==> freq`

Pre-defined set of rules is included in the distribution, and can be used directly by the user, and can be found [here](https://github.com/mhardalov/bulstem-py/tree/master/bulstem/stemrules). (examples: [Reading the rules from an external file](#reading-the-rules-from-an-external-file))

### Manually loading rules

```python
from bulstem.stem import BulStemmer

stemmer = BulStemmer(["ой ==> о 10"], min_freq=0, left_context=2)
stemmer.stem('порой')# Excepted output: 1. 'поро'
```

`BulStemmer` constructor params:
1. `rules` - Iterable of strings containing rules.
2. `min_freq` - The minimum frequency of a rule to be used when stemming.
3. `left_context` - Size of the prefix which will not be stemmed.

### Reading the rules from an external file

```python
from bulstem.stem import BulStemmer


# Pre-defined names of rule sets
PRE_DEFINED_RULES = ['stem-context-1', 
                     'stem-context-2',
                     'stem-context-3']
                     
# Excepted output:
# 1 втор
# 2 втори
# 3 вторият
for i, rules_name in enumerate(PRE_DEFINED_RULES, start=1):
    stemmer = BulStemmer.from_file(rules_name, min_freq=2, left_context=i)
    print(i, stemmer.stem('вторият'))

stemmer = BulStemmer.from_file('stem_rules_context_2_utf8.txt', min_freq=2, left_context=i)
stemmer.stem('вторият') # Excepted output: 1. 'втори'
stemmer.stem('вероятен') # Excepted output: 1. 'вероят'
```

`BulStemmer.from_file` params:
1. `path` - Path (or pre-defined name) to the rules file formatted, as follows: word ==> stem ==> freq.
2. `min_freq` - The minimum frequency of a rule to be used when stemming.
3. `left_context` - Size of the prefix which will not be stemmed.


## Other implementations

[Perl (Original)](http://people.ischool.berkeley.edu/~nakov/bulstem/apply_stem.pl),
[Java (JDK 1.4)](http://people.ischool.berkeley.edu/~nakov/bulstem/Stemmer.java),
[Ruby](https://github.com/tbmihailov/bulstem),
[C#](https://github.com/tbmihailov/bulstem-cs),
[Python2](https://github.com/peio/PyBulStem),
[GATE plugin (Java)](https://gate.ac.uk/gate/plugins/Lang_Bulgarian/src/gate/bulstem/BulStemPR.java)

## License

For license information, see [LICENSE](https://github.com/mhardalov/bulstem-py/blob/master/LICENSE).
