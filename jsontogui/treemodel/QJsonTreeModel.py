"""This module create model for QTreeView

QTreeView allow to display data providen by models derived from the QAbstractItemModel.
Due to this QJsonTreeModel inherited from QAbstractItemModel with some overriden methods.

    Typical usage example:
    ----------------------

    model = QJsonTreeModel()
    model.load({"Example key", "Example value"})
    model.get_json_from_tree()
"""
import sys
import gettext
from configparser import ConfigParser

from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt5 import QtGui

sys.path.insert(1, "..")
from utils.Utils import Utils
from utils.JsonParsing import JsonParsing
sys.path.insert(1, Utils().get_abs_file_path("treemodel"))
from QJsonTreeItem import QJsonTreeItem


CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read("utils/config/config.ini")

TRANSLATE_QJSONTREEMODEL = gettext.translation(
    domain="QJsonTreeModel",
    localedir=Utils().get_abs_file_path("utils/locale"),
    languages=[CONFIG_OBJECT.get("Language", "default_gui_language")])
TRANSLATE_QJSONTREEMODEL.install()

class QJsonTreeModel(QAbstractItemModel):
    """Class to create basic tree item.

    Attributes:
    -----------
    root_item:
        Root item
    headers:
        Headers of column=0 and column=1

    Methods:
    --------
    clear:
        Clear model by loading an empty dict to it
    load:
        Loads input document to QTreeView
    data:
        Return data for specific input index
    getItem:
        Return item for specific input index
    setData:
        Sets input value for specific index depends of input role
    headerData:
        Return header data
    index:
        Return index for specific row and column
    parent:
        Return parent for specific index
    rowCount:
        Return amount of rows for specific parent
    columnCount:
        Return amount of columns
    flags:
        Sets flags on displaying or editing specific column
    getJsonFromTree:
        Return JSON from tree
    generateJsonFromTree:
        Generate JSON from tree
    insertRows:
        Inserts rows for specific position
    removeRows:
        Removes rows for specific position
    """

    def __init__(self, parent=None) -> None:
        """Constructs all the necessary attributes for the QJsonTreeModel object.

        Args:
        -----
            parent:
                Parent of the model. Default is None
        """
        super(QJsonTreeModel, self).__init__(parent)
        self._root_item = QJsonTreeItem(
            [TRANSLATE_QJSONTREEMODEL.gettext("Key"),
             TRANSLATE_QJSONTREEMODEL.gettext("Value"),
             TRANSLATE_QJSONTREEMODEL.gettext("Type")])
        self._headers = (
            TRANSLATE_QJSONTREEMODEL.gettext("Key"),
            TRANSLATE_QJSONTREEMODEL.gettext("Value"),
            TRANSLATE_QJSONTREEMODEL.gettext("Type"))
        self._is_editable = False

    @property
    def is_editable(self):
        """Get or set current _is_editable property."""
        return self._is_editable

    @is_editable.setter
    def is_editable(self, is_editable):
        self._is_editable = is_editable

    def clear(self) -> None:
        """Clear model.

        Clear model by loading to it an empty dictionary
        """
        self.load({})

    def load(self, document: dict) -> None:
        """Load JSON to the model.

        Load input document to the model. If document is not dict, list or tuple
        it throws an error message.

        Args:
        -----
            document: dict
                JSON file previously saved to the dictionary

        Returns:
        --------
            True if model was successfully loaded
        """
        assert isinstance(document, (dict, list, tuple)), (
            TRANSLATE_QJSONTREEMODEL.gettext("`document` must be of dict, list or tuple, not %s" %
                                             (type(document)))
        )

        self.beginResetModel()

        self._root_item = QJsonTreeItem.load_json_to_tree(document)
        self._root_item.type = type(document)

        self.endResetModel()
        return True

    @classmethod
    def data(cls, index: QModelIndex, role: Qt.ItemDataRole) -> str:
        """Return data for specific index.

        Returns the data stored under the given role for the item referred to by the index.
        Return if role is Qt.DisplayRole or Qt.EditRole; otherwise returns None.

        Args:
        -----
            index: QModelIndex
                Index to display data for
            role: Qt.ItemDataRole
                Role. Only Qt.DisplayRole or Qt.EditRole

        Returns:
        --------
            True data if role is acceptable and index is valid; otherwise None
        """
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return item.data(index.column())
            if index.column() == 1:
                return item.value
            if index.column() == 2:
                if str(item.type) == "<class 'str'>":
                    return TRANSLATE_QJSONTREEMODEL.gettext("str")
                elif str(item.type) == "<class 'int'>":
                    return TRANSLATE_QJSONTREEMODEL.gettext("int")
                elif str(item.type) == "<class 'bool'>":
                    return TRANSLATE_QJSONTREEMODEL.gettext("bool")
                else:
                    return

        if role == Qt.CheckStateRole and item.type is bool:
            if index.column() == 1:
                return Qt.Checked if item.value is True else Qt.Unchecked

        # if role == Qt.ForegroundRole:
        #     if item.type is dict:
        #         return QtGui.QBrush(QtGui.QColor('#FF9900'))
        #     elif item.type is list:
        #         return QtGui.QBrush(QtGui.QColor('#ff0080'))
        #     elif item.type is str or item.type is int or item.type is bool:
        #         pass

        # only one choose:
        # or Qt.ForegroundRole or in MainWindow in self.tree_view.setStyleSheet -> item
        if role == Qt.BackgroundRole:
            if item.data(index.parent().column()) is None:
                if item.type is dict:
                    return QtGui.QBrush(QtGui.QColor(
                        CONFIG_OBJECT.get("QTreeView-color", "color_dict")))
                if item.type is list:
                    return QtGui.QBrush(QtGui.QColor(
                        CONFIG_OBJECT.get("QTreeView-color", "color_list")))
                else:
                    return QtGui.QBrush(QtGui.QColor(
                        CONFIG_OBJECT.get("QTreeView-color", "color_else")))

        if role == Qt.FontRole:
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            if item.data(index.parent().column()) is None:
                if index.column() == 0:
                    font.setPointSize(14)
                elif index.column() == 1:
                    font.setItalic(True)
                    font.setPointSize(12)
                elif index.column() == 2:
                    font.setFamily("Tahoma")
                    font.setPointSize(10)
            else:
                if index.column() == 0:
                    if item.type is dict or item.type is list:
                        font.setBold(True)
                    else:
                        font.setBold(False)
                    font.setPointSize(10)
                elif index.column() == 1:
                    font.setBold(False)
                    font.setItalic(True)
                    font.setPointSize(10)
                elif index.column() == 2:
                    font.setFamily("Tahoma")
                    font.setPointSize(10)
            return font

        if role == Qt.DecorationRole:
            if index.column() == 0:
                if item.type is dict:
                    return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/object.png"))
                if item.type is list:
                    return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/array.png"))
                # if item.type is int:
                #     return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/int.png"))
                # if item.type is str and item.key != "file":
                #     return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/str.png"))
                # if item.type is bool:
                #     return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/bool.png"))
                if item.key == "file":
                    return QtGui.QIcon(QtGui.QPixmap("utils/images/treeview/file.png"))
            elif index.column() == 1:
                pass

        if role == Qt.TextAlignmentRole:
            if index.column() == 2:
                return Qt.AlignCenter
        return None

    def getItem(self, index: QModelIndex) -> QJsonTreeItem:
        """Return item for specific index.

        Return QJsonTreeItem for specific index if index is valid, else return root item.

        Args:
        -----
            index: QModelIndex
                Index to get data for

        Returns:
        --------
            QJsonTreeItem
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self._root_item

    def setData(self,
                index: QModelIndex,
                value: str=None,
                role: Qt.ItemDataRole=Qt.EditRole
               ) -> bool:
        """Sets value for specific index.

        Sets value for specific index.
        If role is Qt.EditRole, default edit
        If value is Qt.DecorationRole, then sets str() value.
        If value is Qt.ToolTipRole, then sets int() value.
        If value is Qt.StatusTipRole, then sets bool() value.
        If value is Qt.WhatsThisRole, then sets dict() value.
        If value is Qt.SizeHintRole, then sets list() value.

        Args:
        -----
            index: QModelIndex
                Index to set data for
            value: str
                Value to set
            role: Qt.ItemDataRole
                Depending on the role it sets str(), dict() or list()

        Returns:
        --------
            True if data was successfully seted, False if not
        """
        if role == Qt.EditRole:
            item = index.internalPointer()
            item.setData(index.column(), value)
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        if role == Qt.DecorationRole:
            item = index.internalPointer()
            if self.getItem(index).parent().type is list:
                item.setData(0, None)
            else:
                item.setData(0, value)
            item.setData(1, TRANSLATE_QJSONTREEMODEL.gettext("[No string value]"))
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        if role == Qt.ToolTipRole:
            item = index.internalPointer()
            if self.getItem(index).parent().type is list:
                item.setData(0, None)
            else:
                item.setData(0, value)
            item.setData(1, int(1))
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        if role == Qt.StatusTipRole:
            item = index.internalPointer()
            if self.getItem(index).parent().type is list:
                item.setData(0, None)
            else:
                item.setData(0, value)
            item.setData(1, False)
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        if role == Qt.WhatsThisRole:
            item = index.internalPointer()
            if self.getItem(index).parent().type is list:
                item.setData(0, None)
            else:
                item.setData(0, TRANSLATE_QJSONTREEMODEL.gettext("[No dict() name]"))
            item.setData(1, dict())
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        if role == Qt.SizeHintRole:
            item = index.internalPointer()
            if self.getItem(index).parent().type is list:
                item.setData(0, None)
            else:
                item.setData(0, TRANSLATE_QJSONTREEMODEL.gettext("[No list() name]"))
            item.setData(1, list())
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: Qt.ItemDataRole
                  ) -> str:
        """Return header data.

        Returns the data for the given role and section in the header
        with the specified orientation. For horizontal headers, the section
        number corresponds to the column number. Similarly, for vertical headers,
        the section number corresponds to the row number.

        Args:
        -----
            section: int
                Position of header data. 0 or 1
            orientation: Qt.Orientation
                Orientation
            role: Qt.ItemDataRole
                Role. Return header data only for Qt.DisplayRole role

        Returns:
        --------
            Return header data only for Qt.DisplayRole role, else return None
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

    def index(self, row: int, column: int, parent: QModelIndex=QModelIndex()) -> QModelIndex:
        """Return index.

        Returns the index of the item in the model specified by the given row,
        column and parent index.

        Args:
        -----
            row: int
                Row to return index of
            column: int
                Column to return index of
            parent: QModelIndex
                Parent

        Returns:
        --------
            QModelIndex
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Return parent of index.

        Returns the parent of the model item with the given index.
        If the item has no parent, an invalid QModelIndex is returned.

        Args:
        -----
            index: QModelIndex
                Index to return parent for

        Returns:
        --------
            QModelIndex
        """
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self._root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """Return amount of rows.

        Returns the number of rows under the given parent.
        When the parent is valid it means that rowCount is returning
        the number of children of parent.

        Args:
        -----
            parent: QModelIndex
                Parent to return row count for

        Returns:
        --------
            Amount of rows
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.childCount()

    def columnCount(self, parent: QModelIndex=QModelIndex()) -> int:
        """Return amount of column.

        Returns the number of columns for the children of the given parent.

        Args:
        -----
            parent: QModelIndex
                Parent to return column count for

        Returns:
        --------
            Amount of column
        """
        return 3

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Returns the item flags for the given index.

        Args:
        -----
            index: QModelIndex
                Index to return flags for

        Returns:
        --------
            Qt.ItemFlags
        """
        flags = super(QJsonTreeModel, self).flags(index)
        if self.is_editable:
            if index.column() == 0 or index.column() == 1:
                if self.getItem(index).type == dict or self.getItem(index).type == list:
                    if index.column() == 1:
                        return flags
                if self.getItem(index).parent().type is list:
                    if index.column() == 0:
                        return flags
                return Qt.ItemIsEditable | flags
            else:
                return flags
        else:
            return flags

    def insertRows(self, position: int, rows: int, parent: QModelIndex) -> bool:
        """Inserts rows.

        Inserts rows before the given row in the child items of the parent specified. Items in the
        new row will be children of the item represented by the parent model index.

        If position is 0, the rows are prepended to any existing rows in the parent.
        If position is rowCount(), the rows are appended to any existing rows in the parent.
        If parent has no children, a single column with count input rows is inserted.

        Args:
        -----
            position: int
                Given position
            rows: int
                Amount of rows
            parent: QmodelIndex
                Parent to insert rows in

        Returns:
        --------
            Returns True if the rows were successfully inserted; otherwise returns False.
        """
        parent_item = self.getItem(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        success = parent_item.insertChildren(position, rows, self._root_item.columnCount())
        self.endInsertRows()

        return success

    def removeRows(self, position: int, rows: int, parent: QModelIndex) -> bool:
        """Remove rows.

        Removes the given position row from the child items of the parent specified.
        On models that support this, removes amounr of rows starting with the given
        position under parent parent from the model.

        Args:
        -----
            position: int
                Given position
            rows: int
                Amount of rows
            parent: QmodelIndex
                Parent to remove rows in

        Returns:
        --------
            Returns True if the rows were successfully removed; otherwise returns False.
        """
        parent_item = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parent_item.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def get_json_from_tree(self, root: QJsonTreeItem=None) -> dict:
        """Gets JSON from tree.

        Args:
        -----
            root: QJsonTreeItem
                Root of the model

        Returns:
        --------
            Generated JSON from tree to dictionary
        """
        root = root or self._root_item
        return self.generate_json_from_free(root)

    def generate_json_from_free(self, item) -> dict:
        """Recursive function to generate JSON from tree.

        Args:
        -----
            item: dict(), list() or str()
                Item of the tree

        Returns:
        --------
            Generated JSON from tree to dictionary
        """

        if item is None:
            item = self._rootItem

        amount_of_child = item.childCount()

        if item.type is dict:
            document = {}
            for i in range(amount_of_child):
                child = item.child(i)
                document[
                    JsonParsing().translate(
                        child.key,
                        CONFIG_OBJECT.get("Language", "write_to_json_language"))] = \
                    self.generate_json_from_free(child)
            return document
        elif item.type == list:
            document = []
            for i in range(amount_of_child):
                child = item.child(i)
                document.append(self.generate_json_from_free(child))
            return document
        else:
            return item.value
