from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from collections import OrderedDict
import json


class JsonParsing():
	def __init__(self, jsonDictinary = None):
		self.jsonDictinary = jsonDictinary

	def getJsonFromFile(self, filePath):
		with open(filePath, mode='r') as openedFile:
			jsonData = json.load(openedFile)

		# return jsonData
		return OrderedDict(sorted(jsonData.items()))

	def saveChanges(self):
		pass

	# TODO: Currenctly not working
	def editItem(self, item, column):
		try:
			if column == 1:
				item.setFlags(item.flags() | Qt.ItemIsEditable)
			else:
				pass
		except Exception as exception:
			print(exception)

	def treeFromDictionary1(self, data = None, parent = None):
		# Working but wrong tree node
		for key, value in data.items():
			item = QTreeWidgetItem(parent)
			item.setText(0, key)
			if isinstance(value, dict):
				self.treeFromDictionary1(data = value, parent = item)
			elif isinstance(value, list):
				for idx, i in enumerate(value):
					if idx != 0:
						item = QTreeWidgetItem(parent)
						item.setText(0, key)
					self.treeFromDictionary1(i, parent = item)
			else:
				item.setText(1, str(value))

		# Not workig 
		# if type(data) is dict:
		# 	for key, value in sorted(data.items()):
		# 		print("is dict")
		# 		child = QTreeWidgetItem()
		# 		child.setText(0, key)
		# 		parent.addChild(child)
		# 		self.treeFromDictionary(child, value)
		# elif type(data) is list:
		# 	for value in data:
		# 		child = QTreeWidgetItem()
		# 		parent.addChild(child)
		# 		if type(value) is dict:
		# 			child.setText(0, 'dict')
		# 			self.treeFromDictionary(child, value)
		# 		elif type(value) is list:
		# 			child.setText(0, 'list')
		# 			self.treeFromDictionary(child, value)
		# 		else:
		# 			child.setText(0, value)
		# 		child.setExpanded(True)
		# else:
		# 	child = QTreeWidgetItem()
		# 	child.setText(0, data)
		# 	parent.addChild(child)

	def fillWidget(self, widget, data):
		widget.clear()
		self.treeFromDictionary(widget.invisibleRootItem(), data)

	def treeFromDictionary(self, parent, data):
		def newItem(position, parent, text):
			# child = QTreeWidgetItem([str(text)])
			child = QTreeWidgetItem()
			child.setText(position, str(text))
			
			#if not isinstance(text, (dict, list, tuple)):
			if text not in ("[dict]", "[list]", "[tuple]"):
				child.setFlags(child.flags() | Qt.ItemIsEditable)
			parent.addChild(child)

			return child

		if isinstance(data, dict):
			newParent = newItem(0, parent, self.getNameFromDict(data))
			# newParent = newItem(0, parent, data.keys())
			for key, value in data.items():
				subParent = newItem(0, newParent, key)
				self.treeFromDictionary(subParent, value)
		elif isinstance(data, (tuple, list)):
			# newParent = newItem(0, parent, data) # - old version
			for value in data:
				# self.treeFromDictionary(newParent, value) # - old version
				self.treeFromDictionary(parent, value)
		else:
			parent.setText(1, str(data)) # display value without creating a subtree
			# newItem(1, parent, data) # display value with creating a subtree

		# if isinstance(data, dict):
		# 	newParent = newItem(parent, data.keys())
		# 	for key, value in data.items():
		# 		subParent = newItem(newParent, key)
		# 		self.treeFromDictionary(subParent, value)
		# elif isinstance(data, (tuple, list)):
		# 	newParent = newItem(parent, data)
		# 	for value in data:
		# 		self.treeFromDictionary(newParent, value)
		# else:
		# 	newItem(parent, data)

	def treeToDictionary(self):
		pass

	def getNameFromDict(self, data):
		outputString = ""
		tempList = []

		if isinstance(data, dict):
			tempList.append(data.get('id', None))
			tempList.append(data.get('name', None))

			# remove all None elements in list -> map all elements to str -> convert back to list for join
			tempList = list(map(str, list(filter(None, tempList))))

			if len(tempList) > 0:
				outputString = " : ".join(tempList)
				return outputString
			else:
				return list(data.keys())
		if isinstance(data, list):
			pass
		if isinstance(data, tuple):
			pass

		return data.keys()


def main():
	pass

if __name__ == '__main__':
	main()
