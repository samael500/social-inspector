import unittest


class TestColor(unittest.TestCase):

    def test_true(self):
        self.assertTrue(5 == 5)
        self.assertTrue(5 is 5)
        self.assertTrue(True)
        self.assertTrue(not False)

    def test_false(self):
        self.assertFalse(5 != 5)
        self.assertFalse(5 is not 5)
        self.assertFalse(not True)
        self.assertFalse(False)
