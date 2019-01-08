'''
Created on Jan 7, 2019

@author: carlos
'''
import unittest

from Qt import QtGui, QtWidgets
from icons import get_icon


class TestIconLib(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        app = QtWidgets.QApplication.instance()
        if not app:
            app = QtWidgets.QApplication([])

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        app = QtWidgets.QApplication.instance()
        del app

    def test_get_browse_icon(self):
        icon = get_icon('browse')
        self.assertTrue(isinstance(icon, QtGui.QIcon))

    def test_get_invalid_icon(self):
        with self.assertRaises(ValueError):
            icon = get_icon('trash icon that dont exist')


if __name__ == '__main__':
    unittest.main()
