# -*- coding: utf-8 -*-

import unittest
from inspector.src.classifier import Classifier


class TestClassifier(Classifier):
    filenames = ('positive.test', 'negative.test', )


class TestClassifierClass(unittest.TestCase):

    """ Test classifier class """

    def setUp(self):
        self.classifier = TestClassifier()

    def test_classifier_constants(self):
        """ Check classifier class has correct values """
        for name in ('positive.ru', 'positive.en', 'negative.ru', 'negative.en'):
            self.assertIn(name, Classifier.filenames)
        self.assertEquals(Classifier.filename_suffix, '.yaml')

    def test_file_path(self):
        """ Check correct filepath returned """
        filepaths = list(self.classifier.get_file_path)
        self.assertIn('/positive.test.yaml', filepaths[0][0])
        self.assertIn('/negative.test.yaml', filepaths[1][0])
        self.assertEquals('positive', filepaths[0][1])
        self.assertEquals('negative', filepaths[1][1])

    def test_classify_tweet(self):
        """ Check correct classify tweet """
        self.assertEquals('positive', self.classifier.classify_tweet('i am happy'))
        self.assertEquals('negative', self.classifier.classify_tweet('i am sad'))

    def test_classify_coord_tweets(self):
        """ Check correct classify tweet list """
        tweets = (['i am happy'], ['i am sad'], )
        tweets = self.classifier.classify_coord_tweets(tweets)
        self.assertEquals('positive', tweets[0][1])
        self.assertEquals('negative', tweets[1][1])
