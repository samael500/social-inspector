# -*- coding: utf-8 -*-

from src.twitter import Twitter
from src.geocoder import CachedGeocoder
from src.classifier import Classifier


class Inspector(object):

    """ The engine inspector class """

    def __init__(self):
        self.twitter = Twitter()
        self.geocoder = CachedGeocoder()
        self.classifier = Classifier()

    def search(self, query, since, until,):
        """ Search tweets data and classify it """
        tweets = []
        for lang in ('ru', 'en', 'es', 'pt', 'de'):
            tweets.extend(self.twitter.search_interval(
                query=u'{query} lang:{lang}'.format(query=query, lang=lang), since=since, until=until))
        # get coords from tweets and classify it
        return self.classifier.classify_coord_tweets(self.geocoder.tweets_to_coords(tweets))

    def classify(self, message):
        """ Classify given text """
        return self.classifier.classify_tweet(message)

    def create_map(self, coord_tweets):
        pass
