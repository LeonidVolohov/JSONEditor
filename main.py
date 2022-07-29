"""Main module"""
import sys
from configparser import ConfigParser

from PyQt5.QtWidgets import QApplication

from utils.Utils import Utils
from mainwindow.MainWindow import MainWindow


if __name__ == '__main__':
    CONFIG_OBJECT = ConfigParser()
    CONFIG_OBJECT.read("utils/config/config.ini")

    APPLICATION = QApplication(sys.argv)
    MAIN_WINDOW = MainWindow(
        json_file_name=CONFIG_OBJECT.get("Other", "defaultjsonfilename"),
        show_maximized=Utils().string_to_boolean(CONFIG_OBJECT.get("MainWindow", "showmaximized")))

    sys.exit(APPLICATION.exec_())
