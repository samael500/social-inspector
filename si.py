# -*- coding: utf-8 -*-
from inspector.src.twitter import Twitter
from inspector.src.geocoder import CachedGeocoder as Geocoder
from inspector.src.classifier import Classifier
from inspector.settings import DATA_DIR
import yaml


cls = Classifier()
geocoder = Geocoder()
twitter = Twitter()
print ''

xx = twitter.search(u'отчаяние lang:ru', emotion=':(')
xxx = []
for x in xx['statuses']:
    if x['text'].lower() not in xxx:
        xxx.append(x['text'].lower().replace('"', "'").replace('\n', " "))
for x in xxx:
    print u'- "%s"' % x

sys.exit()
# twitter.timeout = 0

from inspector import settings
from geojson import Feature, Point, FeatureCollection
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from random import choice


query = 'крым'
tweets = []
tweets = twitter.search_interval(u'крым lang:ru')
# tweets.extend(twitter.search_interval(u'crimea lang:es'))
# tweets.extend(twitter.search_interval(u'crimea lang:pt'))
tweets.extend(twitter.search_interval(u'crimea lang:en'))
# tweets.extend(twitter.search_interval(u'happy lang:en'))
# tweets.extend(twitter.search_interval(u'sad lang:en', emotion=':(', ))
# tweets.extend(twitter.search(u'sad lang:en', emotion=':)', count=10, )['statuses'])
# tweets.extend(twitter.search_interval(u'crimea lang:de'))
# tweets.extend(twitter.search_interval(u'克里米亚 lang:zh'))

coords = geocoder.tweets_to_coords(tweets)
coords = cls.classify_coord_tweets(coords)
colors = dict(positive='red', negative='blue', )

crd = dict()

for coord in coords:
    key = '%f;%f' % coord[1]

    if key in crd:
        crd[key]['w'] += 1
    else:
        crd[key] = dict(w=1, c=coord[1], color=dict(positive=0, negative=0))

    if coord[3] in colors:
        crd[key]['color'][coord[3]] += 1

features = []

import operator

for key, value in crd.iteritems():
    if value['c'] == (0., 0.):
        continue
    point = Point(value['c'])
    color = max(value['color'].iteritems(), key=operator.itemgetter(1))[0]
    feature = Feature(geometry=point, properties=dict(weight=value['color'][color], color=colors[color]))
    color = min(value['color'].iteritems(), key=operator.itemgetter(1))[0]
    feature = Feature(geometry=point, properties=dict(weight=value['color'][color], color=colors[color]))
    # feature = Feature(geometry=point, properties=dict(weight=value['w'], color=colors[color]))
    features.append(feature)

env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIR))
template = env.get_template('map.html')

with open(settings.RESULT_DIR + '/map-%s-%s.html' % (query, datetime.now().strftime('%Y.%m.%d-%H:%M')), 'w') as result:
    result.write(template.render(geoJson=FeatureCollection(features)))
