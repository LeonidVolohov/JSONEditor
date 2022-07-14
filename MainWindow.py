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

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    # Main window components
    def UiComponents(self, jsonText): #jsonText: dict
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        self.treeView = QTreeView()
        self.pushButton = QPushButton()

        self.pushButton.setText("Print Tree to file /JsonToGUI/new.json")
        self.pushButton.clicked.connect(self.buttonClicked)

        self.model = QJsonModel()
        self.treeView.setModel(self.model)

        self.model.clear()
        self.model.load(jsonText)

        layout.addWidget(self.treeView)
        layout.addWidget(self.pushButton)

        # self.treeView.expandAll()
        # self.treeView.expandToDepth(0)

        self.setCentralWidget(widget)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())

    def buttonClicked(self):
        if self.pushButton.isChecked():
            pass
        else:
            JsonParsing().writeJsonToFile("/home/user/jsontogui/JsonToGUI/new.json", self.model.json())

def main():
    application = QApplication(sys.argv)
    mainWindow = MainWindow({"1": "1", "3": "3", "2": "2"}, showMaximized = False)
    sys.exit(application.exec_())
    

if __name__ == '__main__':
    main()
