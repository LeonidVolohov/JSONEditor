import json
from collections import OrderedDict

from PyQt5.QtWidgets import *

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

	def editItem(self):
		pass

	def treeFromDictionary(self, data = None, parent = None):
		for key, value in data.items():
			item = QTreeWidgetItem(parent)
			item.setText(0, key)

			if isinstance(value, dict):
				self.treeFromDictionary(data = value, parent = item)
			elif isinstance(value, list):
				for idx, i in enumerate(value):
					if idx != 0:
						item = QTreeWidgetItem(parent)
						item.setText(0, key)
					self.treeFromDictionary(i, parent = item)
			else:
				item.setText(1, str(value))

	def treeToDictionary(self):
		pass


def main():
	pass

if __name__ == '__main__':
	main()
