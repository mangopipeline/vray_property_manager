'''
this methods are meant to help keep code working on both PySide and PySide2
Latest version of
'''

# TODO:  Qt.py makes some of this stuff obsolete as soon as they
# adress the QStyleOptionViewItem there should be and attempt to depricate

from Qt import QtCore, QtGui, QtWidgets, QtMultimedia


def setHeaderViewResizeMode(widget, mode, column=0):
    try:
        return widget.setSectionResizeMode(column, mode)
    except Exception:
        return widget.setResizeMode(column, mode)


def makeQSortFilterProxyModel(parent):
    try:
        # Qt5
        return QtCore.QSortFilterProxyModel(parent)
    except Exception:
        # Qt4
        return QtGui.QSortFilterProxyModel(parent)


def QStyleOptionViewItem(opt):
    try:
        # TODO: this is a patch as the Qt lib seems be broken in the latest version
        import PySide.QtGui as tmp
        return tmp.QStyleOptionViewItemV4(opt)
    except Exception, e:
        # print str(e)
        return QtWidgets.QStyleOptionViewItem(opt)


def getQItemSelectionModel():
    try:
        # Qt5
        return QtCore.QItemSelectionModel
    except Exception:
        # Qt4
        return QtGui.QItemSelectionModel


def QItemSelection():
    try:
        return QtGui.QItemSelection()
    except Exception:
        return QtCore.QItemSelection()


def QSoundInstnace(*args, **kwargs):
    try:
        return QtMultimedia.QSound(*args, **kwargs)
    except Exception:
        import PySide.QtGui as tmp
        return tmp.QSound(*args, **kwargs)

    return
