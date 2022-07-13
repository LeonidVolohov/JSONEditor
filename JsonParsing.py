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

	def fillWidget(self, widget, data):
		widget.clear()
		self.treeFromDictionary(widget.invisibleRootItem(), data)

	def treeFromDictionary(self, parent, data):
		def newItem(position, parent, text):
			child = QTreeWidgetItem()
			child.setText(position, str(text))
			parent.addChild(child)

			return child

		if isinstance(data, dict):
			newParent = newItem(0, parent, self.getNameFromDict(data))
			# newParent = newItem(0, parent, data.keys())
			for key, value in data.items():
				subParent = newItem(0, newParent, key)
				self.treeFromDictionary(subParent, value)
		elif isinstance(data, (tuple, list)):
			for value in data:
				self.treeFromDictionary(parent, value)
		else:
			parent.setText(1, str(data)) # display value without creating a subtree
			# newItem(1, parent, data) # display value with creating a subtree
			# parent.setFlags(parent.flags() | Qt.ItemIsEditable) # Make lowest elements editable

	def treeToDictionary(self):
		pass

	def get_dict(self, tree):
		result = None

		def unpack(to_unpack, key, source=None):
			for child_index in range(to_unpack.childCount()):
				child = to_unpack.child(child_index)
				child_text = child.text(0)
				try:
					child_text = float(child_text)
				except ValueError:
					try:
						child_text = int(child_text)
					except ValueError:
						pass

				if source is None:
					core = result
				else:
					core = source

				if key == "[dict]":
					core.update({child_text: None})
					if child.childCount() > 0:
						unpack(child, child_text, core)
				elif key == "[list]" or key == "[tuple]":
					if child_text == "[dict]":
						core.append({})
					elif child_text == "[list]" or child_text == "[tuple]":
						core.append([])
					else:
						core.append(child_text)

					if child.childCount() > 0:
						unpack(child, child_text, core[child_index])
				else:
					if child_text == "[dict]":
						core.update({key: {}})
					elif child_text == "[list]" or child_text == "[tuple]":
						core.update({key: []})
					else:
						core.update({key: child_text})

					if child.childCount() > 0:
						unpack(child, child_text, core[key])

		# print(tree.topLevelItemCount())
		# print(tree.childCount())
		for index in range(tree.topLevelItemCount()):
			parent = tree.topLevelItem(index)
			element_text = parent.text(0)
			if element_text == "[dict]":
				result = {}
				unpack(parent, element_text)
			elif element_text == "[list]" or element_text == "[tuple]":
				result = []
				unpack(parent, element_text)
			else:
				result = element_text

		return result

	def getNameFromDict(self, data):
		outputString = "Object"
		tempList = []

		if isinstance(data, dict):
			tempList.append(data.get('name', None))
			tempList.append(data.get('group', None))
			tempList.append(data.get('description', None))

			# remove all None elements in list -> map all elements to str -> convert back to list for join
			tempList = list(map(str, list(filter(None, tempList))))

			if len(tempList) > 0:
				outputString = " : ".join(tempList)
			return outputString
		if isinstance(data, list):
			pass
		if isinstance(data, tuple):
			pass


def main():
	pass

if __name__ == '__main__':
	main()
