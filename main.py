import json
import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from utils.Utils import *
from utils.JsonParsing import *
from mainwindow.MainWindow import *


def main():
	pass

if __name__ == '__main__':
	main()

	jsonFileName = "config_apak.json"

	application = QApplication(sys.argv)
	mainWindow = MainWindow(jsonFileName = jsonFileName, showMaximized = False)

	sys.exit(application.exec_())
