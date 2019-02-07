import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import	QMainWindow, QLabel, QGridLayout,QWidget,QDesktopWidget, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

class main_window(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		self.setFixedSize(QSize(840,480))
		self.setWindowTitle("EXAM SCHEDULER")
		self.center_screen()
		self.click_btn1()
		self.click_btn2()
		self.click_btn3()
		self.generate()
		self.textbox()

	def center_screen(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def textbox(self):
		self.textbox1 = QLineEdit(self)
		self.textbox1.move(20, 20)
		self.textbox1.resize(600,40)

		self.textbox2 = QLineEdit(self)
		self.textbox2.move(20, 80)
		self.textbox2.resize(600,40)

		self.textbox3 = QLineEdit(self)
		self.textbox3.move(20, 140)
		self.textbox3.resize(600,40)


	def click_btn1(self):
		btn1 = QPushButton("Select File", self)
		btn1.clicked.connect(self.getDirFromUserSelection)
		btn1.move(650,20)
		btn1.resize(150,40)

	def click_btn2(self):
		btn2 = QPushButton("Select File", self)
		btn2.clicked.connect(self.getDirFromUserSelection)
		btn2.move(650,80)
		btn2.resize(150,40)

	def click_btn3(self):
		btn3 = QPushButton("Select File", self)
		
		print( btn3.clicked.connect(self.getDirFromUserSelection) )
		btn3.move(650,140)
		btn3.resize(150,40)

	def generate(self):
		btn = QPushButton("Generate", self)
		btn.move(350,200)
		btn.resize(150,40)

	def getDirFromUserSelection(self):
		dir_name = str(QFileDialog.getExistingDirectory(self,"Select Directory", '/home'))
		if (len(dir_name) > 0):
			return dir_name
		else:
			return None

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWin = main_window()
	mainWin.show()
	sys.exit(app.exec_())

	# def location_on_the_screen(self):
	# 	ag = QDesktopWidget().availableGeometry()
	# 	sg = QDesktopWidget().screenGeometry()
	# 	widget = self.geometry()
	# 	x = (sg.width()/2)-420
	# 	# y = 2 * ag.height() - sg.height() - widget.height()
	# 	y = (sg.height()/2) - 240
	# 	return x,y