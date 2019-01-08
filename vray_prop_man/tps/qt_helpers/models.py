'''
Created on Jan 7, 2019

@author: carlos
'''

from Qt import QtCore


class BasicTreeModel(QtCore.QAbstractItemModel):
    '''
    Basic Tree Model that works with colossus Node helpers for mapping out data

    :param data: this is the root node that for the data you like to map out
    :type data: colossus.Utils.Qt.tree_heler.Node
    :param columns: the name of the columns you would like to use in your view
    :type columns: [str]
    '''

    sortRole = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    itemRole = QtCore.Qt.UserRole + 2

    def __init__(self, data, columns=None, parent=None):
        super(BasicTreeModel, self).__init__(parent)
        self._data = data
        self._columns = columns or ['column1']

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self._data
        else:
            parent_node = parent.internalPointer()

        return len(parent_node.children)

    def columnCount(self, parent):
        return len(self._columns)

    def getDataFromIndex(self, index):
        return self.data(index, self.itemRole)

    def data(self, index, role):
        '''
        # example
        if not index.isValid(): return None

        node = index.internalPointer()
        if role == self.itemRole: return node

        column = index.column()
        key = self._columns[column]
        row = index.row()

        if role in (QtCore.Qt.DisplayRole, self.filterRole): return self.getValue(node, key)
        if role == QtCore.Qt.ToolTipRole: return node.tool_tip()
        if role == self.sortRole: return node.sort_value()
        '''
        pass

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return self._columns[section].title()

    def parent(self, index):
        node = index.internalPointer()
        parent_node = node.parent

        if parent_node == self._data:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)
        child_item = None

        if parent_node.children:
            child_item = parent_node.children[row]

        if child_item:
            return self.createIndex(row, column, child_item)

        return QtCore.QModelIndex()

    def getNode(self, index):
        if index is None:
            return self._data
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._data

    def indexFromNode(self, nd):
        if not nd.parent:
            return QtCore.QModelIndex()
        row = nd.parent.children.index(nd)
        return self.createIndex(row, 0, nd)

    def removeRow(self, nd, keep_chld=True):
        index = self.indexFromNode(nd)
        parent = self.indexFromNode(nd.parent)

        # keep children
        if keep_chld:
            new_p = self.createIndex(-1, -1, self._data)
            ch = nd.children[:]
            dest_int = len(self._data.children)

            self.beginMoveRows(index, 0, len(ch), new_p, dest_int)
            for c in ch:
                c.parent = self._data
            self.endMoveRows()

        # kill node
        r = index.row()
        self.beginRemoveRows(parent, r, r)
        nd.parent = None
        del nd
        self.endRemoveRows()

    def insertNode(self, node, parent=None):
        if not parent:
            parent = self._data
        p_index = self.indexFromNode(parent)
        pos = len(parent.children)
        self.beginInsertRows(p_index, pos, pos)
        node.parent = parent
        self.endInsertRows()


class BasicTableModel(QtCore.QAbstractTableModel):
    '''
    Basic Table Model that works with with lists  for mapping out data

    :param data: this is the root node that for the data you like to map out
    :type data: colossus.Utils.Qt.tree_heler.Node
    :param columns: the name of the columns you would like to use in your view
    :type columns: [str]
    '''
    itemRole = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    sortRole = QtCore.Qt.UserRole + 2

    def __init__(self, data, columns=None, parent=None):
        super(BasicTableModel, self).__init__(parent)
        self._columns = columns or ['column1']
        self._data = data

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._columns[section].title()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._columns)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        index = self.createIndex(row, column, parent)
        return index

    def getItemFromIndex(self, index):
        return self.data(index, self.itemRole)

    def data(self, index, role):
        '''

        # example
        if not index.isValid(): return
        row = index.row()
        column = index.column()
        ent = self._data[row]

        if role == self.itemRole: return self._data[row]

        if role == QtCore.Qt.DisplayRole or role == self.filterRole or role == self.sortRole:
            return self.getEntValue(self._data[row], self._columns[column])

        if role == QtCore.Qt.DecorationRole:
            if column == 0:
                if type(ent).__name__ == 'Resources': return self.getResourceIcon(ent)
                return self.iconC.get_icon('versionIcon')

        if role == QtCore.Qt.TextAlignmentRole:
            if column != 0: return QtCore.Qt.AlignCenter

        if role == QtCore.Qt.FontRole:
            if column == 0:
                font = QtGui.QFont()
                font.setBold(True)
                return font
        '''
        pass

    def updateData(self, data, parent=QtCore.QModelIndex()):
        self.layoutAboutToBeChanged.emit()
        rC = self.rowCount()
        dC = len(data)

        # add display rows if need be

        if dC > rC:
            dif = (dC - rC) - 1
            self.beginInsertRows(parent, rC, rC + dif)
            self._data = data
            self.endInsertRows()
        # remove rows if need be
        elif dC < rC:
            dif = (rC - dC)
            self.beginRemoveRows(parent, dif, rC - 1)
            self._data = data
            self.endRemoveRows()
        else:
            self._data = data

        self.layoutChanged.emit()


class BasicStringList(BasicTableModel):
    def data(self, index, role):
        basic_roles = (QtCore.Qt.DisplayRole,
                       QtCore.Qt.EditRole,
                       self.filterRole,
                       self.sortRole,
                       self.itemRole)

        if role in basic_roles:
            return self._data[index.row()]
