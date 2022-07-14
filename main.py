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

	jsonFileName = "config_apak.json"
	
	application = QApplication(sys.argv)
	mainWindow = MainWindow(jsonFileName = jsonFileName, showMaximized = False)

	sys.exit(application.exec_())
