# -*- coding: utf-8 -*-

import unittest
from inspector.engine import Inspector
from inspector import settings
from datetime import datetime, timedelta
import os
import shutil


class TestInspectorClass(unittest.TestCase):

    """ Test inspector class """

    def setUp(self):
        settings.RESULT_DIR = os.path.join(settings.BASE_DIR, 'test_out')
        self.inspector = Inspector()

    def test_inspector_langs(self):
        """ Check langs for inspector """
        for lang in ('ru', 'en', 'es', 'pt', 'de'):
            self.assertIn(lang, Inspector.languages)

    def test_inspector_classify(self):
        """ Check correct classify """
        self.assertEquals('positive', self.inspector.classify('happy'))
        self.assertEquals('negative', self.inspector.classify('sad'))

    def test_inspector_search(self):
        self.inspector.twitter.twitter.query_string = u'#test lang:en'
        self.inspector.twitter.twitter.timeout = 0
        since = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        until = datetime.now().strftime('%Y-%m-%d')
        search_list = self.inspector.search(query=u'#test lang:en', since=since, until=until)
        for tweet in search_list:
            self.assertTrue(isinstance(tweet[0], unicode))
            self.assertTrue(isinstance(tweet[1], tuple))
            self.assertTrue(isinstance(tweet[2], unicode))
            self.assertTrue(isinstance(tweet[3], str))
        # check map
        self.assertFalse(os.path.exists(settings.RESULT_DIR))
        os.makedirs(settings.RESULT_DIR)
        self.assertTrue(os.path.exists(settings.RESULT_DIR))
        self.assertNotIn('.html', ''.join(os.listdir(settings.RESULT_DIR)))
        self.inspector.create_map(search_list, 'test')
        self.assertIn('.html', ''.join(os.listdir(settings.RESULT_DIR)))
        # clear result
        shutil.rmtree(settings.RESULT_DIR)
