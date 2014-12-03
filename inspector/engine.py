# -*- coding: utf-8 -*-

from geojson import Feature, Point, FeatureCollection
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta

from inspector import settings
from inspector.src.twitter import Twitter
from inspector.src.geocoder import CachedGeocoder
from inspector.src.classifier import Classifier

import operator


class Inspector(object):

    """ The engine inspector class """

    def __init__(self):
        self.twitter = Twitter()
        self.geocoder = CachedGeocoder()
        self.classifier = Classifier()

    def search(self, query, since, until,):
        """ Search tweets data and classify it """
        print ('Start search!')
        tweets = []
        for lang in ('ru', 'en', 'es', 'pt', 'de'):
            tweets.extend(self.twitter.search_interval(
                query=u'{query} lang:{lang}'.format(query=query, lang=lang), since=since, until=until))
        # get coords from tweets and classify it
        print ('Start geocode!')
        coord_tweets = self.geocoder.tweets_to_coords(tweets)
        print ('Start classifyer!')
        classified_tweets = self.classifier.classify_coord_tweets(coord_tweets)
        return classified_tweets

    def classify(self, message):
        """ Classify given text """
        return self.classifier.classify_tweet(message)

    def create_map(self, coord_tweets, query):
        """ Generate g-maps with tweets point mark """
        colors = dict(positive='red', negative='blue', )
        # define madgic num
        COORDINATES = 1
        COLOR = 3
        # coord dict - to accomulate tweets in one point
        crd = dict()
        for tweet in coord_tweets:
            key = '%f;%f' % tweet[COORDINATES]
            if key in crd:  # if point in coord dict - add weight
                crd[key]['w'] += 1
            else:  # else create new coord dict row
                crd[key] = dict(w=1, c=tweet[COORDINATES], color=dict(positive=0, negative=0))
            # set color of this point to coord dict
            if tweet[COLOR] in colors:
                crd[key]['color'][tweet[COLOR]] += 1
        features = []
        for key, value in crd.iteritems():
            # if coord was not succes detected
            if value['c'] == (0., 0.):
                continue
            point = Point(value['c'])
            # create two point for + and - sentiment
            color = max(value['color'].iteritems(), key=operator.itemgetter(1))[0]
            # feature = Feature(geometry=point, properties=dict(weight=value['color'][color], color=colors[color]))
            # color = min(value['color'].iteritems(), key=operator.itemgetter(1))[0]
            # feature = Feature(geometry=point, properties=dict(weight=value['color'][color], color=colors[color]))
            feature = Feature(geometry=point, properties=dict(weight=value['w'], color=colors[color]))
            features.append(feature)

        # load template
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIR))
        template = env.get_template('map.html')
        title = query.replace(' OR ', ' / ')
        # render to file
        with open(settings.RESULT_DIR + '/map-%s.html' % (datetime.now().strftime('%Y.%m.%d-%H:%M')), 'w') as result:
            result.write(template.render(geoJson=FeatureCollection(features), title=title).encode('utf-8'))
