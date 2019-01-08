'''
Created on Jan 7, 2019

@author: carlos
'''
import os

from Qt import QtWidgets, QtCore

from nodes import Root
from tps.qt_helpers import makeQSortFilterProxyModel, setHeaderViewResizeMode
from tps.qt_helpers.uic import load_ui_type
from tree_model import TreeModel


BASE, FORM = load_ui_type(os.path.join(os.path.dirname(__file__), 'ui', 'property_mapper.ui'))


class VrayPropertyMapper(BASE, FORM):
    def __init__(self, api, parent=None):
        super(VrayPropertyMapper, self).__init__(parent)
        self.setupUi(self)
        self._api = api


class VrayPropTreeView(QtWidgets.QTreeView):
    on_parent_changed = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, api, parent=None):
        super(VrayPropTreeView, self).__init__(parent=parent)

        self._tree_model = None
        self._tree_proxy = None
        self._api = api
        self._root = Root()
        self._setup()
        self._connect_signals()

    def get_proxy(self):
        return self._tree_proxy

    def get_model(self):
        return self._tree_model

    def _setup(self):
        # setup drag an drop
        self.setDragDropMode(self.InternalMove)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropOverwriteMode(True)

        self._tree_model = TreeModel(self._api, self._root, parent=self)
        self._tree_proxy = makeQSortFilterProxyModel(self)
        self._tree_proxy.setSourceModel(self._tree_model)
        self.setSortingEnabled(True)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self._tree_proxy.setDynamicSortFilter(True)

        self._tree_proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._tree_proxy.setSortRole(TreeModel.sortRole)
        self._tree_proxy.setFilterRole(TreeModel.filterRole)

        self.setModel(self._tree_proxy)
        self.setColumnWidth(0, 175)

        header = self.header()
        header.setStretchLastSection(False)
        setHeaderViewResizeMode(header, QtWidgets.QHeaderView.Stretch, 0)
        self.setAnimated(True)

    def _gen_new_dir(self):
        dir = self._api.create_directory()
        self._tree_model.insertNode(dir)

    def _rcmenu(self, x):
        menu = QtWidgets.QMenu(self)
        new_dir = QtWidgets.QAction(self)
        new_dir.setText('New Directory')
        new_dir.triggered.connect(self._gen_new_dir)
        menu.addAction(new_dir)
        menu.exec_(self.mapToGlobal(x))

    def _connect_signals(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda x: self._rcmenu(x))

    def _is_valid_drop(self, drag_node, drop_node):
        if not drop_node and drag_node.parent == self._root:
            return False
        if drag_node == drop_node:
            return False
        if not drop_node:
            return True
        if drag_node.parent == drop_node:
            return False
        if drop_node.is_descendant_of(drag_node):
            return False
        return True

    def _get_importer_at_pos(self, pos):
        index = self._tree_proxy.mapToSource(self.indexAt(pos))
        return self._tree_model.data(index, self._tree_model.itemRole)

    def get_selected_impoter(self):
        selMod = self.selectionModel()
        indx = selMod.selectedIndexes()[0]
        indx = self._tree_proxy.mapToSource(indx)
        return self._tree_model.data(indx, self._tree_model.itemRole)

    def dragMoveEvent(self, event):
        drag_node = self.get_selected_impoter()
        drop_node = self._get_importer_at_pos(event.pos())

        if not self._is_valid_drop(drag_node, drop_node):
            event.ignore()
            return

        event.accept()

    def dropEvent(self, event):
        self._updateSel = False
        drop_node = self._get_importer_at_pos(event.pos())
        drag_node = self.get_selected_impoter()

        if not self._is_valid_drop(drag_node, drop_node):
            event.ignore()
            return

        new_index = self._tree_model.parentNode(drag_node, drop_node)
        self.on_parent_changed.emit(new_index)


if __name__ == '__main__':
    APP = QtWidgets.QApplication([])
    UI = VrayPropTreeView()
    UI.show()
    APP.exec_()
