from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5

import json

from JsonParsing import *


class QJsonTreeItem(object):
	def __init__(self, data, parent=None):
		self._parent = parent

		self._key = ""
		self._value = ""
		self._type = None
		self._children = list()
		self.itemData = data

	def appendChild(self, item):
		self._children.append(item)

	def child(self, row):
		return self._children[row]

	def parent(self):
		return self._parent

	def childCount(self):
		return len(self._children)

	def columnCount(self):
		return len(self.itemData)

	def row(self):
		return (
			self._parent._children.index(self)
			if self._parent else 0
		)

	@property
	def key(self):
		return self._key

	@key.setter
	def key(self, key):
		self._key = key

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, typ):
		self._type = typ

	def data(self, column):
		if column is 0:
			return self.key
		elif column is 1:
			return self.value

	def setData(self, column, value):
		if column is 0:
			self.key = value
		if column is 1:
			self.value = value

	@classmethod
	def loadJsonToTree(self, value, parent=None, sort=True):
		rootItem = QJsonTreeItem(parent=parent, data=value)
		rootItem.key = "root"

		if isinstance(value, dict):
			items = (
				sorted(value.items())
				if sort else value.items()
			)

			for key, value in items:
				child = self.loadJsonToTree(value, rootItem)
				child.key = key
				child.type = type(value)
				rootItem.appendChild(child)

		elif isinstance(value, list):
			for index, value in enumerate(value):
				child = self.loadJsonToTree(value, rootItem)
				child.key = JsonParsing().getNameFromDict(value)
				child.type = type(value)
				rootItem.appendChild(child)

		else:
			rootItem.value = value
			rootItem.type = type(value)

		return rootItem

	def insertChildren(self, position, rows, columns):
		if position < 0 or position > len(self._children):
			return False

		for row in range(rows):
			data = [None for v in range(columns)]
			item = QJsonTreeItem(data, self)
			self._children.insert(position, item)

		return True

	def removeChildren(self, position, rows):
		if position < 0 or position + rows > len(self._children):
			return False

		for row in range(rows):
			self._children.pop(position)

		return True


class QJsonTreeModel(QAbstractItemModel):
	def __init__(self, parent=None):
		super(QJsonTreeModel, self).__init__(parent)

		# self._rootItem = QJsonTreeItem()
		self._rootItem = QJsonTreeItem(["Key", "Value"])
		self._headers = ("Key", "Value")

	def clear(self):
		self.load({})

	def load(self, document):
		"""Load from dictionary
		Arguments:
			document (dict): JSON-compatible dictionary
		"""

		assert isinstance(document, (dict, list, tuple)), (
			"`document` must be of dict, list or tuple, "
			"not %s" % type(document)
		)

		self.beginResetModel()

		self._rootItem = QJsonTreeItem.loadJsonToTree(document)
		self._rootItem.type = type(document)

		self.endResetModel()

		return True

	def data(self, index, role):
		if not index.isValid():
			return None

		if role != Qt.DisplayRole and role != Qt.EditRole:
			return None

		item = index.internalPointer()

		if role == Qt.DisplayRole or role == Qt.EditRole:
			if index.column() == 0:
				return item.data(index.column())

			if index.column() == 1:
				return item.value
		return None

	def getItem(self, index):
		if index.isValid():
			item = index.internalPointer()
			if item:
				return item

		return self._rootItem

	def setData(self, index, value, role=Qt.EditRole):
		if role == Qt.EditRole:
			item = index.internalPointer()
			item.setData(index.column(), value) # Somehow not working, need to specify directly column id
			self.dataChanged.emit(index, index, [Qt.EditRole])
			return True
		if role == Qt.DisplayRole:
			item = index.internalPointer()
			item.setData(0, "[No dict() name]")
			item.setData(1, dict())
			self.dataChanged.emit(index, index, [Qt.EditRole])
			return True
		if role == Qt.ToolTipRole:
			item = index.internalPointer()
			item.setData(0, "[No list() name]")
			item.setData(1, list())
			self.dataChanged.emit(index, index, [Qt.EditRole])
			return True
		return False

	def headerData(self, section, orientation, role):
		if role != Qt.DisplayRole:
			return None

		if orientation == Qt.Horizontal:
			return self._headers[section]

	def index(self, row, column, parent=QModelIndex()):
		if not self.hasIndex(row, column, parent):
			return QModelIndex()

		if not parent.isValid():
			parentItem = self._rootItem
		else:
			parentItem = parent.internalPointer()

		childItem = parentItem.child(row)
		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QModelIndex()

	def parent(self, index):
		if not index.isValid():
			return QModelIndex()

		childItem = index.internalPointer()
		parentItem = childItem.parent()

		if parentItem == self._rootItem:
			return QModelIndex()

		return self.createIndex(parentItem.row(), 0, parentItem)

	def rowCount(self, parent=QModelIndex()):
		if parent.column() > 0:
			return 0

		if not parent.isValid():
			parentItem = self._rootItem
		else:
			parentItem = parent.internalPointer()

		return parentItem.childCount()

	def columnCount(self, parent=QModelIndex()):
		return 2

	def flags(self, index):
		flags = super(QJsonTreeModel, self).flags(index)
		if index.column() == 0 or index.column() == 1:
			return Qt.ItemIsEditable | flags
		else:
			return flags

	def getJsonFromTree(self, root=None):
		root = root or self._rootItem
		return self.generateJsonFromTree(root)

	def generateJsonFromTree(self, item):
		numberOfChild = item.childCount()

		if item.type is dict:
			document = {}
			for i in range(numberOfChild):
				child = item.child(i)
				document[child.key] = self.generateJsonFromTree(child)
			return document
		elif item.type == list:
			document = []
			for i in range(numberOfChild):
				child = item.child(i)
				document.append(self.generateJsonFromTree(child))
			return document
		else:
			return item.value

	def insertRows(self, position, rows, parent, *args, **kwargs):
		parentItem = self.getItem(parent)
		
		self.beginInsertRows(parent, position, position + rows - 1)
		success = parentItem.insertChildren(position, rows, self._rootItem.columnCount())
		self.endInsertRows()

		return success

	def removeRows(self, position, rows, parent):
		parentItem = self.getItem(parent)

		self.beginRemoveRows(parent, position, position + rows - 1)
		success = parentItem.removeChildren(position, rows)
		self.endRemoveRows()

		return success


def main():
	model = QJsonTreeModel()

	with open("/home/user/jsontogui/pyqttest/config_apak.json") as f:
		document = json.load(f)
		model.load(document)

	# Sanity check
	assert (
		json.dumps(model.json(), sort_keys=True) ==
		json.dumps(document, sort_keys=True)
	)

if __name__ == '__main__':
	main()
	