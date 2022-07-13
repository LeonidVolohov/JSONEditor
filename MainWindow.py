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
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        self.treeView = QTreeView()
        # self.treeView.setColumnCount(2)
        # self.treeView.setHeaderLabels(["Propery", "Value"])
        
        # self.treeView.itemDoubleClicked.connect(self.editItem)

        model = QJsonModel()
        self.treeView.setModel(model)
        model.clear()
        model.load(jsonText)

        self.vbox.addWidget(self.treeView)
        self.widget.setLayout(self.vbox)

        self.setCentralWidget(self.treeView)

        # JsonParsing().fillWidget(widget = self.treeView, data = jsonText)

        # self.treeView.expandAll()
        # self.treeView.expandToDepth(0)

        # print(JsonParsing().get_dict(self.treeView))

    def editItem(self, item, column):
        try:
            if column == 1:
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            else:
                pass
        except Exception as exception:
            print(exception)

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())


def main():
    application = QApplication(sys.argv)
    mainWindow = MainWindow("test text", showMaximized = False)
    application.exec()
    # sys.exit(application.exec_())
    # sys.exit()


if __name__ == '__main__':
    main()
