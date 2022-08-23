"""Main module."""
import sys
from argparse import ArgumentParser
from configparser import ConfigParser

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from utils.Utils import Utils
from utils.stylesheets import APPLICATION_STYLESHEET
from mainwindow.MainWindow import MainWindow


if __name__ == '__main__':
    CONFIG_OBJECT = ConfigParser()
    CONFIG_OBJECT.read(Utils().get_abs_file_path("utils/config/config.ini"))

    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file", "--filename", "--file_name",
        dest="filename",
        help="open a specific File from command line",
        metavar="FILE"
    )

    args = parser.parse_args()

    file_name = None
    if args.filename:
        file_name = args.filename
    else:
        file_name = CONFIG_OBJECT.get("Other", "default_json_file_name")

    APPLICATION = QApplication(sys.argv)
    MAIN_WINDOW = MainWindow(
        json_file_name=file_name,
        show_maximized=Utils().string_to_boolean(CONFIG_OBJECT.get("MainWindow", "show_maximized")))

    APPLICATION.setStyleSheet(APPLICATION_STYLESHEET)
    APPLICATION.setWindowIcon(QIcon("utils/images/treeview/main_window.png"))

    sys.exit(APPLICATION.exec_())
