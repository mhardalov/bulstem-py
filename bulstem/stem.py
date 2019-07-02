# coding: utf8

"""
BULSTEM: INFLECTIONAL STEMMER FOR BULGARIAN

This is the BulStem stemming algorithm. It follows the algorithm presented in

Nakov, P. BulStem: Design and evaluation of inflectional stemmer for Bulgarian. In Workshop on Balkan Language Resources
and Tools (Balkan Conference in Informatics).

Preslav Nakov, the algorithm's inventor, maintains a web page about the algorithm at

    http://people.ischool.berkeley.edu/~nakov/bulstem/

which includes original Perl implementation, also a Java, and another Python version.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import re
from nltk.compat import python_2_unicode_compatible
from nltk.stem.api import StemmerI


@python_2_unicode_compatible
class BulStemmer(StemmerI):
    """
    A stemmer base on Nakov, P. BulStem: Design and evaluation of inflectional stemmer for Bulgarian.
    In Workshop on Balkan Language Resources and Tools (Balkan Conference in Informatics).

    See http://people.ischool.berkeley.edu/~nakov/bulstem/ for the homepage of the algorithm.
    """

    RULES_PATTERN = re.compile(r"([а-я]+)\s+==>\s+([а-я]+)\s+([0-9]+)", re.IGNORECASE)
    VOWELS = {'а', 'ъ', 'о', 'у', 'е', 'и', 'я', 'ю'}

    class TrieNode:
        def __init__(self):
            """
            Constructs TrieNode.
            """
            self.stem = ""
            self.chars = {}

        def is_stem(self):
            return len(self.stem)

    class SuffixTrie:
        def __init__(self, allow_duplicates=False):
            """
            Constructs SuffixTrie.

            :param allow_duplicates: (Optional) bool, if false it raises ValueError exception when duplicates are found.
            """
            self._root = BulStemmer.TrieNode()
            self._allow_duplicates = allow_duplicates

        def add(self, word, stem):
            """
            Adds a single word with it's stem to the SuffixTrie.

            :param word: string, original word, before stemming.
            :param stem: string, corresponding stem.

            :raises ValueError: if duplicates are found in the fields.
            """
            curr = self._root
            for c in reversed(word.lower()):
                if c not in curr.chars:
                    curr.chars[c] = BulStemmer.TrieNode()
                curr = curr.chars[c]

            if not self._allow_duplicates and curr.is_stem():
                raise ValueError("Duplicate key '{0}' found".format(stem))

            curr.stem = stem

        def get(self, word, vowel_idx):
            """
            Finds the longest possible rule from the end of the word, and appends it to the non-stemmed prefix.

            :param word: string, original word, before stemming.
            :param vowel_idx: int, position of the first vowel.

            :return: string, lower-cased and stemmed version of the word.
            """
            word = word.lower()
            stem = ""
            idx = len(word)
            curr = self._root

            for i, c in enumerate(reversed(word)):
                i = len(word) - i - 1
                if c not in curr.chars or i < vowel_idx:
                    break

                curr = curr.chars[c]

                if curr.is_stem():
                    stem = curr.stem
                    idx = i

            return word[:idx] + stem

    def __init__(self, rules, min_freq=2, left_context=3, allow_duplicates=False):
        """
        Constructs BulStemmer.

        :param rules: Iterable[string], a collection of strings formatted, as follows: word ==> stem freq.
        :param min_freq: (Optional) int, the minimum frequency of a rule to be used when stemming.
        :param left_context: (Optional) int, size of the prefix which will not be stemmed.
        :param allow_duplicates: (Optional) bool, if false it raises ValueError exception when duplicates are found.

        :raises ValueError: if duplicates are found in the fields.
        """
        self._min_freq = min_freq
        self._left_context = left_context
        self._stem_rules = self._read_rules(rules, allow_duplicates)

    @classmethod
    def from_file(cls, path, encoding="utf-8", min_freq=2, left_context=3, allow_duplicates=False):
        """
        Constructs BulStemmer from file.

        :param path: string, path to the rules file formatted: word ==> stem freq.
        :param encoding: (Optional) string, encoding of the rules file
        :param min_freq: (Optional) int, the minimum frequency of a rule to be used when stemming.
        :param left_context: (Optional) int, size of the prefix which will not be stemmed.
        :param allow_duplicates: (Optional) bool, if false it raises ValueError exception when duplicates are found.

        :returns BulStemmer, an instance of BulStemmer.
        :raises ValueError: if duplicates are found in the fields.
        """
        with open(path, 'r', encoding=encoding) as rules:
            stemmer = cls(rules, min_freq, left_context, allow_duplicates)

        return stemmer

    def _read_rules(self, rules, allow_duplicates=False):
        """
        Fills the Trie with the corresponding rules

        :param rules: Iterable[string], a collection of strings formatted, as follows: word ==> stem freq.
        :param allow_duplicates: (Optional) bool, if false it raises ValueError exception when duplicates are found.

        :return: SuffixTrie, Trie filled with stemming rules.
        :raises ValueError: if duplicates are found in the fields.
        """
        stem_rules = BulStemmer.SuffixTrie(allow_duplicates)
        for line in rules:
            m = BulStemmer.RULES_PATTERN.match(line.strip())
            if not m or len(m.groups()) != 3:
                continue

            (word, stem, freq) = m.groups()
            if int(freq) >= self._min_freq:
                stem_rules.add(word, stem)

        return stem_rules

    @staticmethod
    def pos_first_vowel(token):
        """
        Finds the position of the first vowel in a token.

        :param token: string, a lower-cased word.

        :return: string, position of the first vowel, if found, else one position after the last index.
        """
        i = 0
        while i < len(token) and token[i] not in BulStemmer.VOWELS:
            i += 1

        return i

    def stem(self, token):
        """
        The stemming is performed by applying the longest possible rule (if any), provided that the stem produced
        contains at least one vowel.

        :param token: string, token to be stemmed.

        :return: string, stem of the word.
        """
        stem = token.lower()
        if len(stem) > self._left_context:
            # There must be at least one vowel in the resultant stem, hence we stem everything after the first one.
            i = BulStemmer.pos_first_vowel(stem) + 1
            stem = self._stem_rules.get(stem, i)

        return stem

stemmer = BulStemmer(["ой ==> о 10"], min_freq=0, left_context=0)
stemmer.stem('тоой')