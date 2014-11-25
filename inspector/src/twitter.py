# -*- coding: utf-8 -*-

from settings import TWITTER_OAUTH_INFO
from twython import Twython, TwythonError
from datetime import datetime, timedelta

import time


class Twitter(object):

    """ Class for twitter use """

    query_string = u'{query} since:{since} until:{until} {emotion}'

    date_format = '%Y-%m-%d'
    timeout = 1

    def __init__(self, auth=TWITTER_OAUTH_INFO):
        self.twitter = Twython(**auth)

    def search(self, query=None, emotion='', geocode='44.948056,34.104167,250km', count=100, since=None, until=None):
        """ Search tweet with query ref """
        since = since or (datetime.now() - timedelta(days=7)).strftime(self.date_format)
        until = until or datetime.now().strftime(self.date_format)
        query = self.query_string.format(query=query, since=since, until=until, emotion=emotion).strip()
        return self.twitter.search(q=query, count=count, geocode=geocode)

    def search_interval(self, query, since=None, until=None):
        """
        Serch tweets of query in given interval for every day
        Warning! API return only last week tweets, so be careful with interval
        """
        tweets = []
        # get dates of interval
        since = since or (datetime.now() - timedelta(days=7)).strftime(self.date_format)
        until = until or datetime.now().strftime(self.date_format)
        d_start = datetime.strptime(since, self.date_format).date()
        d_end = datetime.strptime(until, self.date_format).date()
        days = (d_end - d_start).days
        dates = [d_start + timedelta(days=day) for day in xrange(days + 1)]
        # for every day search
        for day in xrange(days):
            since = dates[day].strftime(self.date_format)
            until = dates[day + 1].strftime(self.date_format)
            try:
                tweets.extend(self.search(query, since=since, until=until, geocode=None)['statuses'])
            except Exception, e:
                print e.message
            time.sleep(self.timeout)
        return tweets
