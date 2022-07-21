# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys
from functools import partial

from JsonParsing import *
from QJsonTreeModel import *
from Utils import *


mainWindowFileName = "mainwindow.ui"

class MainWindow(QMainWindow):
	def __init__(self, jsonFileName, showMaximized = False):
		super().__init__()

		uic.loadUi(mainWindowFileName, self)

		self._jsonFileName = jsonFileName

		if len(jsonFileName) == 0:
			self.jsonText = {}
		else:
			self.jsonText = JsonParsing().getJsonFromFile(Utils().getAbsFilePath(jsonFileName)) # dict

		self.setWindowTitle(Utils().getAbsFilePath(jsonFileName))
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

	@property
	def jsonFileName(self):
		return self._jsonFileName

	@jsonFileName.setter
	def jsonFileName(self, jsonFileName):
		self._jsonFileName = jsonFileName
	
	# Main window components
	def UiComponents(self): #jsonText: dict
		widget = QWidget(self)
		layout = QVBoxLayout(widget)

		self.treeView = QTreeView()

		self.model = QJsonTreeModel()
		self.treeView.setModel(self.model)
		self.treeView.setColumnWidth(0, 400)
		self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.treeView.customContextMenuRequested.connect(self.openRightClickMenu)

		self.treeView.setAlternatingRowColors(False)
		self.treeView.setAnimated(False)

		self.model.clear()
		self.model.load(self.jsonText)

		layout.addWidget(self.treeView)

		# self.treeView.expandAll()
		# self.treeView.expandToDepth(0)

		self.setCentralWidget(widget)

	def createMenuBar(self):
		self.setMenuBar(self.menuBar)

		self.actionOpen.triggered.connect(self.menuBarActionOpen)
		self.actionOpen.setShortcut(QKeySequence("Ctrl+O"))
		self.actionSave.triggered.connect(self.menuBarActionSave)
		self.actionSave.setShortcut(QKeySequence("Ctrl+S"))
		self.actionRefresh.triggered.connect(self.menuBarActionRefresh)
		self.actionRefresh.setShortcut(QKeySequence(Qt.Key_F5))
		self.actionClose.triggered.connect(self.menuBarActionClose)
		self.actionClose.setShortcut("Ctrl+Q")

	def menuBarActionOpen(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Choose Json File", "","Json Files (*.json)", options=options)
		if fileName:
			self.jsonFileName = fileName
			self.model.load(JsonParsing().getJsonFromFile(fileName))
			self.setWindowTitle(fileName)

	def menuBarActionSave(self):
		JsonParsing().writeJsonToFile(self.jsonFileName, self.model.getJsonFromTree())

	def menuBarActionRefresh(self):
		self.model.load(JsonParsing().getJsonFromFile(Utils().getAbsFilePath(self.jsonFileName)))

	def menuBarActionClose(self):
		sys.exit()

	def openRightClickMenu(self, position):
		indexes = self.sender().selectedIndexes()
		mdlIdx = self.treeView.indexAt(position)
		parent = self.model.parent(mdlIdx)	
		if not mdlIdx.isValid():
			return
		# item = self.model.itemFromIndex(mdlIdx)
		item = self.model.data(mdlIdx, Qt.EditRole)
		if len(indexes) > 0:
			level = 0
			index = indexes[0]
			while index.parent().isValid():
				index = index.parent()
				level += 1
		else:
			level = 0
		right_click_menu = QMenu()
		act_add = right_click_menu.addAction(self.tr("Add Item"))
		act_add.triggered.connect(partial(self.treeAddItem))

		# if item.parent() != None:
		if self.model.parent(mdlIdx) != None:
			insert_child = right_click_menu.addAction(self.tr("Insert Child"))
			insert_child.triggered.connect(partial(self.treeAddItemChild))

			insert_up = right_click_menu.addAction(self.tr("Insert Item Above"))
			insert_up.triggered.connect(partial(self.treeItemInsertUp))

			insert_down = right_click_menu.addAction(self.tr("Insert Item Below"))
			insert_down.triggered.connect(partial(self.treeItemInsertDown, level, mdlIdx))

			act_del = right_click_menu.addAction(self.tr("Delete Item"))
			act_del.triggered.connect(partial(self.treeItemDelete))
		right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

	def treeAddItem(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index.parent()

			if self.model.data(parent, Qt.EditRole) == None:
				if not self.model.insertRow(index.row() + 1, parent):
					return

				for column in range(self.model.columnCount(parent)):
					child = self.model.index(index.row() + 1, column, parent)
					self.model.setData(child, "[No data]", Qt.EditRole)
			else:
				QMessageBox.about(self, "Error", 
					"You can only use this function to root QTreeView Node")
		except Exception as exception:
			print("Exception in treeAddItem() function: ", str(exception))
			QMessageBox.about(self, "Error", str(exception))	
			return

	def treeAddItemChild(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index

			if(self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) == ""):
				if not self.model.insertRow(0, parent):
					return

				for column in range(self.model.columnCount(parent)):
					child = self.model.index(0, column, parent)
					self.model.setData(child, "[No data]", Qt.EditRole)
			else:
				QMessageBox.about(self, "Error", 
					"Can`t create subnode to str() value. Create list() or dict() directly from .json file")
				return
		except Exception as exception:
			print("Exception in treeAddItemChild() function: ", str(exception))
			QMessageBox.about(self, "Error", str(exception))	
			return

	def treeItemInsertUp(self):
		pass

	def treeItemInsertDown(self):
		pass

	def treeItemDelete(self):
		index = self.treeView.selectionModel().currentIndex()
		parent = index.parent()

		self.model.removeRows(position=index.row(), rows=1, parent=parent)	

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
