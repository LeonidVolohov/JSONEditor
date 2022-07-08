import json

class JsonParsing():
	def __init__(self):
		pass

	def getJsonFromFile(self, filePath):
		with open(filePath, mode='r') as openedFile:
			jsonData = json.load(openedFile)

		return jsonData


def main():
	pass

if __name__ == '__main__':
	main()
