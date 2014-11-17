# -*- coding: utf-8 -*-

from settings import TWITTER_OAUTH_INFO
from twython import Twython, TwythonError

from datetime import datetime, timedelta


class Twitter(object):

    """ Class for twitter use """

    query_string = u'{query} since:"{since}" until:"{until}" {emotion}'

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def search(self, query=None, emotion='', geocode='44.948056,34.104167,150km', count=100, since=None, until=None):
        """ Search tweet with query ref """
        since = since or (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        until = until or datetime.now().strftime('%Y-%m-%d')
        query = self.query_string.format(query=query, since=since, until=until, emotion=emotion).strip()
        return self.twitter.search(q=query, count=count, geocode=geocode)
