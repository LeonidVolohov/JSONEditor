from collections import OrderedDict
import json
import gettext

from utils.Utils import *


translateJsonParsing = gettext.translation(
		domain="JsonParsing", 
		localedir=Utils().getAbsFilePath("utils/locale"), 
		languages=["ru"])
translateJsonParsing.install()


class JsonParsing():
	def __init__(self, jsonDictinary = None):
		self.jsonDictinary = jsonDictinary

	def getJsonFromFile(self, filePath):
		with open(filePath, mode='r', encoding="utf-8") as openedFile:
			jsonData = json.load(openedFile)

		# In Json there is a property for sorting keys (sort_Keys=True (False by default)), so there is no need in this
		# return OrderedDict(sorted(jsonData.items())) 
		return jsonData

	def writeJsonToFile(self, fileLocation, jsonFile):
		with open(fileLocation, mode="w", encoding="utf-8") as openedFile:
			openedFile.write(json.dumps(jsonFile, indent=2, ensure_ascii=False, sort_keys=True))
	
	def getNameFromDict(self, data):
		outputString = translateJsonParsing.gettext("__Object__")

		if isinstance(data, dict):
			# Add property name at the beginning
			tempDict = OrderedDict()
			tempDict[translateJsonParsing.gettext("__Name__")] = data.get('name', None)
			tempDict[translateJsonParsing.gettext("__Group__")] = data.get('group', None)
			tempDict[translateJsonParsing.gettext("__Description__")] = data.get('description', None)
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
