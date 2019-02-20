import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import	QMainWindow, QLabel, QGridLayout,QWidget,QDesktopWidget, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class main_window(QMainWindow):

	def __init__(self, parent=None):
		# QMainWindow.__init__(self)
		super(main_window, self).__init__(parent)
		self.setFixedSize(QSize(840,480))
		self.setWindowTitle("EXAM SCHEDULER")
		self.center_screen()
		self.heading()	

	def heading(self):
		self.label = QLabel("EXAM SCHEDULER", self)
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setStyleSheet("color:green;font: bold 40pt 'Arial'; background-color:red")	
		self.label.resize(840,100)
		self.label.move(0,0)

	def center_screen(self):
		qr = self.frameGeometry()
		self.cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(self.cp)
		self.move(qr.topLeft())

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWin = main_window()
	mainWin.show()
	sys.exit(app.exec_())