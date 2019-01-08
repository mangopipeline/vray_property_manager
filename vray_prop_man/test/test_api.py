import __future__

import unittest

from api import VrayPropManApi


class TestApi(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._api = VrayPropManApi()

    def test_propname_index_mapping(self):
        prop_names = self._api.get_property_names()
        # test round trip mapping
        index_list = [self._api.get_property_index(name) for name in prop_names]
        test_vals = [self._api.get_property_name_from_index(index) for index in index_list]

        self.assertListEqual(prop_names, test_vals)


if __name__ == '__main__':
    unittest.main()
