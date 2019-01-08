import os
from Qt import QtGui

_CACHE_ICONS = {}


def get_icon(name):
    root = os.path.dirname(__file__)
    fpn = os.path.join(root, 'imgs', name + '.png')

    key = fpn.lower()

    if key in _CACHE_ICONS:
        return _CACHE_ICONS[key]

    if not os.path.isfile(fpn):
        raise ValueError('could not find icon %s' % fpn)

    icon = QtGui.QIcon(QtGui.QPixmap(fpn, '1'))
    _CACHE_ICONS[key] = icon

    return icon
