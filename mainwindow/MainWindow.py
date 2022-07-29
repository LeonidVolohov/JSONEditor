# -*- coding: utf-8 -*-
"""This module create main window with its UI elements.

MainWindow inherited from QMainWindow.

    Typical usage example:
    ----------------------

    mainWindow = MainWindow(
            json_file_name = configObject.get("Other", "defaultjsonfilename"),
            show_maximized = Utils().string_to_boolean(configObject.get(
                "MainWindow", "showmaximized")))
"""
import sys
import gettext
from functools import partial
from configparser import ConfigParser

from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QMainWindow, QMenu,
    QMessageBox, QTreeView, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5 import uic

from utils.JsonParsing import JsonParsing
from utils.Utils import Utils
from treemodel.QJsonTreeModel import QJsonTreeModel


CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read("utils/config/config.ini")

TRANSLATE_MAINWINDOW = gettext.translation(
    domain="MainWindow",
    localedir=Utils().get_abs_file_path("utils/locale"),
    languages=[CONFIG_OBJECT.get("Language", "defaultlanguage")])
TRANSLATE_MAINWINDOW.install()

MAIN_WINDOW_FILE_NAME = Utils().get_abs_file_path("mainwindow/mainwindow.ui")


class MainWindow(QMainWindow):
    """Class to create main window.

    Attributes:
    -----------
    json_file_name:
        File name of JSON
    show_maximized:
        Show maximized or minimized window if True or False

    Methods:
    --------
    ui_components:
        Creates main components of the window

    create_menu_bar:
        Creates manu bar

    action_new_json_file:
        Action to create new an empty JSON file on the main window

    action_open_file_dialog:
        Action for opening file dialog

    action_save_json_file:
        Action for saving to file

    action_save_json_file_as:
        Action for saving file as

    action_refresh_json_file:
        Action for loading JSON from file to the main window. "Refreshing"

    action_close_application:
        Action for closing application

    open_right_click_menu:
        Action for creating on QTreeView right click menu

    tree_add_item:
        Action for adding item to QTreeView

    tree_add_item_child:
        Action for adding child item to QTreeView

    tree_item_delete:
        Action for deleting item from QTreeView

    action_tree_item_open_json_file:
        Action for opening JSON file from QTreeView if matched

    center:
        Action for centering main window
    """
    def __init__(self, json_file_name: str, show_maximized: bool=False) -> None:
        """Constructs all the necessary attributes for the QJsonTreeModel object.

        Args:
        -----
            json_file_name:
                File name of file to open it it QTreeView. Could be "".
            show_maximized:
                Show maximized or minimized MainWindow
        """
        super().__init__()

        uic.loadUi(MAIN_WINDOW_FILE_NAME, self)

        self._json_file_name = json_file_name

        if len(json_file_name) == 0:
            self.json_text = {TRANSLATE_MAINWINDOW.gettext("[No data]"):
                              TRANSLATE_MAINWINDOW.gettext("[No data]")}
        else:
            self.json_text = JsonParsing(json_file_name).get_json_from_file() # dict

        self.setWindowTitle(Utils().get_abs_file_path(json_file_name))
        #self.setGeometry(0, 0, 640, 480)
        self.resize(1024, 720)
        self.center()
        self.ui_components()
        self.create_menu_bar()

        if show_maximized:
            self.showMaximized()
        else:
            self.show()

    @property
    def model(self):
        """Get or set current model"""
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def json_text(self):
        """Get or set current json_text"""
        return self._json_text

    @json_text.setter
    def json_text(self, json_text):
        self._json_text = json_text

    @property
    def json_file_name(self):
        """Get or set current json_file_name"""
        return self._json_file_name

    @json_file_name.setter
    def json_file_name(self, json_file_name):
        self._json_file_name = json_file_name

    def ui_components(self) -> None:
        """Load all components of MainWindow.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        self.tree_view = QTreeView()

        self.model = QJsonTreeModel()
        self.tree_view.setModel(self.model)
        self.tree_view.setColumnWidth(0, 400)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_right_click_menu)

        self.tree_view.setAlternatingRowColors(
            Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView", "setalternatingrowcolors")))
        self.tree_view.setAnimated(
            Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView", "setanimated")))

        self.model.clear()
        self.model.load(self.json_text)

        layout.addWidget(self.tree_view)

        if Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView", "expandall")):
            self.tree_view.expandAll()
        if int(CONFIG_OBJECT.get("QTreeView", "expandtodepth")) >= -1:
            self.tree_view.expandToDepth(int(CONFIG_OBJECT.get("QTreeView", "expandtodepth")))

        self.setCentralWidget(widget)

    def create_menu_bar(self) -> None:
        """Creates menu bar.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        self.menuFile.setTitle(TRANSLATE_MAINWINDOW.gettext("File"))
        self.setMenuBar(self.menuBar)

        self.action_new_json.triggered.connect(self.action_new_json_file)
        self.action_new_json.setText(TRANSLATE_MAINWINDOW.gettext("New"))
        self.action_new_json.setShortcut(QKeySequence("Ctrl+N"))

        self.action_open_file.triggered.connect(self.action_open_file_dialog)
        self.action_open_file.setText(TRANSLATE_MAINWINDOW.gettext("Open"))
        self.action_open_file.setShortcut(QKeySequence("Ctrl+O"))

        self.action_save_file.triggered.connect(self.action_save_json_file)
        self.action_save_file.setText(TRANSLATE_MAINWINDOW.gettext("Save"))
        self.action_save_file.setShortcut(QKeySequence("Ctrl+S"))

        self.action_save_file_as.triggered.connect(self.action_save_json_file_as)
        self.action_save_file_as.setText(TRANSLATE_MAINWINDOW.gettext("Save As..."))
        self.action_save_file_as.setShortcut(QKeySequence("Ctrl+Shift+S"))

        self.action_refresh_file.triggered.connect(self.action_refresh_json_file)
        self.action_refresh_file.setText(TRANSLATE_MAINWINDOW.gettext("Refresh"))
        self.action_refresh_file.setShortcut(QKeySequence(Qt.Key_F5))

        self.action_close_app.triggered.connect(self.action_close_application)
        self.action_close_app.setText(TRANSLATE_MAINWINDOW.gettext("Quit"))
        self.action_close_app.setShortcut("Ctrl+Q")

    def action_new_json_file(self) -> None:
        """Creates new an empty JSON-file to QTreeView.

        Changes window title to "untilted" and loads to QTreeView model an empty dictionary

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        self.json_file_name = TRANSLATE_MAINWINDOW.gettext("untilted")
        self.setWindowTitle(self.json_file_name)
        self.model.clear()
        self.model.load({TRANSLATE_MAINWINDOW.gettext("[No data]"):
                         TRANSLATE_MAINWINDOW.gettext("[No data]")})

    def action_open_file_dialog(self) -> None:
        """Opens file dialog to for opening new JSON-file.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            TRANSLATE_MAINWINDOW.gettext("Choose Json File"),
            "",
            "Json Files (*.json)",
            options=options)
        if file_name:
            self.json_file_name = file_name
            self.model.load(JsonParsing(file_name).get_json_from_file())
            self.setWindowTitle(file_name)

    def action_save_json_file(self) -> None:
        """Saves JSON to file.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            FileNotFoundError:
                An error occured when the file is not found
            OSError:
                An error occured during opening the file
            BaseException:
                Base exception if others could not catch the exception
        """
        try:
            if self.json_file_name == "untilted" or self.json_file_name == "без названия":
                QMessageBox.about(
                    self,
                    TRANSLATE_MAINWINDOW.gettext("Error"),
                    TRANSLATE_MAINWINDOW.gettext(
                        "Failed to save file. Choose `Save As...` function."))
            else:
                JsonParsing(self.json_file_name).write_json_to_file(self.model.get_json_from_tree())
        except FileNotFoundError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "FileNotFoundError exception in action_save_json_file() function: %s") % \
                    str(exception))
        except OSError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "OSError exception in action_save_json_file() function: %s") % \
                    str(exception))
        except BaseException as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "BaseException in action_save_json_file() function: %s") % str(exception))

    def action_save_json_file_as(self) -> None:
        """Saves JSON to file as new file.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            FileNotFoundError:
                An error occured when the file is not found
            OSError:
                An error occured during opening the file
            BaseException:
                Base exception if others could not catch the exception
        """
        try:
            file_name = QFileDialog.getSaveFileName(
                self,
                TRANSLATE_MAINWINDOW.gettext("Save File"),
                "",
                "Json Files (*.json);;Text Files (*.txt);;All Files (*)")
            if Utils().file_name_match(file_name[0]):
                JsonParsing(file_name[0]).write_json_to_file(self.model.get_json_from_tree())

                # load just added file to QTreeView
                self.json_file_name = file_name[0]
                self.model.load(JsonParsing(file_name[0]).get_json_from_file())
                self.setWindowTitle(file_name[0])
            else:
                QMessageBox.about(
                    self,
                    TRANSLATE_MAINWINDOW.gettext("Error"),
                    TRANSLATE_MAINWINDOW.gettext(
                        "File does not match .json files. Name the file correctly"))
        except FileNotFoundError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "FileNotFoundError exception in action_save_json_file_as() function: %s") % \
                    str(exception))
        except OSError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "OSError exception in action_save_json_file_as() function: %s") % \
                    str(exception))
        except BaseException as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "BaseException in action_save_json_file_as() function: %s") % str(exception))

    def action_refresh_json_file(self) -> None:
        """Loads JSON form file to QTreeView.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            FileNotFoundError:
                An error occured when the file is not found
            OSError:
                An error occured during opening the file
            BaseException:
                Base exception if others could not catch the exception
        """
        try:
            if self.json_file_name == "untilted" or self.json_file_name == "без названия":
                QMessageBox.about(
                    self,
                    TRANSLATE_MAINWINDOW.gettext("Error"),
                    TRANSLATE_MAINWINDOW.gettext(
                        "Failed to save file. Choose `Save As...` function."))
            else:
                self.model.load(
                    JsonParsing(Utils().get_abs_file_path(
                        self.json_file_name)).get_json_from_file())
        except FileNotFoundError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "FileNotFoundError exception in action_refresh_json_file() function: %s") % \
                    str(exception))
        except OSError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "OSError exception in action_refresh_json_file() function: %s") % \
                    str(exception))
        except BaseException as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "BaseException in action_refresh_json_file() function: %s") % str(exception))

    def action_close_application(self) -> None:
        """Closes MainWindow application.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        sys.exit()

    def open_right_click_menu(self, position) -> None:
        """Opens right cklick menu on QTreeView items.

        Args:
        -----
            position: QtCore.QPoint
                Position of clicking

        Returns:
        --------
            None

        Raises:
        -------
            IndexError:
                When the index of clicking is out of range
            BaseException:
                When previous exception could not catch the exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index.parent()

            if not index.isValid():
                return

            right_click_menu = QMenu()
            action_add_item = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add Item")))
            action_add_item.triggered.connect(
                partial(self.tree_add_item, Qt.EditRole))

            action_add_dictionary = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add dict()")))
            action_add_dictionary.triggered.connect(
                partial(self.tree_add_item, Qt.DisplayRole))

            action_add_list = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add list()")))
            action_add_list.triggered.connect(
                partial(self.tree_add_item, Qt.ToolTipRole))

            right_click_menu.addSeparator()

            action_insert_child = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child")))
            action_insert_child.triggered.connect(
                partial(self.tree_add_item_child, Qt.EditRole))

            action_insert_child_dict = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child dict()")))
            action_insert_child_dict.triggered.connect(
                partial(self.tree_add_item_child, Qt.DisplayRole))

            action_insert_child_list = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child list()")))
            action_insert_child_list.triggered.connect(
                partial(self.tree_add_item_child, Qt.ToolTipRole))

            right_click_menu.addSeparator()

            action_delete_item = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Delete Item")))
            action_delete_item.triggered.connect(
                partial(self.tree_item_delete))

            right_click_menu.addSeparator()

            file_name = self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole)
            action_tree_item_open_json_file = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Open File")))
            action_tree_item_open_json_file.triggered.connect(
                partial(self.tree_item_open_json_file, file_name))
            action_tree_item_open_json_file.setVisible(False)

            if ((self.model.data(parent, Qt.EditRole) is None) and
                    (self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole) == "")):
                action_add_item.setVisible(True)
                action_add_dictionary.setVisible(True)
                action_add_list.setVisible(True)
                action_insert_child.setVisible(True)
                action_insert_child_dict.setVisible(True)
                action_insert_child_list.setVisible(True)
                action_delete_item.setVisible(True)
            elif self.model.data(parent, Qt.EditRole) is None:
                action_add_item.setVisible(True)
                action_add_dictionary.setVisible(True)
                action_add_list.setVisible(True)
                action_insert_child.setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_delete_item.setVisible(True)
            elif ((self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole) != "") and
                  (Utils().file_name_match(file_name))):
                action_add_item.setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_tree_item_open_json_file.setVisible(True)
                action_delete_item.setVisible(True)
            elif self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole) != "":
                action_add_item.setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_delete_item.setVisible(True)
            elif self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole) == "":
                action_add_item.setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.setVisible(True)
                action_insert_child_dict.setVisible(True)
                action_insert_child_list.setVisible(True)
                action_delete_item.setVisible(True)
            else:
                action_add_item.setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_delete_item.setVisible(True)

            right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))
        except IndexError as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "IndexError exception in open_right_click_menu() function: %s") % \
                    str(exception))
        except BaseException as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "BaseException in open_right_click_menu() function: %s") % str(exception))

    def tree_add_item(self, role: Qt.ItemDataRole) -> None:
        """Adds item to the model.

        Adding items to QTreeView depends on the input role.
        Qt.EditRole = str(), Qt.DisplayRole = dict(), Qt.ToolTipRole = list()

        Args:
        -----
            role:
                Input role

        Returns:
        --------
            None

        Raises:
        -------
            Exception:
                Basic exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index.parent()

            if self.model.data(parent, Qt.EditRole) == None:
                if not self.model.insertRow(index.row() + 1, parent):
                    return

                for column in range(self.model.columnCount(parent)):
                    child = self.model.index(index.row() + 1, column, parent)

                    if role == Qt.EditRole:
                        self.model.setData(
                            index=child,
                            value=TRANSLATE_MAINWINDOW.gettext("[No data]"),
                            role=role)
                        return
                    elif role == Qt.DisplayRole or Qt.ToolTipRole:
                        self.model.setData(index=child, value=None, role=role)
                        self.action_save_json_file()
                        self.action_refresh_json_file()
                        return
                    else:
                        return
            else:
                QMessageBox.about(
                    self,
                    TRANSLATE_MAINWINDOW.gettext("Error"),
                    TRANSLATE_MAINWINDOW.gettext(
                        "You can only use this function to root QTreeView Node, \
                        choose another actions"))
        except Exception as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "Exception in tree_add_item() function: %s") % str(exception))

    def tree_add_item_child(self, role: Qt.ItemDataRole) -> None:
        """Adds child item to the model.

        Adding child items to QTreeView depends on the input role.
        Qt.EditRole = str(), Qt.DisplayRole = dict(), Qt.ToolTipRole = list()
        When adding dict() or list() it is impossible to add them and work with them immediately
        after. Firstly it is needed to save model and only then to work with it.

        Args:
        -----
            role:
                Input role

        Returns:
        --------
            None

        Raises:
        -------
            Exception:
                Basic exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index

            if not self.model.insertRow(0, parent):
                return

            for column in range(self.model.columnCount(parent)):
                child = self.model.index(0, column, parent)
                if role == Qt.EditRole:
                    self.model.setData(
                        index=child,
                        value=TRANSLATE_MAINWINDOW.gettext("[No data]"),
                        role=role)
                    self.tree_view.expand(index)
                elif role == Qt.DisplayRole or role == Qt.ToolTipRole:
                    self.model.setData(
                        index=child,
                        value=None,
                        role=role)
                    # self.tree_view.expand(index)
                    # Only expand or save-refresh. Cant use both
                    self.action_save_json_file()
                    self.action_refresh_json_file()
        except Exception as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "Exception in tree_add_item_child() function: %s") % str(exception))

    def tree_item_delete(self) -> None:
        """Removes item from model.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            Exception:
                Basic exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index.parent()

            self.model.removeRows(
                position=index.row(),
                rows=1,
                parent=parent)
        except Exception as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "Exception in tree_item_delete() function: %s") % str(exception))

    def tree_item_open_json_file(self, file_name: str) -> None:
        """Open new window from QTreeView.

        Opens file name from QTreeView if file matches to .json file extensions.

        Args:
        -----
            file_name:
                File name

        Returns:
        --------
            None

        Raises:
        -------
            Exception:
                Basic exception
        """
        try:
            self.new_window = MainWindow(
                json_file_name=Utils().get_abs_file_path(file_name),
                show_maximized=False)
        except Exception as exception:
            QMessageBox.about(
                self,
                TRANSLATE_MAINWINDOW.gettext("Exception"),
                TRANSLATE_MAINWINDOW.gettext(
                    "Exception in tree_item_open_json_file() function: %s") % str(exception))

    def center(self):
        """Centering main window.

        Args:
        -----
            None

        Returns:
        --------
            None

        Raises:
        -------
            None
        """
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
