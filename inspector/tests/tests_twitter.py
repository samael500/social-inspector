# -*- coding: utf-8 -*-

import unittest
from inspector.src.twitter import Twitter
from settings import DEBUG


class TestTwitter(unittest.TestCase):

    """ Test twitter class """

    # @unittest.skipIf(DEBUG, "Don't test when debug")
    def setUp(self):
        self.twitter = Twitter()

    def test_twitter_constants(self):
        """ Check twitter class has correct values """
        self.assertEquals(self.twitter.query_string, u'{query} since:{since} until:{until} {emotion}')
        self.assertEquals(self.twitter.date_format, '%Y-%m-%d')
        self.assertEquals(self.twitter.geocode, u'44.948056,34.104167,250km')
        self.assertEquals(self.twitter.timeout, 1)

    def test_twitter_search(self):
        """ Test search tweets """
        self.twitter.query_string = u'#test lang:en'
        self.twitter.timeout = 0
        search_list = self.twitter.search()
        for tweet in search_list['statuses']:
            self.assertIn(u'test', tweet['text'].lower())

    def test_twitter_search_interval(self):
        """ Test search tweets """
        self.twitter.query_string = u'#test lang:en'
        self.twitter.timeout = 0
        search_list = self.twitter.search_interval(query=u'#test lang:en')
        for tweet in search_list:
            self.assertIn(u'test', tweet['text'].lower())
