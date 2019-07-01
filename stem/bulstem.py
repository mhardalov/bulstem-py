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
            self.stem = ""
            self.chars = {}

        def is_stem(self):
            return len(self.stem)

    class SuffixTrie:
        def __init__(self):
            self._root = BulStemmer.TrieNode()

        def add(self, word, stem):
            """
            Adds a single word with it's stem to the SuffixTrie
            :param word: string, original word, before stemming
            :param stem: string, corresponding stem
            """
            curr = self._root
            for c in reversed(word.lower()):
                if c not in curr.chars:
                    curr.chars[c] = BulStemmer.TrieNode()
                curr = curr.chars[c]

            curr.stem = stem

        def get(self, word, vowel_idx):
            """
            Finds the longest possible rule from the end of the word, and appends it to the non-stemmed prefix.
            :param word: string, original word, before stemming
            :param vowel_idx: int, position of the first vowel
            :return: string, lower-cased and stemmed version of the word
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

    def __init__(self, path, encoding="utf-8", min_freq=2, left_context=3):
        self._min_freq = min_freq
        self._left_context = left_context
        self._stem_rules = self._read_rules(path, encoding=encoding)

    def _read_rules(self, path, encoding="utf-8"):
        """
        Fills the Trie with the corresponding rules in the format:
        word ==> stem ==> freq
        :param path: string, path to the rules file
        :param encoding: (Optional) string, encoding of the rules file
        :return: SuffixTrie, Trie filled with stemming rules
        """
        stem_rules = BulStemmer.SuffixTrie()

        with open(path, 'r', encoding=encoding) as rules:
            for line in rules:
                m = BulStemmer.RULES_PATTERN.match(line.strip())
                if not m or len(m.groups()) != 3:
                    continue

                (word, stem, freq) = m.groups()
                if int(freq) >= self._min_freq:
                    stem_rules.add(word, stem)

        return stem_rules

    @staticmethod
    def pos_first_vowel(stem):
        i = 0
        while i < len(stem) and stem[i] not in BulStemmer.VOWELS:
            i += 1

        return i

    def stem(self, token):
        """
        The stemming is performed by applying the longest possible rule (if any), provided that the stem produced
        contains at least one vowel.
        :param token: string, token to be stemmed
        :return: string, stem of the word
        """
        stem = token.lower()
        if len(stem) > self._left_context:
            # There must be at least one vowel in the resultant stem, hence we stem everything after the first one
            i = BulStemmer.pos_first_vowel(stem) + 1
            stem = self._stem_rules.get(stem, i)

        return stem
