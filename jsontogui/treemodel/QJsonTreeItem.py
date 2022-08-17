"""This module create basic TreeItem for QJsonTreeModel

    Typical usage example:
    ----------------------

    rootItem = QJsonTreeItem("Key", "Value")
    document = {"Example": "Example value"}
    rootItem.load_json_to_tree(document)
"""
import sys
from configparser import ConfigParser

sys.path.insert(1, "..")
from utils.JsonParsing import JsonParsing
from utils.Utils import Utils

CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read(Utils().get_abs_file_path("utils/config/config.ini"))


class QJsonTreeItem(object):
    """Class to create basic tree item

    Attributes:
    -----------
    data:
        Data for the tree item
    parent:
        Parent of the item

    Methods:
    --------
    appendChild:
        Appends child to the list
    child:
        Return child for specific row
    parent:
        Return parent
    childCount:
        Return length of list
    columnCount:
        Return column count
    row:
        Return index of tree
    data:
        Return data for specific column
    setData:
        Sets given data for specific column
    insertChildren:
        Insert children for specific row and column
    removeChildren:
        Remove children from specicif row
    load_json_to_tree:
        Prepare data to load it to tree
    """

    def __init__(self, data, parent=None) -> None:
        self._parent = parent
        self._key = ""
        self._value = ""
        self._type = None
        self._children = list()
        self.item_data = data

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, typ):
        self._type = typ

    def appendChild(self, item) -> None:
        self._children.append(item)

    def child(self, row) -> None:
        return self._children[row]

    def parent(self) -> None:
        return self._parent

    def childCount(self) -> None:
        return len(self._children)

    def columnCount(self) -> None:
        return len(self.item_data)

    def row(self) -> None:
        return (
            self._parent._children.index(self) if self._parent
            else 0
        )

    def data(self, column) -> None:
        if column is 0:
            return self.key
        elif column is 2:
            return self.value

    def setData(self, column, value) -> None:
        if column is 0:
            self.key = value
        if column is 2:
            self.value = value

    def insertChildren(self, position, rows, columns) -> bool:
        if position < 0 or position > len(self._children):
            return False

        for row in range(rows):
            data = [None for v in range(columns)]
            item = QJsonTreeItem(data, self)
            self._children.insert(position, item)

        return True

    def removeChildren(self, position, rows) -> bool:
        if position < 0 or position + rows > len(self._children):
            return False

        for row in range(rows):
            self._children.pop(position)

        return True

    @classmethod
    def load_json_to_tree(cls, value, parent=None, sort: bool=True):
        """Loads JSON to tree.

        Recursion function to prepare data for further loading to QTreeView

        Args:
        -----
            value: Any
                Value to load
            parent: QJsonTreeItem
                Parent item
            sort: bool
                Sort or not

        Returns:
        --------
            QJsonTreeItem
        """
        root_item = QJsonTreeItem(parent=parent, data=value)
        root_item.key = "root"

        if isinstance(value, dict):
            items = (
                sorted(value.items())
                if sort else value.items()
            )

            for key, value in items:
                child = cls.load_json_to_tree(value, root_item)
                child.key = JsonParsing().translate(
                    key, CONFIG_OBJECT.get("Language", "default_tree_language"))
                child.type = type(value)
                root_item.appendChild(child)
        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load_json_to_tree(value, root_item)
                child.key = JsonParsing().get_name_from_dict(value)
                child.type = type(value)
                root_item.appendChild(child)
        else:
            root_item.value = value
            root_item.type = type(value)

        return root_item
