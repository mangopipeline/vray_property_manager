'''
Created on Jan 7, 2019

@author: carlos
'''
import __future__

from Qt import QtCore, QtGui
from tps.qt_helpers.models import BasicTreeModel


class TreeModel(BasicTreeModel):
    _columns = ['Node']

    def __init__(self, api, data, parent=None):
        super(TreeModel, self).__init__(data, self._columns, parent)
        self._api = api

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def flags(self, index):
        default_flags = super(TreeModel, self).flags(index)
        flags = default_flags | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEditable
        return flags

    def parentNode(self, node, parent):
        """
        use this method to move the parenting relationship unlike insert which adds rows
        this uses the move command internaly

        :param node:
        :param parent:
        """

        if not parent:
            parent = self._data

        destination_parent = self.indexFromNode(parent)
        new_indx = self.indexFromNode(node)
        sourceParent = self.parent(new_indx)
        dest = len(parent.children)
        row = new_indx.row()

        self.beginMoveRows(sourceParent, row, row, destination_parent, dest)
        node.parent = parent
        self.endMoveRows()
        return self.indexFromNode(node)

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()
        column = index.column()
        row = index.row()

        if role == self.itemRole:
            return self.getNode(index)

        if role in (QtCore.Qt.DisplayRole, self.sortRole, self.filterRole):
            return node.name

        if role == QtCore.Qt.EditRole:
            if column == 0:
                return node.name
            return node.get_casc_property_by_index(column)

        if role == QtCore.Qt.DecorationRole:
            icon = node.icon()
            if icon:
                return icon

    def setData(self, index, data, role):
        if role != QtCore.Qt.EditRole:
            return True

        if not index.isValid():
            return False

        node = index.internalPointer()
        column = index.column()
        if column == 0:
            # NOTE: #the re parenting process seem to be doing a name change...
            # NOTE: not sure what's that's about so if data is not set we use default
            node.name = data or node.name
        else:
            node.set_property_by_index(column, data)
        return True
