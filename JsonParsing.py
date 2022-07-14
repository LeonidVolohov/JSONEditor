from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from collections import OrderedDict
import json
import codecs


class JsonParsing():
	def __init__(self, jsonDictinary = None):
		self.jsonDictinary = jsonDictinary

	def getJsonFromFile(self, filePath):
		with codecs.open(filePath, 'r', "utf-16") as openedFile:
			jsonData = json.load(openedFile)

		# In Json there is a property for sorting keys (sort_Keys=True (False by default)), so there is no need in this
		# return OrderedDict(sorted(jsonData.items())) 
		return jsonData

	def writeJsonToFile(self, fileLocation, jsonFile):
		with codecs.open(fileLocation, "w", "utf-16") as openedFile:
			openedFile.write(json.dumps(jsonFile, indent=2, ensure_ascii=False, sort_keys=True))
	
	def getNameFromDict(self, data):
		outputString = "Object"

		if isinstance(data, dict):
			# Add property name at the beginning
			tempDict = OrderedDict()
			tempDict["__Name__"] = data.get('name', None)
			tempDict["__Group__"] = data.get('group', None)
			tempDict["__Description__"] = data.get('description', None)
			filteredDict = {key: value for key, value in tempDict.items() if value is not None}

			tempDict.clear()
			tempDict.update(filteredDict)

			if len(tempDict) > 0:
				outputString = ";  ".join(["%s  :  %s" % (key, value) for (key, value) in tempDict.items()])
			return outputString
		if isinstance(data, list):
			pass
		if isinstance(data, tuple):
			pass


def main():
	pass

if __name__ == '__main__':
	main()
