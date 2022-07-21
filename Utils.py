import os
import re

class Utils():
	def __init__(self):
		pass

	def getAbsFilePath(self, fileName):
		try:
			scriptPath = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
			scriptDir = os.path.split(scriptPath)[0] #i.e. /path/to/dir/
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


def main():
	print(Utils().getAbsFilePath("jsons/config_apak.json"))

if __name__ == '__main__':
	main()
