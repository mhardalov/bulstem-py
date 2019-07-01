# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import nltk
import unittest

from bulstem.stem import BulStemmer


class BulStemmerTest(unittest.TestCase):
    RULES_PATH = './rules/stem_rules_context_2_utf8.txt'

    def test_full_stem(self):
        stemmer = BulStemmer(BulStemmerTest.RULES_PATH, min_freq=2, left_context=3)
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
        stemmer = BulStemmer(BulStemmerTest.RULES_PATH, min_freq=2, left_context=3)
        self.assertEqual('вероят', stemmer.stem('вероятен'))


if __name__ == '__main__':
    unittest.main()
