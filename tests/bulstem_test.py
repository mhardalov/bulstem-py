# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import nltk
import unittest

from bulstem.stem import BulStemmer


class BulStemmerTest(unittest.TestCase):
    RULES_1_PATH = './rules/stem_rules_context_1_utf8.txt'
    RULES_2_PATH = './rules/stem_rules_context_2_utf8.txt'
    RULES_3_PATH = './rules/stem_rules_context_3_utf8.txt'

    def setUp(self):
        nltk.download('punkt')

    def test_full_stem(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_2_PATH, min_freq=2, left_context=2)
        text = \
            '''
            Има първи вероятен случай на атипична пневмония в България, съобщи министърът на здравеопазването Божидар 
            Финков. Става дума за 33-годишен пациент, който на 16 април е пристигнал в България след продължителен 
            престой в Торонто, Канада, където вече са регистрирани 19 смъртни случая вследствие на тежкия остър 
            респираторен синдром (ТОРС). Точната диагнозата обаче не може да бъде установена в България и пробите ще 
            бъдат изпратени за изследване Световната здравна организация (СЗО).
            '''

        stemmed = \
            '''
            има първ вероят случа на атипич пневмони в българ, съобщ минист на здравеопазван божидар финков. 
            става дума за 33-годиш пациент, койт на 16 апр е пристигн в българ след продължител престо в торонт, канад, 
            къде вече са регистрира 19 смърт случа вследстви на тежк ост респиратор синдром (торс). 
            точн диагноз обач не може да бъде установ в българ и проби ще бъда изпрат за изследван светов здравн
            организаци (сзо).
            '''

        for (token, stem) in zip(nltk.word_tokenize(text.strip()),
                                 nltk.word_tokenize(stemmed.strip())):
            self.assertEqual(stem, stemmer.stem(token))

    def test_stem(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_2_PATH, min_freq=2, left_context=2)
        self.assertEqual('вероят', stemmer.stem('вероятен'))
        self.assertEqual('този', stemmer.stem('този'))

    def test_no_stem_context(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_2_PATH, left_context=10)
        self.assertEqual('оставката', stemmer.stem('оставката'))

    def test_stem_context1(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_1_PATH, min_freq=2, left_context=1)
        self.assertEqual('остав', stemmer.stem('оставката'))
        self.assertEqual('той', stemmer.stem('той'))

    def test_stem_context2(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_2_PATH, min_freq=2, left_context=2)
        self.assertEqual('оставк', stemmer.stem('оставката'))
        self.assertEqual('той', stemmer.stem('той'))

    def test_stem_context3(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_3_PATH, min_freq=2, left_context=3)
        self.assertEqual('оставк', stemmer.stem('оставката'))
        self.assertEqual('той', stemmer.stem('той'))

    def test_filter_freq(self):
        stemmer = BulStemmer.from_file(BulStemmerTest.RULES_3_PATH, min_freq=200000000)
        self.assertEqual('оставката', stemmer.stem('оставката'))
        self.assertEqual('вероятен', stemmer.stem('вероятен'))

    def test_manual_rules(self):
        stemmer = BulStemmer(["ой ==> о 10"], min_freq=0, left_context=0)
        self.assertEqual('поро', stemmer.stem('порой'))

    def test_allow_duplicates(self):
        stemmer = BulStemmer(["ой ==> о 10", "ой ==> о 30"], min_freq=0, left_context=0, allow_duplicates=True)
        self.assertEqual('поро', stemmer.stem('порой'))

    def test_duplicates_exception(self):
        with self.assertRaises(ValueError):
            BulStemmer(["ой ==> о 10", "ой ==> о 30"], min_freq=0, left_context=0)


if __name__ == '__main__':
    unittest.main()
