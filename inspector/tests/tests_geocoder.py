# -*- coding: utf-8 -*-

import unittest
from inspector.src.geocoder import CachedGeocoder
from settings import DEBUG

import os


class TestGeocoder(unittest.TestCase):

    """ Test geocoder class """

    def setUp(self):
        self.filename = 'test_%s' % CachedGeocoder.filename
        self.geocoder = CachedGeocoder(filename=self.filename)
        self.filepath = self.geocoder.get_geocode_path
        self.assertEquals(self.geocoder.geocodes, dict())

    def tearDown(self):
        # rm file after tests
        del self.geocoder
        os.remove(self.filepath)

    def test_geocoder_constants(self):
        """ Check twitter class has correct values """
        self.assertEquals(CachedGeocoder.timeout, 2)
        self.assertEquals(CachedGeocoder.geocodes, dict())
        self.assertEquals(CachedGeocoder.filename, 'geocode')
        self.assertEquals(CachedGeocoder.filename_suffix, '.json')

    def test_geocoder_loads(self):
        """ Test load geocode data """
        self.assertEquals(self.geocoder.geocodes, dict())
        # set data to geocoder dict
        test_coords = dict(test=dict(lat=3.3, lon=5.5))
        filepath = self.geocoder.get_geocode_path
        self.geocoder.geocodes.update(test_coords)
        # delete obj to save to file
        del self.geocoder
        # load new object to get data from file
        self.geocoder = CachedGeocoder(filename=self.filename)
        self.assertEquals(self.geocoder.geocodes, test_coords)

    def test_geocoder_empty(self):
        """ Test load geocode data """
        del self.geocoder
        # load new object to get data from file
        self.geocoder = CachedGeocoder(filename=self.filename)
        self.assertEquals(self.geocoder.geocodes, {'': dict(lat=0, lon=0)})

    def test_geocoder_geocode(self):
        """ Test get geocode coord response """
        # get coord
        sev1 = {'lat': 44.61665, 'lon': 33.525367}
        sev2 = {'lat': 44.61661, 'lon': 33.525363}
        coord = self.geocoder.geocode(u'Севастополь')
        self.assertEquals(coord, sev1)
        # change coord to check no new request
        self.geocoder.geocodes[u'севастополь'] = sev2
        coord = self.geocoder.geocode(u'Севастополь')
        self.assertEquals(coord, sev2)
        self.assertNotEquals(sev1, sev2)

    def test_geocoder_zero_result(self):
        """ Test get geocode zero response """
        # get coord
        coord0 = {'lat': 0, 'lon': 0}
        coord = self.geocoder.geocode(u'asdflkjasdg')
        self.assertEquals(coord, coord0)
