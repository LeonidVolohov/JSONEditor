# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys

from JsonParsing import *
from QJsonModel import *


mainWindowFileName = "mainwindow.ui"

class MainWindow(QMainWindow):
    def __init__(self, jsonText, showMaximized = False):
        super().__init__()

        uic.loadUi(mainWindowFileName, self)

        self.jsonText = jsonText

        self.setWindowTitle("JsonToGUI")
        #self.setGeometry(0, 0, 640, 480)
        self.resize(1024, 720)
        self.center()
        self.UiComponents(jsonText)

        if(showMaximized):
            self.showMaximized()
        else:
            self.show()

    # Main window components
    def UiComponents(self, jsonText): #jsonText: dict
        self.treeView = QTreeView()

        model = QJsonModel()
        self.treeView.setModel(model)

        model.clear()
        model.load(jsonText)

        # self.treeView.expandAll()
        # self.treeView.expandToDepth(0)

        self.setCentralWidget(self.treeView)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())


def main():
    application = QApplication(sys.argv)
    mainWindow = MainWindow({"1": "1", "3": "3", "2": "2"}, showMaximized = False)
    sys.exit(application.exec_())
    

if __name__ == '__main__':
    main()
