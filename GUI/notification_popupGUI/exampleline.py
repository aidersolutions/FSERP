#unused file
from testing import Ui_Dialog
from PySide.QtGui import *

class Line(QLineEdit):
	def __init__(self,parent=None):
		super(Line,self).__init__(self,parent)

class Main(QMainWindow,Line):
	def __init__(self):
		QMainWindow.__init__(self)
		Line.__init__(self,parent=self)
		self.setGeometry(0,0,100,100)


if __name__=='__main__':
	import sys
	ap=QApplication(sys.argv)
	win=Main()
	win.show()
	sys.exit(ap.exec_())
