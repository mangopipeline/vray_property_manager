'''
Created on Jan 7, 2019

@author: carlos
'''
import __future__

import unittest

from tps.dcc_commands import load_dcc_commands


class TestDccCommands(unittest.TestCase):
    def test_error(self):
        api = load_dcc_commands()

        with self.assertRaises(RuntimeError):
            api = load_dcc_commands(dcc='unsported app')


if __name__ == '__main__':
    unittest.main()
