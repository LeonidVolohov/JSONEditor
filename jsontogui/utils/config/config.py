"""This module creates config.ini file for an easier changing Application properties."""
from configparser import ConfigParser


CONFIG_OBJECT = ConfigParser()

CONFIG_OBJECT["QTreeView"] = {
    "set_alternating_row_colors": "False",
    "set_animated": "False"
}

CONFIG_OBJECT["QTreeView-expand"] = {
    "expand_all": "False",

    # -2: Dont Expand, -1: ExpandAll, 0: Expand to 1 level, ...
    "expand_to_depth": "-2"
}

CONFIG_OBJECT["QTreeView-color"] = {
    "color_dict": "#90CAF9",
    "color_list": "#BBDEFB",
    "color_else": "#E3F2FD"
}

CONFIG_OBJECT["Other"] = {
    "default_json_file_name": "config_apak.json" # default: ""
}

CONFIG_OBJECT["Language"] = {
    "default_gui_language": "en", # Language for GUI
    "default_tree_language": "en", # Language for QTreeView
    "write_to_json_language": "en" # Language for writing back to JSON-file
}

CONFIG_OBJECT["MainWindow"] = {
    "show_maximized": "False"
}

with open("config.ini", "w") as config:
    CONFIG_OBJECT.write(config)
