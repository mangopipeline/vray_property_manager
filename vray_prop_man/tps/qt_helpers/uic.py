import __future__

from cStringIO import StringIO


from Qt import QtGui, QtCore, QtWidgets
import xml.etree.ElementTree as xml


try:
    import pyside2uic as uic
except ImportError:
    import pysideuic as uic


def load_ui_type(ui_file):
    """
    Pyside "load_ui_type" command like PyQt4 has one, so we have to convert the 
    ui file to py code in-memory first and then execute it in a special frame
    to retrieve the form_class.
    """

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type
        # in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('QtWidgets.%s' % widget_class)

    return base_class, form_class
