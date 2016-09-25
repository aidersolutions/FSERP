#unused file
from testing import Ui_Dialog
from PySide.QtGui import *

class Dialog(QDialog):
	def __init__(self,parent=None):
		super(Dialog,self).__init__(parent)
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.paddingLeft=10
		self.paddingBottom=10
	
	def setParent(self, parent):
		self.updatePosition()
		return super(Dialog, self).setParent(parent)
  
	def updatePosition(self):
        
		if hasattr(self.parent(), 'viewport'):
			parentRect = self.parent().viewport().rect()
		else:
			parentRect = self.parent().rect()
            
		if not parentRect:
			return
		x = parentRect.width() - self.width() - self.paddingLeft
		y = parentRect.height() - self.height() - self.paddingBottom
		self.setGeometry(x, y, self.width(), self.height())
	def resizeEvent(self, event):
		super(Dialog, self).resizeEvent(event)
		self.updatePosition()
	def showEvent(self, event):
		self.updatePosition()
		return super(Dialog, self).showEvent(event)
class Dol(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.dia=Dialog(self)
		self.dia.show()
	def resizeEvent(self, event):
		super(Dol, self).resizeEvent(event)
		self.dia.updatePosition()

if __name__=='__main__':
	import sys
	ap=QApplication(sys.argv)
	wi=Dol()
	wi.show()
	sys.exit(ap.exec_())
