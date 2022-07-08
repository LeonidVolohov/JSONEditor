
# main json file --- /home/user/ProjectData/APAK

# sudo mount -o loop /home/user/distrib/Astra-1.6-Install.iso /media/mnt/   
# sudo mount -o loop /home/user/distrib/Astra-1.6-Install.iso /media/inst/
# sudo mount -o loop /home/user/distrib/Astra-1.6-devel.iso /media/inst/  
# sudo umount /media/inst 
# sudo mount -o loop /home/user/distrib/Astra-1.6-devel.iso /media/devel/

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
	jsonFileName = "config_apak.json"
	filePath = Utils().getAbsFilePath("config_apak.json")

	jsonData = JsonParsing().getJsonFromFile(filePath) # dict
	jsonDataKeys = jsonData.keys()
	jsonDataPrerryOutput = json.dumps(jsonData, indent=2, sort_keys=True) # str

	print(jsonDataPrerryOutput)


	application = QApplication(sys.argv)
	mainWindow = MainWindow(jsonText = jsonDataPrerryOutput, showMaximized = True)
	mainWindow.show()
	application.exec()
	sys.exit(application.exec_())

if __name__ == '__main__':
	main()
