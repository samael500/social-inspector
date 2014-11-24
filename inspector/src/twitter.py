# -*- coding: utf-8 -*-

from settings import TWITTER_OAUTH_INFO
from twython import Twython, TwythonError

from datetime import datetime, timedelta


class Twitter(object):

    """ Class for twitter use """

    query_string = u'{query} since:"{since}" until:"{until}" {emotion}'
    date_format = '%Y-%m-%d'

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def search(self, query=None, emotion='', geocode='44.948056,34.104167,250km', count=100, since=None, until=None):
        """ Search tweet with query ref """
        since = since or (datetime.now() - timedelta(days=7)).strftime(self.date_format)
        until = until or datetime.now().strftime(self.date_format)
        query = self.query_string.format(query=query, since=since, until=until, emotion=emotion).strip()
        return self.twitter.search(q=query, count=count, geocode=geocode)
