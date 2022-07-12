# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

import sys

from JsonParsing import *


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
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Propery", "Value"])
        # self.treeWidget.itemDoubleClicked.connect(JsonParsing().editItem)

        self.vbox.addWidget(self.treeWidget)
        self.widget.setLayout(self.vbox)

        self.setCentralWidget(self.treeWidget)

        JsonParsing().fillWidget(widget = self.treeWidget, data = jsonText)

        # self.treeWidget.expandAll()
        self.treeWidget.expandToDepth(1)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())


def main():
    application = QApplication(sys.argv)
    mainWindow = MainWindow("test text", showMaximized = False)
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
