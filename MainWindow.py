# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys

from JsonParsing import *
from QJsonModel import *
from Utils import *


mainWindowFileName = "mainwindow.ui"

class MainWindow(QMainWindow):
	def __init__(self, jsonText, showMaximized = False):
		super().__init__()

		uic.loadUi(mainWindowFileName, self)

		self._jsonText = jsonText

		self.setWindowTitle("JsonToGUI")
		#self.setGeometry(0, 0, 640, 480)
		self.resize(1024, 720)
		self.center()
		self.UiComponents()
		self.createMenuBar()

		if(showMaximized):
			self.showMaximized()
		else:
			self.show()

	@property
	def model(self):
		return self._model

	@model.setter
	def model(self, model):
		self._model = model

	@property
	def jsonText(self):
		return self._jsonText

	@jsonText.setter
	def jsonText(self, jsonText):
		self._jsonText = jsonText
	
	# Main window components
	def UiComponents(self): #jsonText: dict
		widget = QWidget(self)
		layout = QVBoxLayout(widget)

		self.treeView = QTreeView()

		self.model = QJsonModel()
		self.treeView.setModel(self.model)

		self.model.clear()
		self.model.load(self.jsonText)

		layout.addWidget(self.treeView)

		# self.treeView.expandAll()
		# self.treeView.expandToDepth(0)

		self.setCentralWidget(widget)

	def createMenuBar(self):
		self.setMenuBar(self.menuBar)

		self.actionOpen.triggered.connect(self.menuBarActionOpen)
		self.actionSave.triggered.connect(self.menuBarActionSave)
		self.actionRefresh.triggered.connect(self.menuBarActionRefresh)
		self.actionClose.triggered.connect(self.menuBarActionClose)

	def menuBarActionOpen(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Json Files (*.json)", options=options)
		if fileName:
			self.model.load(JsonParsing().getJsonFromFile(fileName))

	def menuBarActionSave(self):
		JsonParsing().writeJsonToFile("/home/user/jsontogui/JsonToGUI/config_apak.json", self.model.json())

	def menuBarActionRefresh(self):
		self.model.load(JsonParsing().getJsonFromFile(Utils().getAbsFilePath("config_apak.json")))

	def menuBarActionClose(self):
		sys.exit()

	def center(self):
		frameGeometry = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGeometry.moveCenter(centerPoint)
		self.move(frameGeometry.topLeft())


def main():
	application = QApplication(sys.argv)
	mainWindow = MainWindow({"1": "1", "3": "3", "2": "2"}, showMaximized = False)
	sys.exit(application.exec_())
	

if __name__ == '__main__':
	main()
