import os
import re


class Utils():
	def __init__(self):
		pass

	def getAbsFilePath(self, fileName):
		try:
			scriptPath = os.path.abspath(__file__) 			# ../JsonToGUI/utils/JsonParsing.py
			scriptDir = os.path.split(scriptPath)[0] 		# ../JsonToGUI/utils/
			scriptDir = os.path.dirname(scriptDir) 			# ../JsonToGUI/
			absFilePath = os.path.join(scriptDir, fileName)

			return absFilePath
		except Exception as exception:
			return str(exception)

	def fileNameMatch(self, fileName):
		try:
			return True if re.search("\.json$", fileName) else False
		except Exception as exception:
			return False

		return False

	def stringToBoolean(self, string):
		if(string == "True"):
			return True
		else:
			return False


def main():
	print(Utils().getAbsFilePath("config_apak.json"))
	print(Utils().getAbsFilePath("QJsonTreeModel.py"))
	print(Utils().getAbsFilePath("utils/locale"))

if __name__ == '__main__':
	main()
