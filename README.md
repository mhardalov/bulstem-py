# BulStem-py: A Python Re-implementation of BulStem - inflectional stemmer for Bulgarian

[![CircleCI](https://circleci.com/gh/mhardalov/bulstem-py.svg?style=svg&circle-token=85a1632948c16a50675753abedcd43cc4a64b23d)](https://circleci.com/gh/mhardalov/bulstem-py)

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

## Usage

```python
from bulstem.stem import BulStemmer

stemmer = BulStemmer('stem_rules_context_2_utf8.txt', min_freq=2, left_context=3)
stemmer.stem('вероятен') # Excepted output: 'вероят'
```

`BulStemmer` constructor params:
1. `path` - Path to the rules file formatted: word ==> stem ==> freq.
2. `min_freq` - The minimum frequency of a rule to be used when stemming.
3. `left_context` - Size of the prefix which will not be stemmed.


## Other implementations

[Perl (Original)](http://people.ischool.berkeley.edu/~nakov/bulstem/apply_stem.pl),
[Java (JDK 1.4)](http://people.ischool.berkeley.edu/~nakov/bulstem/Stemmer.java),
[Ruby](https://github.com/tbmihailov/bulstem),
[C#](https://github.com/tbmihailov/bulstem-cs),
[Python2](https://github.com/peio/PyBulStem),
[GATE plugin (Java)](https://gate.ac.uk/gate/plugins/Lang_Bulgarian/src/gate/bulstem/BulStemPR.java)
