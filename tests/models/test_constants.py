import unittest

from pymocky.models.constants import Constants


class ConstantTests(unittest.TestCase):
    def test_default_values(self):
        self.assertEqual(Constants.HOST, "0.0.0.0")
        self.assertEqual(Constants.PORT, 9000)
        self.assertEqual(Constants.DEFAULT_SCENARIO, "default")
