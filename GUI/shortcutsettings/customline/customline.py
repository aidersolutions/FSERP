#creates custromised line edit entry
import sys
import time
from PySide.QtCore import *
from PySide.QtGui import *


class CustomLine(QLineEdit):
    """A customized line edit system to add shortcut keys as a string entry"""
    def keyPressEvent(self, e):
        text = self.text()
        # if int(e.modifiers()) == (int(Qt.AltModifier)+int(Qt.ControlModifier)):
        # self.setText(text+'+ CTRL + ALT' if text else 'CTRL + ALT')
        if int(e.modifiers()) == int(Qt.ControlModifier):
            self.setText(text + '+Ctrl' if text else 'Ctrl')
        elif int(e.modifiers()) == int(Qt.AltModifier):
            self.setText(text + '+Alt' if text else 'Alt')
        elif int(e.modifiers()) == int(Qt.ShiftModifier):
            self.setText(text + '+Shift' if text else 'Shift')
        elif e.key() < 257:
            self.setText(text + '+%s' % chr(e.key()) if text else '%s' % chr(e.key()))
            return
        super(CustomLine, self).keyPressEvent(e)


class Main(QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        line1 = CustomLine(self)
        line2 = CustomLine(self)
        layout = QVBoxLayout(self)
        layout.addWidget(line1)
        layout.addWidget(line2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()
