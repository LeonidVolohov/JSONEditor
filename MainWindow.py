# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

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
    def UiComponents(self, jsonText):
        # jsonLabel = QLabel(self)
        # jsonLabel.setText(jsonText)
        # jsonLabel.resize(jsonLabel.sizeHint())


        self.scrollArea = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        #self.vbox.addWidget(self.label.setText(jsonText))

        self.vbox.addWidget(QLabel(jsonText))

        self.widget.setLayout(self.vbox)

        self.scrollArea.setWidget(self.widget)

        self.setCentralWidget(self.scrollArea)

        # layout = QVBoxLayout(self)
        # layout.addWidget(self.scrollArea)

        # self.label.setText(jsonText)
        # self.label.resize(self.label.sizeHint())

        # layout.addWidget(self.label)


        # jsonLabel = ScrollLabel(self)
        # jsonLabel.setText(jsonText)
        # jsonLabel.resize(jsonLabel.sizeHint())

    def center(self):
        frameGeometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeometry.moveCenter(centerPoint)
        self.move(frameGeometry.topLeft())

class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        layout = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop | Qt.AlignBottom)
        self.label.setWordWrap(True)

        layout.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)
        #self.label.resize(self.sizeHint())


def main():
    application = QApplication(sys.argv)

    mainWindow = MainWindow("test text",    showMaximized = False)

    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
