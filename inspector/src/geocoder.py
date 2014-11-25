# -*- coding: utf-8 -*-

from pygeocoder import Geocoder, GeocoderError
from inspector.settings import DATA_DIR
import time
import json
import os


class CachedGeocoder(Geocoder):

    """ Overrides geocoder to minimize the number of queries """

    timeout = 2
    geocodes = {}

    filename = 'geocode'
    filename_suffix = '.json'

    def __init__(self, *args, **kwargs):
        super(CachedGeocoder, self).__init__(*args, **kwargs)
        # load codes from file
        self.load_geocodes()

    def __del__(self):
        # save codes to file
        self.geocodes.update({'': dict(lat=0, long=0)})
        self.save_geocodes()

    def geocode(self, address, **kwargs):
        address = address.lower().replace(',', ' ').strip()
        if address not in self.geocodes:
            time.sleep(self.timeout)
            try:
                result = super(CachedGeocoder, self).geocode(address=address, **kwargs)
                self.geocodes[address] = self.get_coords(result)
            except GeocoderError, err:
                if err.message == GeocoderError.G_GEO_ZERO_RESULTS:
                    self.geocodes[address] = dict(lat=0, lon=0)
                else:
                    raise err
        return self.geocodes.get(address)

    def get_coords(self, geocoder_result):
        coords = geocoder_result[0].coordinates
        return dict(lat=coords[0], lon=coords[1])

    @property
    def get_geocode_path(self):
        """ Return file path to self geocode file """
        return os.path.join(DATA_DIR, self.filename + self.filename_suffix)

    def load_geocodes(self):
        """ Init geocodes as dict if available file path, else - {} """
        try:
            with open(self.get_geocode_path, 'r') as geocodes_file:
                self.geocodes = json.load(geocodes_file)
        except IOError:
            self.geocodes = {}
        return self.geocodes

    def save_geocodes(self):
        """ Save geocodes as file """
        with open(self.get_geocode_path, 'w') as geocodes_file:
            geocodes_file.write(json.dumps(self.geocodes))

    def tweets_to_coords(self, tweets):
        """ Convert list of tweets to list of (message, coord) """
        result = []
        for tweet in tweets:
            coord = None
            if tweet['coordinates']:
                coord = tuple(tweet['coordinates']['coordinates'])
            elif tweet['place']:
                coord = tweet['place']['bounding_box']['coordinates'][0][0]
            elif tweet['user'] and tweet['user']['location']:
                try:
                    gc = self.geocode(tweet['user']['location'])
                    coord = (gc['lon'], gc['lat'])
                except Exception, e:
                    print e.message
            if not coord:
                continue
            # coord must be an tuple!
            assert isinstance(coord, tuple)
            result.append((tweet['text'], coord, tweet['user']['lang']))
        return result
