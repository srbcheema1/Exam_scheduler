import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout,QWidget,QDesktopWidget, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#developer window
class second_window(QDialog):
	def __init__(self, parent=None):
		super(second_window, self).__init__(parent)
		self.setWindowTitle("Developer")
		self.setFixedSize(QSize(400,80))

		self.namelabel1 = QLabel("Sarbjit Cheema (srbcheema2@gmail.com) ", self)
		self.namelabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.namelabel1.setAlignment(Qt.AlignCenter)
		self.namelabel2 = QLabel("Rakesh Kumar (rakekum34@gmail.com)", self)
		self.namelabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.namelabel2.setAlignment(Qt.AlignCenter)

		#vertical box layout
		vbox = QVBoxLayout()
		vbox.addWidget(self.namelabel1)
		vbox.addStretch(0.1)
		vbox.addWidget(self.namelabel2)
		self.setLayout(vbox)

# Main window
class Window(QDialog):
	def __init__(self, parent=None):
		# QMainWindow.__init__(self)
		super(Window, self).__init__(parent)
		self.title = "Exam Scheduler"
		self.InitWindow()

	def InitWindow(self):
		self.setWindowIcon(QIcon('icon.png'))
		self.setWindowTitle(self.title)
		self.setFixedSize(QSize(840,480))
		self.Main_Layouts()
		self.center_screen()

		vBox = QVBoxLayout()
		vBox.addWidget(self.Mainlabel)
		vBox.addSpacing(-140)
		# vBox.insertSpacing(0,20)
		vBox.addLayout(self.hBoxlayout)
		vBox.addSpacing(40)
		vBox.addLayout(self.genbtnHBox)
		vBox.addSpacing(20)
		vBox.addLayout(self.lastbar_hboxlayout)
		self.setLayout(vBox)
		self.developer_window = second_window(self)
		self.show()

	# function for set main window at center of screen
	def center_screen(self):
		qr = self.frameGeometry()
		self.cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(self.cp)
		self.move(qr.topLeft())

	def Main_Layouts(self):
		self.hBoxlayout = QHBoxLayout()

		# Heading Label
		self.Mainlabel = QLabel("EXAM SCHEDULER", self)
		# self.Mainlabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.Mainlabel.setAlignment(Qt.AlignCenter)
		self.Mainlabel.setStyleSheet("color:green;font: bold 40pt 'Courier'; background-color:#ED764D")

		label_name = ['Room list','Schedule List','Teacher List']
		for i in range(3):
			vBoxlayout = QVBoxLayout()
			label = QLabel("Select "+(label_name[i] if i < len(label_name) else 'extra'), self)
			label.setStyleSheet("font: bold 12pt 'Courier'")
			label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			label.setAlignment(Qt.AlignCenter)
			button = QPushButton()
			button.setStyleSheet("font : 'Arial'; color:red; border :1px solid black; background-image: url(bckgrng.png)")
			button.setAutoFillBackground(True)
			button.setMaximumSize(QtCore.QSize(120,150))
			button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
			button.clicked.connect(self.choose_file)
			btnHBox = QHBoxLayout()
			btnHBox.addWidget(button)
			vBoxlayout.addWidget(label)
			vBoxlayout.addSpacing(-160)
			vBoxlayout.addLayout(btnHBox)
			self.hBoxlayout.addLayout(vBoxlayout)
		
		self.genbtnHBox = QHBoxLayout()
		genrate_btn = QPushButton("Generate", self)
		genrate_btn.setMaximumSize(QtCore.QSize(500,80))
		genrate_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		self.genbtnHBox.addWidget(genrate_btn)
		genrate_btn.clicked.connect(self.generate_btn_fun)

		self.lastbar_hboxlayout = QHBoxLayout()
		developer_label = QLabel("Developer    ", self)
		developer_label.setStyleSheet("color:blue;font: bold 12pt 'Courier'")
		developer_label.mouseReleaseEvent = self.developer_fun
		sourcecode_label = QLabel("Source Code", self)
		sourcecode_label.setStyleSheet("color:blue;font: bold 12pt 'Courier'")
		urlLink="<a href=\"https://github.com/srbcheema1/Exam_scheduler\">Source Code</a>" 
		sourcecode_label.linkActivated.connect(self.link)
		sourcecode_label.setText(urlLink)

		self.lastbar_hboxlayout.addStretch(1)
		self.lastbar_hboxlayout.addWidget(developer_label)
		self.lastbar_hboxlayout.addWidget(sourcecode_label)


	def link(self, linkStr):
		QDesktopServices.openUrl(QUrl(linkStr))

	def developer_fun(self, event):
		self.developer_window.show()

	def generate_btn_fun(self):
		QMessageBox.information(self, "Exam Scheduler", "File Succesfully Generated")

	def choose_file(self):
		self.file_name = QFileDialog.getOpenFileName(self, "Select File", './','Excel Files(*.xls *.xlsb *.xlsx)')
	
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())