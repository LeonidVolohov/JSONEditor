"""This module does basic operations to prepare input json file for further analysis.

    Typical usage example:
    ----------------------

    json_parsing = Utils()
    json_parsing.get_json_from_file("example.json")
    json_parsing.write_json_to_file("example.json")
    json_parsing.get_name_from_dict({"name": "username"})
"""
import json
import gettext
from collections import OrderedDict
from configparser import ConfigParser

from utils.Utils import Utils


CONFIG_OBJECT = ConfigParser()
CONFIG_OBJECT.read("utils/config/config.ini")

TRANSLATE_JSONPARSING = gettext.translation(
    domain="JsonParsing",
    localedir=Utils().get_abs_file_path("utils/locale"),
    languages=[CONFIG_OBJECT.get("Language", "default_gui_language")])
TRANSLATE_JSONPARSING.install()

class JsonParsing():
    """Class parsing JSON-file for further analysis.

    Attributes:
    -----------
    file_name:
        File name of the file to work with

    Methods:
    --------
    get_json_from_file() -> dict:
        Return JSON data from given file_name

    write_json_to_file(json_data: str) -> None:
        Write to given file_name given json_data

    get_name_from_dict(data: dict) -> str
        Return str with some parameters which was found from given data
    """

    def __init__(self, file_name: str=None) -> None:
        """Constructs all the necessary attributes for the Utils object.

        Args:
        -----
            _file_name:
                File name of the file to work with.
        """
        self._file_name = file_name

    @property
    def file_name(self):
        """Get or set current file_name"""
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    def get_json_from_file(self) -> dict:
        """Get JSON from file.

        Return dictionary filled with JSONs data.

        Args:
        -----
            None

        Returns:
        --------
            Return dictionary filled with data from self.file_name

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
            with open(self.file_name, mode='r', encoding="utf-8") as opened_file:
                json_data = json.load(opened_file)

                # In Json there is a property for sorting keys (sort_Keys=True (False by default)),
                # so there is no need in this:
                # return OrderedDict(sorted(json_data.items()))
                return json_data
        except FileNotFoundError:
            print("Could not found the file: %s" % self.file_name)
        except OSError:
            print("OSError occurred trying open the file: %s" % self.file_name)
        except BaseException as exception:
            print("BaseException occurred trying open the file: %s" % self.file_name)
            print(exception)


    def write_json_to_file(self, json_data: dict) -> None:
        """Write JSON to file.

        Write json_data (dictionary) to self.file_name

        Args:
        -----
            json_data: dict
                Dictionary with JSON-data

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
                Base exception if others could not the catch exception
        """
        try:
            with open(self.file_name, mode="w", encoding="utf-8") as opened_file:
                opened_file.write(
                    json.dumps(
                        json_data,
                        indent=2,
                        ensure_ascii=False,
                        sort_keys=True))
        except FileNotFoundError:
            print("Could not found the file: %s" % self.file_name)
        except OSError:
            print("OSError occurred trying write to the file: %s" % self.file_name)
        except BaseException as exception:
            print("BaseException occurred trying write to the file: %s" % self.file_name)
            print(exception)

    @classmethod
    def get_name_from_dict(cls, data: dict) -> str:
        """Gets predefined params from data

        Return string with predefined parameters which was found in data. Predefined
        parameters starts and ends with "__"

        Args:
        -----
            json_data: dict
                Dictionary from JSON

        Returns:
        --------
            Return string with predefined parameters which was found in data.
            Predefied parameters are: "name", "group" and "description".
            If parameters was not found it returns default string
            which is "__Object__"

        Raises:
        -------
            None
        """
        if isinstance(data, dict):
            output_string = TRANSLATE_JSONPARSING.gettext("Object")

            ordered_dict = OrderedDict()
            ordered_dict[TRANSLATE_JSONPARSING.gettext("Name")] = data.get(
                'name', None)
            ordered_dict[TRANSLATE_JSONPARSING.gettext("Group")] = data.get(
                'group', None)
            filtered_dict = {key: value for key, value in ordered_dict.items() if value is not None}

            ordered_dict.clear()
            ordered_dict.update(filtered_dict)

            if len(ordered_dict) > 0:
                output_string = ";  ".join(["%s: %s" % (key, value)
                                            for (key, value) in ordered_dict.items()])
            return output_string
        if isinstance(data, list):
            pass
        if isinstance(data, tuple):
            pass
