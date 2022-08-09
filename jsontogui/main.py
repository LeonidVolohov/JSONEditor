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
        json_file_name=CONFIG_OBJECT.get("Other", "default_json_file_name"),
        show_maximized=Utils().string_to_boolean(CONFIG_OBJECT.get("MainWindow", "show_maximized")))

    APPLICATION.setStyleSheet("""
        QHeaderView::section {
            /* background-color: #678DB2; */
            color: black;
            height: 28px;
            font-size: 16px;
            font-family: courier;
        }
    """)

    sys.exit(APPLICATION.exec_())
