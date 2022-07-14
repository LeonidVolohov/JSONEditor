import json
import sys
import os

from Utils import *
from JsonParsing import *
from MainWindow import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def main():
	pass

if __name__ == '__main__':
	main()

	jsonFileName = "jsons/config_apak.json"
	filePath = Utils().getAbsFilePath(jsonFileName)

	jsonData = JsonParsing().getJsonFromFile(filePath) # dict
	jsonDataPrerryOutput = json.dumps(jsonData, indent=2, sort_keys=True) # str

	application = QApplication(sys.argv)
	mainWindow = MainWindow(jsonText = jsonData, showMaximized = False)

	sys.exit(application.exec_())
