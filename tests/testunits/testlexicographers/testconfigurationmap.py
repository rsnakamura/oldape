from unittest import TestCase

from mock import MagicMock

from tottest.lexicographers import configurationmap

ConfigurationMap = configurationmap.ConfigurationMap


class ConfigurationMapTest(TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.map = ConfigurationMap("name")
        self.map._parser = self.parser
        return

    def test_get_ranges(self):
        self.map.get_list = MagicMock()
        self.map.get_list.return_value = ['1-3']
        ranges = self.map.get_ranges("NAXXX", "switches")
        self.assertEqual(ranges, [1,2,3])
        self.map.get_list.return_value = None
        ranges = self.map.get_ranges("NAXXX", 's')
        self.assertEqual(ranges, None)
        self.map.get_list.return_value = ['2-5', '10', '3-12']
        ranges = self.map.get_ranges('NAXXX', 'switches')
        self.assertEqual(ranges, [2,3,4,5,10,3,4,5,6,7,8,9,10,11,12])
        return

    def test_get_list(self):
        value = "3,4,5"
        self.map._parser.get.return_value = value
        output = self.map.get_list("DUT", "ids")
        self.assertEqual(value.split(','), output)
        return

    def test_get_list_optional(self):
        value = None
        self.map._parser.get.return_value = value
        output = self.map.get_list("DUT", "paths", optional=True)
        self.assertEqual(value, output)
