import json
import sys
import os
from configparser import ConfigParser

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

	configObject = ConfigParser()
	configObject.read("utils/config/config.ini")
	
	application = QApplication(sys.argv)
	mainWindow = MainWindow(
			jsonFileName = configObject.get("Other", "defaultjsonfilename"), 
			showMaximized = Utils().stringToBoolean(configObject.get("MainWindow", "showmaximized")))

	sys.exit(application.exec_())
