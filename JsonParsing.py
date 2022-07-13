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
