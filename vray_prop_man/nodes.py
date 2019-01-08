'''
Created on Jan 7, 2019

@author: carlos
'''
from itertools import count

from icons import get_icon
from tps.qt_helpers.tree_model_helper import Node


class Root(Node):
    def __init__(self):
        super(Root, self).__init__('root')


class Directory(Node):
    _counter = count()

    def __init__(self, api, parent=None):
        indx = self._counter.next()
        name = 'Directory_%s' % str(indx).zfill(4)
        super(Directory, self).__init__(name=name, parent=parent)
        self._icon = get_icon('browse')
        self._api = api
        self._props = {}

    def get_property(self, prop_name):
        """
        get the value stored in the current instance if any for the given property name

        :param prop_name:
        """
        if prop_name not in self._props:
            return None

        return self._props[prop_name]

    def set_property(self, prop_name, val):
        if not self._api.is_valid_prop_name(prop_name):
            raise ValueError('% is not a valid property name')
        self._props[prop_name] = val

    def set_property_by_index(self, index, val):
        prop_name = self._api.get_property_name_from_index(index)
        self.set_property(prop_name, val)

    def get_casc_property_by_index(self, index):
        """
        get cascading value for node based on index

        :param index:
        """
        prop_name = self._api.get_property_name_from_index(index)
        return self.get_casc_property(prop_name)

    def get_casc_property(self, prop_name):
        """
        get cascading property value for node

        :param prop_name:
        """

        val = self.get_property(prop_name)
        if val is not None:
            return val
        pars = self.list_parents() or []
        pars.reverse()
        for par in pars:
            if isinstance(par, Root):
                continue
            val = par.get_property(prop_name)
            if val is not None:
                return val

        return self._api.get_default_val(prop_name)
