# -*- coding: utf-8 -*-
from inspector.src.twitter import Twitter
from inspector.src.classifier import classify_tweet


twitter = Twitter()
tweets = twitter.search_interval(u'крым lang:ru', emotion=':)')

twts = []
for tweet in tweets:
    if tweet['text'] not in twts:
        twts.append(tweet['text'])

with open('out.txt', 'w') as fff:
    for t in twts:
        fff.write(u'- "%s"\n'.encode('utf8') % t)

# tweets_2 = twitter.search_interval(u'крым lang:ru', emotion=':(')

#"""

posneg = dict(positive=0, negative=0)

for tweet in tweets:
    posneg[classify_tweet(tweet['text'].lower())] += 1


# print len(tweets['statuses']), len(tweets_2['statuses'])
print posneg
print len(tweets)

# print classify_tweet(u'люблю')
# print classify_tweet(u'Люблю')
# print classify_tweet(u'ненавижу')
# print classify_tweet(u'Ненавижу')

#"""
"""

from inspector import , Geocoder, settings
from geojson import Feature, Point, FeatureCollection
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta
from random import choice

geocoder = Geocoder()

# geocode='%f,%f,150km' % coord
query = 'крым'

tweets = twitter.search_interval(u'крым lang:ru')
tweets.extend(twitter.search_interval(u'crimea lang:es'))
tweets.extend(twitter.search_interval(u'crimea lang:pt'))
tweets.extend(twitter.search_interval(u'crimea lang:en'))
tweets.extend(twitter.search_interval(u'crimea lang:de'))
tweets.extend(twitter.search_interval(u'克里米亚 lang:zh'))

coords = geocoder.tweets_to_coords(tweets)

colors = dict(ru='red', es='green', en='blue', pt='orange', de='brown', zh='pink', no='white')

crd = dict()

for coord in coords:
    key = '%f;%f' % coord[1]

    if key in crd:
        crd[key]['w'] += 1
    else:
        crd[key] = dict(w=1, c=coord[1], color=dict(ru=0, es=0, en=0, pt=0, de=0, zh=0, no=0))

    if coord[2] in colors:
        crd[key]['color'][coord[2]] += 1
    else:
        crd[key]['color']['no'] += 1

features = []

import operator

for key, value in crd.iteritems():
    if value['c'] == (0., 0.):
        continue
    point = Point(value['c'])
    color = max(value['color'].iteritems(), key=operator.itemgetter(1))[0]
    feature = Feature(geometry=point, properties=dict(weight=value['w'], color=colors[color]))
    features.append(feature)

env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIR))
template = env.get_template('map.html')

with open(settings.RESULT_DIR + '/map-%s-%s.html' % (query, datetime.now().strftime('%Y.%m.%d-%H:%M')), 'w') as result:
    result.write(template.render(geoJson=FeatureCollection(features)))
"""
