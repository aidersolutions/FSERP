#unused file
from PySide.QtGui import *

class Dil(QDialog):
	def __init__(self,parent=None):
		super(Dil,self).__init__(parent)
		self.show()
		self.but=QPushButton('ok')
		self.setGeometry(0,0,100,100)
	def update_size(self):
		if hasattr(self.parent(), 'viewport'):
			parentRect = self.parent().viewport().rect()
		else:
			parentRect = self.parent().rect()
		x = parentRect.width() - self.width()
		y = parentRect.height() - self.height()
		self.setGeometry(x, y, self.width(), self.height())
	def resizeEvent(self,event):
		super(Dil,self).resizeEvent(event)
		self.update_size()


class Dol(QMainWindow,Dil):
	def __init__(self):
		QMainWindow.__init__(self)
		Dil.__init__(self,parent=self)
		self.setGeometry(0,0,300,300)
		self.wi=Dil(parent=self)
		self.wid=QPushButton(self,"push")
		self.wid.clicked.connect(lambda:self.wi.setVisible(True) if self.wi.isVisible() else self.wi.setVisible(False))
	def resizeEvent(self,event):
		super(Dol,self).resizeEvent(event)
		self.wi.update_size()
	def moveEvent(self,event):
		super(Dol,self).moveEvent(event)
		self.wi.update_size()

if __name__=='__main__':
	import sys
	ap=QApplication(sys.argv)
	d=Dol()
	d.show()
	ap.exec_()
	sys.exit(0)
