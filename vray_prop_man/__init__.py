'''
Created on Jan 7, 2019

@author: carlos
'''
import __future__

import os

from Qt import QtWidgets
from api import VrayPropManApi
from tps.qt_helpers.uic import load_ui_type
from widgets import VrayPropTreeView, VrayPropertyMapper


BASE, FORM = load_ui_type(os.path.join(os.path.dirname(__file__), 'ui', 'main.ui'))


class MainUi(BASE, FORM):
    """
    Main UI Class
    """

    def __init__(self, dcc='base', parent=True):
        super(MainUi, self).__init__(parent)
        self._api = VrayPropManApi(dcc=dcc)
        self.setupUi(self)
        self._setup_view()
        self._map_widget_to_model()

    def _setup_view(self):
        self._view = VrayPropTreeView(self._api, parent=self)
        self._mapw = VrayPropertyMapper(self._api, parent=self)

        self.verticalLayout_2.addWidget(self._mapw)
        self.verticalLayout.addWidget(self._view)

    def _set_mapper_index(self, index):
        proxy = self._view.get_proxy()
        index = proxy.mapToSource(index)

        self._mapper_obj.setRootIndex(index.parent())
        self._mapper_obj.setCurrentModelIndex(index)

    def _mapper_parent_change(self, index):
        self._mapper_obj.setRootIndex(index.parent())
        self._mapper_obj.setCurrentModelIndex(index)

    def _map_widget_to_model(self):
        self._mapper_obj = QtWidgets.QDataWidgetMapper(self)

        self._mapper_obj.setModel(self._view.get_model())

        self._mapper_obj.addMapping(self._mapw.use_def_mob_smpl,
                                    self._api.get_property_index('use_default_mobo_samples'))

        sel_mod = self._view.selectionModel()
        sel_mod.currentChanged.connect(self._set_mapper_index)
        self._view.on_parent_changed.connect(self._mapper_parent_change)


def run_vray_prop_man_ui(dcc='base'):
    """
    convenience method for quickly running opening the ui
    """
    runapp = False
    app = QtWidgets.QApplication.instance()
    if not app:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        runapp = True

    ui = MainUi(parent=None)
    ui.show()

    if runapp:
        sys.exit(app.exec_())

    return app


if __name__ == '__main__':
    run_vray_prop_man_ui()
