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
import os
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
from utils.stylesheets import QTREEVIEW_STYLESHEET
from treemodel.QJsonTreeModel import QJsonTreeModel


CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read(Utils().get_abs_file_path("utils/config/config.ini"))

TRANSLATE_MAINWINDOW = gettext.translation(
    domain="MainWindow",
    localedir=Utils().get_abs_file_path("utils/locale"),
    languages=[CONFIG_OBJECT.get("Language", "default_gui_language")])
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
    closeEvent:
        Close event for QMainWindow
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
    action_change_flags:
        Changes opportunity for editing item
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
            json_file_name: str
                File name of file to open it it QTreeView. Could be "".
            show_maximized: bool
                Show maximized or minimized MainWindow
        """
        super().__init__()

        uic.loadUi(MAIN_WINDOW_FILE_NAME, self)

        self._json_file_name = json_file_name
        self._model = None
        self.new_window = None

        if len(json_file_name) == 0:
            self._json_text = {TRANSLATE_MAINWINDOW.gettext("[No data]"):
                               TRANSLATE_MAINWINDOW.gettext("[No data]")}
            self.setWindowTitle(TRANSLATE_MAINWINDOW.gettext("untilted"))
        else:
            self._json_text = JsonParsing().get_json_from_file(json_file_name) # dict
            self.setWindowTitle(Utils().get_abs_file_path(self.json_file_name))

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
        """Get or set current model."""
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def json_text(self):
        """Get or set current json_text."""
        return self._json_text

    @json_text.setter
    def json_text(self, json_text):
        self._json_text = json_text

    @property
    def json_file_name(self):
        """Get or set current json_file_name."""
        return self._json_file_name

    @json_file_name.setter
    def json_file_name(self, json_file_name):
        self._json_file_name = json_file_name

    def ui_components(self) -> None:
        """Load all UI components of MainWindow."""
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        self.tree_view = QTreeView()

        self.model = QJsonTreeModel()
        self.tree_view.setModel(self.model)
        self.tree_view.setColumnWidth(0, 512)
        self.tree_view.setColumnWidth(1, 256)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_right_click_menu)
        self.tree_view.setStyleSheet(QTREEVIEW_STYLESHEET)

        self.tree_view.setAlternatingRowColors(
            Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView", "set_alternating_row_colors")))
        self.tree_view.setAnimated(
            Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView", "set_animated")))

        self.model.clear()
        self.model.load(self.json_text)

        layout.addWidget(self .tree_view)

        if Utils().string_to_boolean(CONFIG_OBJECT.get("QTreeView-expand", "expand_all")):
            self.tree_view.expandAll()
        if int(CONFIG_OBJECT.get("QTreeView-expand", "expand_to_depth")) >= -1:
            self.tree_view.expandToDepth(
                int(CONFIG_OBJECT.get("QTreeView-expand", "expand_to_depth")))

        self.setCentralWidget(widget)


    def closeEvent(self, event):
        """Close event for QMainWindow."""
        self.check_saved_before_exit()

    def create_menu_bar(self) -> None:
        """Creates menu bar."""
        self.setMenuBar(self.menu_bar)
        self.init_file_menu()
        self.init_view_menu()

    def init_file_menu(self) -> None:
        """Creates menu file item."""
        self.menu_file.setTitle(TRANSLATE_MAINWINDOW.gettext("File"))

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

        self.action_close_app.triggered.connect(self.close)
        self.action_close_app.setText(TRANSLATE_MAINWINDOW.gettext("Quit"))
        self.action_close_app.setShortcut("Ctrl+Q")

    def init_view_menu(self) -> None:
        """Creates menu view item."""
        self.action_is_editable.triggered.connect(self.action_change_flags)
        self.action_is_editable.setText(TRANSLATE_MAINWINDOW.gettext("Editable"))

        self.menu_view.setTitle(TRANSLATE_MAINWINDOW.gettext("View"))
        self.menu_expand.setTitle(TRANSLATE_MAINWINDOW.gettext("Expand"))

        self.action_collapse.triggered.connect(partial(self.action_expand_tree, "Collapse"))
        self.action_collapse.setText(TRANSLATE_MAINWINDOW.gettext("Collapse"))

        self.action_all.triggered.connect(partial(self.action_expand_tree, "All"))
        self.action_all.setText(TRANSLATE_MAINWINDOW.gettext("All"))

        self.menu_expand_to_level.setTitle(TRANSLATE_MAINWINDOW.gettext("To Level"))

        self.action_one_child.triggered.connect(partial(self.action_expand_tree, "1"))
        self.action_one_child.setText(TRANSLATE_MAINWINDOW.gettext("1"))
        self.action_two_child.triggered.connect(partial(self.action_expand_tree, "2"))
        self.action_two_child.setText(TRANSLATE_MAINWINDOW.gettext("2"))
        self.action_three_child.triggered.connect(partial(self.action_expand_tree, "3"))
        self.action_three_child.setText(TRANSLATE_MAINWINDOW.gettext("3"))

        self.menu_color.setTitle(TRANSLATE_MAINWINDOW.gettext("Color"))

        self.action_none_color.triggered.connect(partial(self.action_tree_color, "None"))
        self.action_none_color.setText(TRANSLATE_MAINWINDOW.gettext("None"))

        self.action_yellow_color.triggered.connect(partial(self.action_tree_color, "Yellow"))
        self.action_yellow_color.setText(TRANSLATE_MAINWINDOW.gettext("Yellow"))

        self.action_orange_color.triggered.connect(partial(self.action_tree_color, "Orange"))
        self.action_orange_color.setText(TRANSLATE_MAINWINDOW.gettext("Orange"))

        self.action_red_color.triggered.connect(partial(self.action_tree_color, "Red"))
        self.action_red_color.setText(TRANSLATE_MAINWINDOW.gettext("Red"))

        self.action_green_color.triggered.connect(partial(self.action_tree_color, "Green"))
        self.action_green_color.setText(TRANSLATE_MAINWINDOW.gettext("Green"))

        self.action_blue_color.triggered.connect(partial(self.action_tree_color, "Blue"))
        self.action_blue_color.setText(TRANSLATE_MAINWINDOW.gettext("Blue"))

        self.action_purple_color.triggered.connect(partial(self.action_tree_color, "Purple"))
        self.action_purple_color.setText(TRANSLATE_MAINWINDOW.gettext("Purple"))

        self.action_grey_color.triggered.connect(partial(self.action_tree_color, "Grey"))
        self.action_grey_color.setText(TRANSLATE_MAINWINDOW.gettext("Grey"))

    def action_new_json_file(self) -> None:
        """Creates new an empty JSON-file to QTreeView.

        Changes window title to "untilted" and loads to QTreeView model an empty dictionary
        """
        self.json_file_name = TRANSLATE_MAINWINDOW.gettext("untilted")
        self.setWindowTitle(self.json_file_name)
        self.model.clear()
        self.model.load({TRANSLATE_MAINWINDOW.gettext("[No data]"):
                         TRANSLATE_MAINWINDOW.gettext("[No data]")})

    def action_open_file_dialog(self) -> None:
        """Opens file dialog to for opening new JSON-file."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            TRANSLATE_MAINWINDOW.gettext("Choose JSON File"),
            "",
            "JSON Files (*.json)",
            options=options)
        if file_name:
            self.json_file_name = file_name
            self.model.load(JsonParsing().get_json_from_file(file_name))
            self.setWindowTitle(file_name)

    def action_save_json_file(self) -> None:
        """Saves JSON to file.

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
                message = TRANSLATE_MAINWINDOW.gettext(
                    "Failed to save file. Choose `Save As...` function.")
                self.create_message_box(
                    message=message,
                    type="Critical")
            else:
                JsonParsing().write_json_to_file(
                    self.json_file_name, self.model.get_json_from_tree())

                # Update config default_json_file_name
                CONFIG_OBJECT["Other"]["default_json_file_name"] = str(self.json_file_name)
                with open(Utils().get_abs_file_path("utils/config/config.ini"), "w") as config_file:
                    CONFIG_OBJECT.write(config_file)
        except FileNotFoundError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "FileNotFoundError exception in action_save_json_file() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except OSError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "OSError exception in action_save_json_file() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "BaseException in action_save_json_file() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def action_save_json_file_as(self) -> None:
        """Saves JSON to file as new file.

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
                "JSON Files (*.json);;Text Files (*.txt);;All Files (*)")
            if file_name:
                if file_name[0] == "" and file_name[1] == "":
                    return

                new_file_name = None
                if file_name[1] == "Text Files (*.txt)":
                    if Utils().file_name_match(file_name[0], "txt"):
                        new_file_name = file_name[0]
                    else:
                        new_file_name = file_name[0] + ".txt"
                elif file_name[1] == "JSON Files (*.json)":
                    if Utils().file_name_match(file_name[0], "json"):
                        new_file_name = file_name[0]
                    else:
                        new_file_name = file_name[0] + ".json"
                else:
                    new_file_name = file_name[0]

                JsonParsing().write_json_to_file(new_file_name, self.model.get_json_from_tree())

                # load just added file to QTreeView
                self.json_file_name = new_file_name
                self.model.load(JsonParsing().get_json_from_file(new_file_name))
                self.setWindowTitle(new_file_name)

                # Update config default_json_file_name
                CONFIG_OBJECT["Other"]["default_json_file_name"] = str(self.json_file_name)
                with open(Utils().get_abs_file_path("utils/config/config.ini"), "w") as config_file:
                    CONFIG_OBJECT.write(config_file)
        except FileNotFoundError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "FileNotFoundError exception in action_save_json_file_as() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except OSError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "OSError exception in action_save_json_file_as() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "BaseException in action_save_json_file_as() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def action_refresh_json_file(self) -> None:
        """Loads JSON form file to QTreeView.

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
                message = TRANSLATE_MAINWINDOW.gettext(
                    "Failed to save file. Choose `Save As...` function.")
                self.create_message_box(
                    message=message,
                    type="Critical")
            else:
                self.model.load(
                    JsonParsing().get_json_from_file(self.json_file_name))
        except FileNotFoundError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "FileNotFoundError exception in action_refresh_json_file() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except OSError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "OSError exception in action_refresh_json_file() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "BaseException in action_refresh_json_file() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def action_change_flags(self) -> None:
        """Changes boolean parameter in QJsonTreeModel for editing or not item."""
        if self.action_is_editable.isChecked():
            self.model.is_editable = True
        else:
            self.model.is_editable = False

    def action_expand_tree(self, expand_lvl: str) -> None:
        """Expands QTreeView depending on input expand_lvl."""
        if expand_lvl == "Collapse":
            self.tree_view.collapseAll()
            CONFIG_OBJECT["QTreeView-expand"]["expand_all"] = "False"
            CONFIG_OBJECT["QTreeView-expand"]["expand_to_depth"] = "-2"
        elif expand_lvl == "All":
            self.tree_view.expandAll()
            CONFIG_OBJECT["QTreeView-expand"]["expand_all"] = "True"
            CONFIG_OBJECT["QTreeView-expand"]["expand_to_depth"] = "-1"
        else:
            self.tree_view.expandToDepth(int(expand_lvl) - 1)
            CONFIG_OBJECT["QTreeView-expand"]["expand_all"] = "False"
            CONFIG_OBJECT["QTreeView-expand"]["expand_to_depth"] = str(int(expand_lvl) - 1)
        with open(Utils().get_abs_file_path("utils/config/config.ini"), "w") as config_file:
            CONFIG_OBJECT.write(config_file)

    def action_tree_color(self, color: str) -> None:
        """Update QTreeView items color and write them to config.ini."""
        if color == "None":
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#FFFFFF"
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#FFFFFF"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#FFFFFF"
        elif color == "Yellow":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#FFEE58"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#FFF59D"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#FFFDE7"
        elif color == "Orange":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#FFA726"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#FFCC80"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#FFF3E0"
        elif color == "Red":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#EF5350"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#EF9A9A"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#FFEBEE"
        elif color == "Green":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#26A69A"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#80CBC4"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#E0F2F1"
        elif color == "Blue":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#29B6F6"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#81D4FA"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#E1F5FE"
        elif color == "Purple":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#AB47BC"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#CE93D8"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#F3E5F5"
        elif color == "Grey":
            CONFIG_OBJECT["QTreeView-color"]["color_list"] = "#757575"
            CONFIG_OBJECT["QTreeView-color"]["color_dict"] = "#BDBDBD"
            CONFIG_OBJECT["QTreeView-color"]["color_else"] = "#EEEEEE"
        else:
            pass
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText(TRANSLATE_MAINWINDOW.gettext("Application needs to be restarted!"))
        message.setWindowTitle(TRANSLATE_MAINWINDOW.gettext("Information"))
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return_value = message.exec()
        if return_value == QMessageBox.Ok:
            with open(Utils().get_abs_file_path("utils/config/config.ini"), "w") as config_file:
                CONFIG_OBJECT.write(config_file)
            os.execl(sys.executable, sys.executable, *sys.argv)

    def open_right_click_menu(self, position) -> None:
        """Opens right cklick menu on QTreeView items.

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
            action_add_item = right_click_menu.addMenu(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add Item")))

            action_add_item_str = action_add_item.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add string")))
            action_add_item_str.triggered.connect(
                partial(self.tree_add_item, Qt.DecorationRole))

            action_add_item_int = action_add_item.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add integer")))
            action_add_item_int.triggered.connect(
                partial(self.tree_add_item, Qt.ToolTipRole))

            action_add_item_bool = action_add_item.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add boolean")))
            action_add_item_bool.triggered.connect(
                partial(self.tree_add_item, Qt.StatusTipRole))

            action_add_dictionary = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add dict()")))
            action_add_dictionary.triggered.connect(
                partial(self.tree_add_item, Qt.WhatsThisRole))

            action_add_list = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Add list()")))
            action_add_list.triggered.connect(
                partial(self.tree_add_item, Qt.SizeHintRole))

            right_click_menu.addSeparator()

            action_insert_child = right_click_menu.addMenu(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child")))

            action_insert_child_str = action_insert_child.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert child string")))
            action_insert_child_str.triggered.connect(
                partial(self.tree_add_item_child, Qt.DecorationRole))

            action_insert_child_int = action_insert_child.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert child integer")))
            action_insert_child_int.triggered.connect(
                partial(self.tree_add_item_child, Qt.ToolTipRole))

            action_insert_child_bool = action_insert_child.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert child boolean")))
            action_insert_child_bool.triggered.connect(
                partial(self.tree_add_item_child, Qt.StatusTipRole))

            action_insert_child_dict = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child dict()")))
            action_insert_child_dict.triggered.connect(
                partial(self.tree_add_item_child, Qt.WhatsThisRole))

            action_insert_child_list = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Insert Child list()")))
            action_insert_child_list.triggered.connect(
                partial(self.tree_add_item_child, Qt.SizeHintRole))

            right_click_menu.addSeparator()

            action_delete_item = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Delete Item")))
            action_delete_item.triggered.connect(
                partial(self.tree_item_delete))

            right_click_menu.addSeparator()

            file_name = str(self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole))
            action_tree_item_open_json_file = right_click_menu.addAction(
                self.tr(TRANSLATE_MAINWINDOW.gettext("Open File")))
            action_tree_item_open_json_file.triggered.connect(
                partial(self.tree_item_open_json_file, file_name))

            empty_value = self.model.data(self.tree_view.selectedIndexes()[1], Qt.EditRole) == ""

            if not self.model.is_editable:
                action_add_item.menuAction().setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.menuAction().setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_delete_item.setVisible(False)

                if not empty_value and Utils().file_name_match(file_name, "json"):
                    action_tree_item_open_json_file.setVisible(True)
                else:
                    action_tree_item_open_json_file.setVisible(False)
            else:
                is_parent_root = self.model.data(parent, Qt.EditRole) is None
                item_type_dict_or_list = \
                    self.model.getItem(self.tree_view.selectedIndexes()[1]).type is dict or \
                    self.model.getItem(self.tree_view.selectedIndexes()[1]).type is list

                action_add_item.menuAction().setVisible(False)
                action_add_dictionary.setVisible(False)
                action_add_list.setVisible(False)
                action_insert_child.menuAction().setVisible(False)
                action_insert_child_dict.setVisible(False)
                action_insert_child_list.setVisible(False)
                action_delete_item.setVisible(True)
                action_tree_item_open_json_file.setVisible(False)
                if is_parent_root and not item_type_dict_or_list:
                    action_add_item.menuAction().setVisible(True)
                    action_add_dictionary.setVisible(True)
                    action_add_list.setVisible(True)
                    if not empty_value and Utils().file_name_match(file_name, "json"):
                        action_tree_item_open_json_file.setVisible(True)
                elif is_parent_root and item_type_dict_or_list:
                    action_add_item.menuAction().setVisible(True)
                    action_add_dictionary.setVisible(True)
                    action_add_list.setVisible(True)
                    action_insert_child.menuAction().setVisible(True)
                    action_insert_child_dict.setVisible(True)
                    action_insert_child_list.setVisible(True)
                elif not is_parent_root and item_type_dict_or_list:
                    action_insert_child.menuAction().setVisible(True)
                    action_insert_child_dict.setVisible(True)
                    action_insert_child_list.setVisible(True)
                elif item_type_dict_or_list:
                    action_insert_child.menuAction().setVisible(True)
                    action_insert_child_dict.setVisible(True)
                    action_insert_child_list.setVisible(True)
                elif not empty_value and Utils().file_name_match(file_name, "json"):
                    action_tree_item_open_json_file.setVisible(True)
                elif is_parent_root:
                    action_add_item.menuAction().setVisible(True)
                    action_add_dictionary.setVisible(True)
                    action_add_list.setVisible(True)

            right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))
        except IndexError as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "IndexError exception in open_right_click_menu() function: %s") % \
                str(exception)
            self.create_message_box(
                message=message,
                type="Critical")
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "BaseException in open_right_click_menu() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def tree_add_item(self, role: Qt.ItemDataRole) -> None:
        """Adds item to the model.

        Adding items to QTreeView depends on the input role.
        Qt.EditRole = str(), Qt.DisplayRole = dict(), Qt.ToolTipRole = list()

        Raises:
        -------
            Exception:
                Basic exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index.parent()

            if self.model.data(parent, Qt.EditRole) is None:
                if not self.model.insertRow(index.row() + 1, parent):
                    return

                for column in range(self.model.columnCount(parent)):
                    child = self.model.index(index.row() + 1, column, parent)
                    if role == Qt.DecorationRole:
                        self.model.setData(
                            index=child,
                            value=TRANSLATE_MAINWINDOW.gettext("[No string key]"),
                            role=role)
                        self.model.getItem(child).type = str
                        return
                    elif role == Qt.ToolTipRole:
                        self.model.setData(
                            index=child,
                            value=TRANSLATE_MAINWINDOW.gettext("[No int data]"),
                            role=role)
                        self.model.getItem(child).type = int
                        return
                    elif role == Qt.StatusTipRole:
                        self.model.setData(
                            index=child,
                            value=TRANSLATE_MAINWINDOW.gettext("[No bool data]"),
                            role=role)
                        self.model.getItem(child).type = bool
                        return
                    elif role == Qt.WhatsThisRole:
                        self.model.setData(index=child, value=None, role=role)
                        self.model.getItem(child).type = dict
                        return
                    elif role == Qt.SizeHintRole:
                        self.model.setData(index=child, value=None, role=role)
                        self.model.getItem(child).type = list
                        return
                    else:
                        return
            else:
                message = TRANSLATE_MAINWINDOW.gettext(
                    "You can only use this function to root QTreeView Node, choose another actions")
                self.create_message_box(
                    message=message,
                    type="Critical")
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "Exception in tree_add_item() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def tree_add_item_child(self, role: Qt.ItemDataRole) -> None:
        """Adds child item to the model.

        Adding child items to QTreeView depends on the input role.
        Qt.EditRole = str(), Qt.DisplayRole = dict(), Qt.ToolTipRole = list()
        When adding dict() or list() it is impossible to add them and work with them immediately
        after. Firstly it is needed to save model and only then to work with it.

        Args:
        -----
            role: Qt.ItemDataRole
                Input role

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
                if role == Qt.DecorationRole:
                    self.model.setData(
                        index=child,
                        value=TRANSLATE_MAINWINDOW.gettext("[No string key]"),
                        role=role)
                    self.model.getItem(child).type = str
                elif role == Qt.ToolTipRole:
                    self.model.setData(
                        index=child,
                        value=TRANSLATE_MAINWINDOW.gettext("[No int data]"),
                        role=role)
                    self.model.getItem(child).type = int
                elif role == Qt.StatusTipRole:
                    self.model.setData(
                        index=child,
                        value=TRANSLATE_MAINWINDOW.gettext("[No bool data]"),
                        role=role)
                    self.model.getItem(child).type = bool
                elif role == Qt.WhatsThisRole:
                    self.model.setData(
                        index=child,
                        value=None,
                        role=role)
                    self.model.getItem(child).type = dict
                elif role == Qt.SizeHintRole:
                    self.model.setData(
                        index=child,
                        value=None,
                        role=role)
                    self.model.getItem(child).type = list
                self.tree_view.expand(index)
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "Exception in tree_add_item_child() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def tree_item_delete(self) -> None:
        """Removes item from model.

        Raises:
        -------
            BaseException:
                Basic exception
        """
        try:
            index = self.tree_view.selectionModel().currentIndex()
            parent = index.parent()

            self.model.removeRows(
                position=index.row(),
                rows=1,
                parent=parent)
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "Exception in tree_item_delete() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def tree_item_open_json_file(self, file_name: str) -> None:
        """Open new window from QTreeView.

        Opens file name from QTreeView if file matches to .json file extensions.

        Args:
        -----
            file_name: str
                File name

        Raises:
        -------
            BaseException:
                Basic exception
        """
        try:
            file_path = os.path.dirname(self.json_file_name)
            file_path = os.path.join(file_path, file_name)
            self.new_window = MainWindow(
                json_file_name=file_path,
                show_maximized=False)
        except BaseException as exception:
            message = TRANSLATE_MAINWINDOW.gettext(
                "Exception in tree_item_open_json_file() function: %s") % str(exception)
            self.create_message_box(
                message=message,
                type="Critical")

    def center(self):
        """Centering main window."""
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def create_message_box(self, message: str, type: str) -> None:
        """Creates message box with predefined string message and type.

        Args:
        -----
            message: str
                Message to display in QMessageBox
            type: str
                Type of icon to display
        """
        windows_title = ""
        message_box = QMessageBox()

        if type == "Question":
            pass
        elif type == "Information":
            windows_title = TRANSLATE_MAINWINDOW.gettext("Information")
            message_box.setIcon(QMessageBox.Information)
        elif type == "Warning":
            windows_title = TRANSLATE_MAINWINDOW.gettext("Warning")
            message_box.setIcon(QMessageBox.Warning)
        elif type == "Critical":
            windows_title = TRANSLATE_MAINWINDOW.gettext("Critical")
            message_box.setIcon(QMessageBox.Critical)

        message_box.setText(message)
        message_box.setWindowTitle(windows_title)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()

    def check_saved_before_exit(self):
        """Shows QMessageBox if data was not saved.

        Checks if data from model does not match to json_file data and throws an QMessageBox
        with the offer to save information
        """
        if self.model.get_json_from_tree() != JsonParsing().get_json_from_file(self.json_file_name):
            message = QMessageBox()
            message.setIcon(QMessageBox.Warning)
            message.setText(TRANSLATE_MAINWINDOW.gettext("Save changes to file before closing?"))
            message.setWindowTitle(TRANSLATE_MAINWINDOW.gettext("Warning"))
            message.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
            return_value = message.exec()
            if return_value == QMessageBox.Save:
                self.action_save_json_file()
