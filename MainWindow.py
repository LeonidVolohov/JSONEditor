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
		try:
			JsonParsing().writeJsonToFile(self.jsonFileName, self.model.getJsonFromTree())
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in menuBarActionSave() function: " + str(exception))	
			return

	def menuBarActionRefresh(self):
		try:
			self.model.load(JsonParsing().getJsonFromFile(Utils().getAbsFilePath(self.jsonFileName)))
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in menuBarActionRefresh() function: " + str(exception))	
			return

	def menuBarActionClose(self):
		sys.exit()

	def openRightClickMenu(self, position):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index.parent()

			if not index.isValid():
				return

			rightClickMenu = QMenu()			
			actionAddItem = rightClickMenu.addAction(self.tr("Add Item"))
			actionAddItem.triggered.connect(partial(self.treeAddItem))

			actionAddDictionary = rightClickMenu.addAction(self.tr("Add dict()"))
			actionAddDictionary.triggered.connect(partial(self.treeAddDictionary))

			actionAddList = rightClickMenu.addAction(self.tr("Add list()"))
			actionAddList.triggered.connect(partial(self.treeAddList))

			rightClickMenu.addSeparator()

			actionInsertChild = rightClickMenu.addAction(self.tr("Insert Child"))
			actionInsertChild.triggered.connect(partial(self.treeAddItemChild))

			actionInsertChildDict = rightClickMenu.addAction(self.tr("Insert Child dict()"))
			actionInsertChildDict.triggered.connect(partial(self.treeAddItemChildDict))

			actionInsertChildList = rightClickMenu.addAction(self.tr("Insert Child list()"))
			actionInsertChildList.triggered.connect(partial(self.treeAddItemChildList))

			rightClickMenu.addSeparator()

			actionDeleteItem = rightClickMenu.addAction(self.tr("Delete Item"))
			actionDeleteItem.triggered.connect(partial(self.treeItemDelete))

			rightClickMenu.addSeparator()			

			fileName = self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole)
			actionTreeItemOpenJsonFile = rightClickMenu.addAction(self.tr("Open File"))
			actionTreeItemOpenJsonFile.triggered.connect(partial(self.treeItemOpenJsonFile, fileName))
			actionTreeItemOpenJsonFile.setVisible(False)

			# if ((self.model.data(parent, Qt.EditRole) == None) and 
			# 	(self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) == "")):
			# 	actionAddItem.setVisible(True)
			# 	actionInsertChild.setVisible(True)
			# 	actionDeleteItem.setVisible(True)		
			# elif self.model.data(parent, Qt.EditRole) == None:
			# 	actionAddItem.setVisible(True)
			# 	actionInsertChild.setVisible(False)
			# 	actionDeleteItem.setVisible(True)
			# elif ((self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) != "") and 
			# 		(Utils().fileNameMatch(fileName))):
			# 	actionAddItem.setVisible(False)
			# 	actionInsertChild.setVisible(False)
			# 	actionTreeItemOpenJsonFile.setVisible(True)
			# 	actionDeleteItem.setVisible(True)
			# elif (self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) != ""):
			# 	actionAddItem.setVisible(False)
			# 	actionInsertChild.setVisible(False)
			# 	actionDeleteItem.setVisible(True)
			# elif (self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) == ""):
			# 	actionAddItem.setVisible(False)
			# 	actionInsertChild.setVisible(True)
			# 	actionDeleteItem.setVisible(True)
			# else:
			# 	actionAddItem.setVisible(False)
			# 	actionInsertChild.setVisible(False)
			# 	actionDeleteItem.setVisible(True)

			rightClickMenu.exec_(self.sender().viewport().mapToGlobal(position))
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in openRightClickMenu() function: " + str(exception))	
			return

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
			QMessageBox.about(self, "Exception", "Exception in treeAddItem() function: " + str(exception))	
			return

	def treeAddDictionary(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index.parent()

			if self.model.data(parent, Qt.EditRole) == None:
				if not self.model.insertRow(index.row() + 1, parent):
					return

				for column in range(self.model.columnCount(parent)):
					child = self.model.index(index.row() + 1, column, parent)
					self.model.setData(child, "[No data]", Qt.DisplayRole)
			else:
				QMessageBox.about(self, "Error", 
					"You can only use this function to root QTreeView Node")
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeAddItem() function: " + str(exception))	
			return

	def treeAddList(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index.parent()

			if self.model.data(parent, Qt.EditRole) == None:
				if not self.model.insertRow(index.row() + 1, parent):
					return

				for column in range(self.model.columnCount(parent)):
					child = self.model.index(index.row() + 1, column, parent)
					self.model.setData(child, "[No data]", Qt.ToolTipRole)
			else:
				QMessageBox.about(self, "Error", 
					"You can only use this function to root QTreeView Node")
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeAddItem() function: " + str(exception))	
			return

	def treeAddItemChild(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index

			if not self.model.insertRow(0, parent):
				return

			for column in range(self.model.columnCount(parent)):
				child = self.model.index(0, column, parent)
				self.model.setData(child, "[No data]", Qt.EditRole)

			# if(self.model.data(self.treeView.selectedIndexes()[1], Qt.EditRole) == ""):
			# 	if not self.model.insertRow(0, parent):
			# 		return

			# 	for column in range(self.model.columnCount(parent)):
			# 		child = self.model.index(0, column, parent)
			# 		self.model.setData(child, "[No data]", Qt.EditRole)
			# else:
			# 	QMessageBox.about(self, "Error", 
			# 		"Can`t create subnode to str() value. Create list() or dict() directly from .json file")
			# 	return
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeAddItemChild() function: " + str(exception))	
			return

	def treeAddItemChildDict(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index

			if not self.model.insertRow(0, parent):
				return

			for column in range(self.model.columnCount(parent)):
				child = self.model.index(0, column, parent)
				self.model.setData(child, "[No data]", Qt.DisplayRole)
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeAddItemChild() function: " + str(exception))	
			return

	def treeAddItemChildList(self):
		try:
			index = self.treeView.selectionModel().currentIndex()
			parent = index

			if not self.model.insertRow(0, parent):
				return

			for column in range(self.model.columnCount(parent)):
				child = self.model.index(0, column, parent)
				self.model.setData(child, "[No data]", Qt.ToolTipRole)
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeAddItemChild() function: " + str(exception))	
			return

	def treeItemDelete(self):
		try:			
			index = self.treeView.selectionModel().currentIndex()
			parent = index.parent()

			self.model.removeRows(position=index.row(), rows=1, parent=parent)	
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeItemDelete() function: " + str(exception))	
			return

	def treeItemOpenJsonFile(self, fileName):
		try:			
			self.newWindow = MainWindow(jsonFileName = Utils().getAbsFilePath(fileName), showMaximized = False)
		except Exception as exception:
			QMessageBox.about(self, "Exception", "Exception in treeItemOpenJsonFile() function: " + str(exception))	
			return	

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
