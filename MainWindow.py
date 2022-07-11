# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from JsonParsing import *

import sys


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
    def UiComponents(self, jsonText): #if QLabel - jsonText: str, if QTreeWidget - jsonText: dict
        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.treeWidget = QTreeWidget()
        #self.treeWidget.setModel(model)

        self.vbox.addWidget(self.treeWidget)
        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)
        self.setCentralWidget(self.scrollArea)

        JsonParsing().treeFromDictionary(data = jsonText, parent = self.treeWidget) # load jsonData to TreeWidget

        # TODO: scrollArea is small when app is loading. The idea is to open it on full screen 
        # self.scrollArea.resize(self.scrollArea.sizeHint())

        # For QLabel
        # self.vbox.addWidget(QLabel(jsonText))
        # self.widget.setLayout(self.vbox)
        # self.scrollArea.setWidget(self.widget)
        # self.setCentralWidget(self.scrollArea)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())


def main():
    application = QApplication(sys.argv)
    mainWindow = MainWindow("test text",    showMaximized = False)
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
