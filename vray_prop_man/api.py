'''
Created on Jan 7, 2019

@author: carlos
'''
from nodes import Directory
from tps.dcc_commands import load_dcc_commands


class VrayPropManApi(object):
    def __init__(self, dcc=None):
        dcc = dcc or 'base'
        self._cmds = load_dcc_commands(dcc)

    def get_default_property_dic(self):
        dic = {'use_default_mobo_samples': True,
               'mobo_samples': 2,
               'mobo_duration_on': False,
               'mobo_duration': 1.0,
               'velo_chan_on': False,
               'velo_chan': 1,
               'velo_chan_mult': 1.0,
               'matte_obj_on': False,
               'matte_refl_refr_on': False,
               'alpha_contribution': 0.0}

        return dic

    def create_directory(self):
        """
        create directory node
        """
        dirnd = Directory(self)
        return dirnd

    def is_valid_prop_name(self, prop_name):
        def_dic = self.get_default_property_dic()
        return prop_name in def_dic

    def get_property_names(self):
        keys = self.get_default_property_dic().keys()
        keys.sort()
        return keys

    def get_property_index(self, prop_name):
        if not self.is_valid_prop_name(prop_name):
            raise ValueError('%s is not a valid property name' % prop_name)

        props = self.get_property_names()
        return props.index(prop_name)

    def get_property_name_from_index(self, index):
        props = self.get_property_names()
        try:
            return props[index]
        except IndexError:
            raise ValueError('%i is not a valid property index' % index)

    def get_default_val(self, prop_name):
        dic = self.get_default_property_dic()
        return dic[prop_name]
