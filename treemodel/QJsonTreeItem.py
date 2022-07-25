import gettext
import sys

sys.path.insert(1, "..")
from utils.JsonParsing import *


translateQJsonTreeItem = gettext.translation(
		domain="QJsonTreeModel", 
		localedir=Utils().getAbsFilePath("utils/locale"), 
		languages=["ru"])
translateQJsonTreeItem.install()


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
				child.key = translateQJsonTreeItem.gettext(key)
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


def main():
	pass

if __name__ == '__main__':
	main()
